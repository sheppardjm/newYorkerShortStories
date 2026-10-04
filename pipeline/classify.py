import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
import json, re, os, html, urllib.request, time
from concurrent.futures import ThreadPoolExecutor
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
a=json.load(open('art.json'))
cls=json.load(open('cls.json')) if os.path.exists('cls.json') else {}
def get(u):
    for i in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=30).read().decode('utf-8','replace')
        except Exception as e:
            if getattr(e,'code',0) in (404,410): return ''
            time.sleep(3*(i+1))
    return None
def one(p):
    s=get("https://www.newyorker.com"+p)
    if s is None: return p,None
    m=re.search(r'"functionalTags":\[([^\]]*)\]',s)
    ft=re.findall(r'"([^"]+)"',m.group(1)) if m else []
    tg=re.search(r'"tags":"([^"]*)"',s)
    i=s.find('class="body__inner-container'); body=s[i:i+300000] if i>=0 else ''
    if 'ContentFooter' in body: body=body[:body.find('ContentFooter')]
    paras=re.findall(r'<p[^>]*>(.*?)</p>',body,re.S)
    txt=' '.join(html.unescape(re.sub('<[^>]+>',' ',x)) for x in paras)
    txt=re.sub(r'\s+',' ',txt).replace('View this story as it originally appeared »','').strip()
    return p,dict(ft=ft,tags=tg.group(1) if tg else '',br=body.count('<br'),bw=len(txt.split()),head=txt[:500])
todo=[p for p,v in a.items() if v and (v.get('wc') or v.get('wc2')) and int(v.get('wc') or v.get('wc2'))<int(os.environ.get('MAXW','1500')) and cls.get(p) is None]
print('todo',len(todo),flush=True)
with ThreadPoolExecutor(8) as ex:
    for p,r in ex.map(one,todo): cls[p]=r
json.dump(cls,open('cls.json','w'))
print('done',len(cls))
