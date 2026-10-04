import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
import json, re, csv
import os
a=json.load(open('art.json')); u=json.load(open('urls.json'))
from rules import classify
cls=json.load(open('cls.json')) if os.path.exists('cls.json') else {}
dropped={}
KEEP={'/magazine/1976/01/19/a-fresno-fable','/magazine/1981/06/01/the-gift-of-the-prodigal'}  # user exceptions
import glob
verdict={}
for fn in glob.glob('judgments/*.out.tsv'):
    for line in open(fn):
        parts=line.rstrip('\n').split('\t')
        if len(parts)==2: verdict[parts[0]]=parts[1].strip()
flash=json.load(open('flash.json'))
for p in flash: a.pop(p, None)  # user excludes the New Yorker's Flash Fiction series
rows=[]; seen=set()
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
    if path not in KEEP and verdict.get(path)=='N': dropped['not_story']=dropped.get('not_story',0)+1; continue
    w=None if k=='unknown' else int(w)
    if path not in KEEP and w is not None and w<500: dropped['under500']=dropped.get('under500',0)+1; continue
    if src=='flash': t+=' (Flash Fiction series)'
    rows.append([t,v['author'],int(dm.group(1)),f"{dm.group(1)}-{dm.group(2)}-{dm.group(3)}",w,path,d])
authlab={a:'F' for a in json.load(open('auth_auto.json'))} if os.path.exists('auth_auto.json') else {}
for fn in glob.glob('judgments/auth*.out.tsv'):
    for line in open(fn):
        p=line.rstrip('\n').split('\t')
        if len(p)==2: authlab[p[0]]=p[1].strip()
def mainauth(a): return re.split(r',\s*|\s+and\s+',a or '')[0].strip()
for r in rows: r.append(authlab.get(mainauth(r[1]),'U'))
rows.sort(key=lambda r:(r[4] is None, r[4] or 0, r[3]))
json.dump(rows,open('../../public/data.json','w'),ensure_ascii=False,separators=(',',':'))
with open('../../public/new_yorker_stories_by_word_count.csv','w',newline='') as f:
    wr=csv.writer(f); wr.writerow(['rank','words','title','author','known_fiction_writer','issue_date','url','summary'])
    for i,r in enumerate(rows,1): wr.writerow([i if r[4] else '',r[4] or 'unknown (archive scan only)',r[0],r[1],{'F':'yes','H':'no'}.get(r[7],'unknown'),r[3],'https://www.newyorker.com'+r[5],r[6]])
print(dropped, len(rows), 'unknown', sum(1 for r in rows if r[4] is None))
