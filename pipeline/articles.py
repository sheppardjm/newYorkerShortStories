import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
import re, json, os, html, urllib.request, time, sys
from concurrent.futures import ThreadPoolExecutor
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
def get(u):
    for i in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=30).read().decode('utf-8','replace')
        except Exception as e:
            if getattr(e,'code',0) in (404,410): return ''
            time.sleep(3*(i+1))
    return None
def f(p,s):
    m=re.search(p,s,re.S); return m.group(1) if m else None
def parse(path):
    s=get("https://www.newyorker.com"+path)
    if s is None: return path,None
    if not s: return path,{'missing':True}
    ld={}
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
        try:
            j=json.loads(b)
            if isinstance(j,dict) and j.get('@type') in ('NewsArticle','Article'): ld=j
        except: pass
    au=ld.get('author') or []
    if isinstance(au,dict): au=[au]
    return path,dict(
        title=html.unescape(ld.get('headline') or f(r'<title>(.*?)</title>',s) or ''),
        author=', '.join(a.get('name','') for a in au if isinstance(a,dict)),
        dek=html.unescape(ld.get('description') or ''),
        wc=f(r'"content4d":\{"wordcount":(\d+)',s),
        wc2=f(r'"wordCount":"(\d+)"',s),
        subsection=f(r'"subsection":"([^"]*)"',s),
        rubric=f(r'"articleSection":"([^"]*)"',s),
        date=ld.get('datePublished',''),
    )
urls=json.load(open('urls.json'))
out=json.load(open('art.json')) if os.path.exists('art.json') else {}
todo=[u for u in urls if u not in out or out[u] is None]
print('todo',len(todo),flush=True)
with ThreadPoolExecutor(8) as ex:
    for i,(p,r) in enumerate(ex.map(parse,todo)):
        out[p]=r
        if i%250==0:
            json.dump(out,open('art.json','w')); print(i,flush=True)
json.dump(out,open('art.json','w'))
print('done',sum(1 for v in out.values() if v is None),'failed')
