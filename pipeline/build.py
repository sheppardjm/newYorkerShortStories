import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
import json, re, csv
import os
a=json.load(open('art.json')); u=json.load(open('urls.json'))
from rules import classify
cls=json.load(open('cls.json')) if os.path.exists('cls.json') else {}
dropped={}
CFG=json.load(open('../filter_config.json'))
KEEP=set(CFG['keep'])  # owner's exceptions to every filter
FLASH_MAX=CFG['flash_max_words']  # at or under this is flash fiction
import glob
verdict={}
for fn in sorted(glob.glob('judgments/*.out.tsv')):
    for line in open(fn):
        parts=line.rstrip('\n').split('\t')
        if len(parts)==2: verdict[parts[0]]=parts[1].strip()
flash=json.load(open('flash.json'))
for p in flash: a.pop(p, None)  # user excludes the New Yorker's Flash Fiction series
rows=[]; seen=set()
authlab={a:'F' for a in json.load(open('auth_auto.json'))} if os.path.exists('auth_auto.json') else {}
for fn in sorted(glob.glob('judgments/auth*.out.tsv')):
    for line in open(fn):
        p=line.rstrip('\n').split('\t')
        if len(p)==2: authlab[p[0]]=p[1].strip()
def mainauth(a): return re.split(r',\s*|\s+and\s+',a or '')[0].strip()
PROTECT_F=CFG.get('protect_fiction_writers', True)  # known fiction writers bypass the flash and story/not-story filters
for path,v in a.items():
    if not v or v.get('missing'): continue
    src=u.get(path,'listing')
    if src=='listing' and v.get('subsection')!='fiction': continue
    w=v.get('wc') or v.get('wc2')
    if not w: continue
    t=v['title'].replace('\xa0',' ').strip()
    m=re.match(r'^[“"](.+?)[,.]?[”"](?:,| by| an| a |:).*$',t)
    if m: t=m.group(1)
    t=re.sub(r'^Flash Fiction:\s*','',t)
    t=re.sub(r',\s*by .*$','',t)
    t=t.strip('“”"').strip()
    t=re.sub(r'\s*\|\s*The New Yorker$','',t)
    d=v.get('dek','').replace('\xa0',' ')
    if 'was published in the print edition' in d or 'issue of The New Yorker' in d: d=''
    if len(d)>220: d=d[:217].rsplit(' ',1)[0]+'…'
    if src=='issue' and path not in KEEP: dropped['pre1940']=dropped.get('pre1940',0)+1; continue
    dm=re.match(r'/magazine/(\d{4})/(\d{2})/(\d{2})/',path) or re.match(r'(\d{4})-(\d{2})-(\d{2})',v.get('date',''))
    if int(dm.group(1))<1940 and path not in KEEP: dropped['pre1940']=dropped.get('pre1940',0)+1; continue
    key=(t.lower(),v['author'].lower())
    if key in seen: continue
    seen.add(key)
    k=classify(v, cls.get(path))
    if path not in KEEP and k in ('visual','poem'): dropped[k]=dropped.get(k,0)+1; continue
    fic = PROTECT_F and authlab.get(mainauth(v.get('author')),'U')=='F'
    if path not in KEEP and not fic and verdict.get(path)=='N': dropped['not_story']=dropped.get('not_story',0)+1; continue
    w=None if k=='unknown' else int(w)
    if path not in KEEP and not fic and w is not None and w<=FLASH_MAX: dropped['flash']=dropped.get('flash',0)+1; continue
    if src=='flash': t+=' (Flash Fiction series)'
    rows.append([t,v['author'],int(dm.group(1)),f"{dm.group(1)}-{dm.group(2)}-{dm.group(3)}",w,path,d])
for r in rows: r.append(authlab.get(mainauth(r[1]),'U'))
club={k:v for k,v in json.load(open('story_club.json')).items() if not k.startswith('_') and v['kind']=='taught'}  # stories taught on Saunders's Story Club; passing mentions stay in the file but off the site
for r in rows: c=club.get(r[5]); r.append([c['kind'],c['post']] if c else 0)
missing=set(club)-{r[5] for r in rows}
if missing: print('story_club.json paths not in the list:', sorted(missing))
rows.sort(key=lambda r:(r[4] is None, r[4] or 0, r[3]))
json.dump(rows,open('../../public/data.json','w'),ensure_ascii=False,separators=(',',':'))
with open('../../public/new_yorker_stories_by_word_count.csv','w',newline='') as f:
    wr=csv.writer(f); wr.writerow(['rank','words','title','author','known_fiction_writer','issue_date','url','summary','story_club'])
    for i,r in enumerate(rows,1): wr.writerow([i if r[4] else '',r[4] or 'unknown (archive scan only)',r[0],r[1],{'F':'yes','H':'no'}.get(r[7],'unknown'),r[3],'https://www.newyorker.com'+r[5],r[6],r[8][0] if r[8] else ''])
print(dropped, len(rows), 'unknown', sum(1 for r in rows if r[4] is None))
