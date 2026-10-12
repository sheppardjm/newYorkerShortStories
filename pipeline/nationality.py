"""Look up each author's country of citizenship and ethnic group on Wikidata.

Pass 1 matches names in bulk through the SPARQL endpoint (label or alias, humans
only).  Pass 2 falls back to the search API, slowly, for names that didn't match.
Writes pipeline/data/wd_authors.json (raw cache) and nationality_auto.json
(author -> countries / ethnic groups / match).  Hand corrections go in
nationality_overrides.json, which build.py applies on top.  Standard library only.
"""
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
import json, re, sys, time, collections, urllib.request, urllib.parse

UA = {'User-Agent': 'NewYorkerFictionByLength/1.0 (github.com/sheppardjm; nationality tagging)', 'Accept': 'application/sparql-results+json'}
API = 'https://www.wikidata.org/w/api.php'; SPARQL = 'https://query.wikidata.org/sparql'
WRITER_OCC = {'Q36180','Q6625963','Q49757','Q4853732','Q1930187','Q214917','Q28389','Q11774202','Q482980','Q487596','Q18844224','Q15980158','Q1209498','Q3658608','Q333634','Q1607826','Q4164507','Q2526255','Q11774156','Q13570226','Q10297252','Q3387717','Q1281618','Q2306091','Q8178443','Q201788','Q15296811','Q12144794','Q18814623','Q1569495','Q2516866','Q16287483'}
WRITER_WORDS = re.compile(r'\b(writer|novelist|author|poet|journalist|playwright|essayist|humou?rist|critic|screenwriter|translator|editor|cartoonist|memoirist|dramatist|short[- ]story)\b', re.I)

def fetch(url, data=None):
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, data=data, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            err = e; wait = int(e.headers.get('Retry-After', 0) or 0) or 15 * (attempt + 1)
            print('  HTTP', e.code, 'waiting', wait, file=sys.stderr); time.sleep(wait)
        except Exception as e:
            err = e; time.sleep(5 * (attempt + 1))
    raise err

def sparql(q): return fetch(SPARQL, urllib.parse.urlencode({'query': q, 'format': 'json'}).encode())['results']['bindings']
def qid(u): return u.rsplit('/', 1)[-1]
def yr(v): m = re.match(r'(-?\d{4})', v or ''); return int(m.group(1)) if m else None

def score(rec, first):
    s = 0
    if set(rec['P106']) & WRITER_OCC: s += 3
    if WRITER_WORDS.search(rec.get('desc', '')): s += 2
    b = rec.get('born')
    if b and b <= first - 14: s += 1
    if b and b > first - 12: s -= 5
    if rec.get('died') and rec['died'] < 1900: s -= 3
    if not rec['P106'] and not rec.get('desc'): s -= 1
    return s

def main():
    d = json.load(open('../../public/data.json'))
    def mainauth(a): return re.split(r',\s*|\s+and\s+', a or '')[0].strip()
    first = {}
    for r in d:
        a = mainauth(r[1])
        if a: first[a] = min(first.get(a, 9999), r[2])
    cache = json.load(open('wd_authors.json')) if os.path.exists('wd_authors.json') else {}
    if '--retry' in sys.argv: cache = {a: v for a, v in cache.items() if v.get('qid')}  # retry misses
    todo = [a for a in first if a not in cache]
    print(len(first), 'authors,', len(todo), 'to look up', file=sys.stderr)

    # Pass 1: bulk label/alias match
    def clean(a): return re.sub(r'\s*\(.*?\)', '', a).replace('’', "'").strip()
    B = 40
    for i in range(0, len(todo), B):
        names = todo[i:i+B]
        variants = {}
        for a in names:
            for v in {clean(a), clean(a).replace("'", '’'), re.sub(r'\.(?=\S)', '. ', clean(a)).replace('  ', ' ')}: variants[v] = a
        vals = ' '.join(json.dumps(v) + '@en' for v in variants)
        q = f'''SELECT ?name ?item ?itemDescription ?born ?died
          (GROUP_CONCAT(DISTINCT ?occ;separator="|") AS ?occs) (GROUP_CONCAT(DISTINCT ?c;separator="|") AS ?cs)
          (GROUP_CONCAT(DISTINCT ?e;separator="|") AS ?es) (GROUP_CONCAT(DISTINCT ?bc;separator="|") AS ?bcs) WHERE {{
          VALUES ?name {{ {vals} }}
          ?item rdfs:label|skos:altLabel ?name . ?item wdt:P31 wd:Q5 .
          OPTIONAL {{ ?item wdt:P106 ?occ }} OPTIONAL {{ ?item wdt:P569 ?born }} OPTIONAL {{ ?item wdt:P570 ?died }}
          OPTIONAL {{ ?item wdt:P27 ?c }} OPTIONAL {{ ?item wdt:P172 ?e }} OPTIONAL {{ ?item wdt:P19/wdt:P17 ?bc }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }} GROUP BY ?name ?item ?itemDescription ?born ?died'''
        rows = sparql(q)
        cands = collections.defaultdict(dict)
        for r in rows:
            a = variants.get(r['name']['value']);
            if not a: continue
            it = qid(r['item']['value'])
            rec = {'qid': it, 'label': r['name']['value'], 'desc': r.get('itemDescription', {}).get('value', ''),
                   'P106': [qid(x) for x in r['occs']['value'].split('|') if x], 'P27': [qid(x) for x in r['cs']['value'].split('|') if x],
                   'P172': [qid(x) for x in r['es']['value'].split('|') if x], 'birthC': [qid(x) for x in r['bcs']['value'].split('|') if x],
                   'born': yr(r.get('born', {}).get('value')), 'died': yr(r.get('died', {}).get('value'))}
            if it in cands[a]:  # same item twice (multiple birth dates); merge
                for k in ('P106', 'P27', 'P172', 'birthC'): rec[k] = sorted(set(rec[k]) | set(cands[a][it][k]))
            cands[a][it] = rec
        for a in names:
            best = None
            for rec in cands.get(a, {}).values():
                rec['score'] = score(rec, first[a])
                if rec['score'] >= 2 and (best is None or rec['score'] > best['score']): best = rec
            cache[a] = dict(best, first=first[a], via='sparql', ncand=len(cands.get(a, {}))) if best else {'first': first[a], 'ncand': len(cands.get(a, {})), 'cands': [[r['qid'], r['score'], r['desc']] for r in cands.get(a, {}).values()]}
        json.dump(cache, open('wd_authors.json', 'w'), ensure_ascii=False, indent=0)
        print(f'sparql {i+len(names)}/{len(todo)} matched so far {sum(1 for a in todo[:i+B] if cache[a].get("qid"))}', file=sys.stderr)
        time.sleep(1)

    # Pass 2: search API for the rest (fuzzy match), slowly
    rest = [a for a in todo if not cache[a].get('qid')]
    print(len(rest), 'to try via search', file=sys.stderr)
    def api(params):
        params.update(format='json'); return fetch(API + '?' + urllib.parse.urlencode(params))
    def ids(claims, prop): return [c['mainsnak']['datavalue']['value']['id'] for c in claims.get(prop, []) if c.get('rank') != 'deprecated' and 'datavalue' in c.get('mainsnak', {}) and isinstance(c['mainsnak']['datavalue']['value'], dict) and 'id' in c['mainsnak']['datavalue']['value']]
    def year(claims, prop):
        for c in claims.get(prop, []):
            v = c.get('mainsnak', {}).get('datavalue', {}).get('value', {})
            if isinstance(v, dict) and v.get('time'): return yr(v['time'].lstrip('+'))
    for n, a in enumerate(rest):
        res = api({'action': 'wbsearchentities', 'search': clean(a), 'language': 'en', 'type': 'item', 'limit': 6}); time.sleep(1)
        cands = [c['id'] for c in res.get('search', [])]
        if not cands: continue
        ents = api({'action': 'wbgetentities', 'ids': '|'.join(cands), 'props': 'claims|descriptions|labels', 'languages': 'en'}).get('entities', {}); time.sleep(1)
        best = None; seen = []
        for q in cands:
            e = ents.get(q, {}); cl = e.get('claims', {})
            if 'Q5' not in ids(cl, 'P31'): continue
            rec = {'qid': q, 'label': e.get('labels', {}).get('en', {}).get('value'), 'desc': e.get('descriptions', {}).get('en', {}).get('value', ''),
                   'P106': ids(cl, 'P106'), 'P27': ids(cl, 'P27'), 'P172': ids(cl, 'P172'), 'P19': ids(cl, 'P19'), 'born': year(cl, 'P569'), 'died': year(cl, 'P570')}
            rec['score'] = score(rec, first[a]); seen.append([q, rec['score'], rec['desc']])
            if rec['score'] >= 2 and (best is None or rec['score'] > best['score']): best = rec
        cache[a] = dict(best, first=first[a], via='search') if best else {'first': first[a], 'ncand': len(seen), 'cands': seen}
        if n % 10 == 0:
            json.dump(cache, open('wd_authors.json', 'w'), ensure_ascii=False, indent=0); print('search', n, a, (best or {}).get('desc', '-'), file=sys.stderr)
    json.dump(cache, open('wd_authors.json', 'w'), ensure_ascii=False, indent=0)

    # Labels for countries, ethnic groups, birthplaces (-> country)
    need = set()
    for rec in cache.values():
        for k in ('P27', 'P172', 'birthC', 'P19'): need.update(rec.get(k, []))
    lab = json.load(open('wd_labels.json')) if os.path.exists('wd_labels.json') else {}
    miss = sorted(q for q in need if q not in lab)
    for i in range(0, len(miss), 200):
        vals = ' '.join('wd:' + q for q in miss[i:i+200])
        for r in sparql(f'SELECT ?item ?itemLabel ?itemDescription ?country WHERE {{ VALUES ?item {{ {vals} }} OPTIONAL {{ ?item wdt:P17 ?country }} SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }} }}'):
            q = qid(r['item']['value'])
            lab[q] = {'label': r.get('itemLabel', {}).get('value', q), 'desc': r.get('itemDescription', {}).get('value', ''), 'P17': [qid(r['country']['value'])] if 'country' in r else []}
        time.sleep(1)
    miss2 = sorted({c for e in lab.values() for c in e['P17'] if c not in lab})
    if miss2:
        vals = ' '.join('wd:' + q for q in miss2)
        for r in sparql(f'SELECT ?item ?itemLabel WHERE {{ VALUES ?item {{ {vals} }} SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }} }}'):
            lab[qid(r['item']['value'])] = {'label': r['itemLabel']['value'], 'desc': '', 'P17': []}
    json.dump(lab, open('wd_labels.json', 'w'), ensure_ascii=False, indent=0)

    auto = {}
    L = lambda q: lab.get(q, {}).get('label', q)
    # Nationality adjectives in a Wikidata description, used only when no citizenship is recorded
    ADJ = {'American': 'United States', 'British': 'United Kingdom', 'English': 'United Kingdom', 'Scottish': 'United Kingdom', 'Welsh': 'United Kingdom',
           'Irish': 'Ireland', 'Canadian': 'Canada', 'Australian': 'Australia', 'Indian': 'India', 'French': 'France', 'German': 'Germany',
           'Italian': 'Italy', 'Israeli': 'Israel', 'Japanese': 'Japan', 'Singaporean': 'Singapore', 'Romanian': 'Romania', 'Chinese': 'China',
           'Afghan': 'Afghanistan', 'Mexican': 'Mexico', 'Nigerian': 'Nigeria', 'Pakistani': 'Pakistan', 'Dutch': 'Netherlands', 'Danish': 'Denmark',
           'Swedish': 'Sweden', 'Norwegian': 'Norway', 'Russian': 'Russia', 'Polish': 'Poland', 'Hungarian': 'Hungary', 'Austrian': 'Austria'}
    for a, rec in cache.items():
        bad = rec.get('qid') and rec['score'] < 6 and ((rec.get('died') and rec['died'] < rec['first'] - 25) or (rec.get('born') and rec['born'] < rec['first'] - 100))
        if not rec.get('qid') or bad:  # no match, or a namesake who died long before the story ran
            auto[a] = {'countries': [], 'ethnic': [], 'match': None, 'first': rec['first'], 'cands': rec.get('cands', []), 'rejected': rec.get('qid')}; continue
        bc = rec.get('birthC') or [c for q in rec.get('P19', []) for c in lab.get(q, {}).get('P17', [])]
        countries = [L(q) for q in rec['P27']]; src = 'citizenship'
        if not countries:
            words = re.findall(r'[A-Z][a-z]+', rec['desc'].split('(')[0])
            countries = list(dict.fromkeys(ADJ[w] for w in words if w in ADJ)); src = 'description' if countries else None
        auto[a] = {'countries': countries, 'source': src, 'birth_country': [L(q) for q in bc[:1]], 'ethnic': [L(q) for q in rec['P172']],
                   'match': rec['qid'], 'desc': rec['desc'], 'score': rec['score'], 'first': rec['first'], 'born': rec.get('born')}
    json.dump(auto, open('nationality_auto.json', 'w'), ensure_ascii=False, indent=1)
    c = collections.Counter(bool(v['match']) for v in auto.values())
    print('matched', c[True], 'unmatched', c[False], file=sys.stderr)

if __name__ == '__main__': main()
