import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
import re, json, urllib.request, datetime
from concurrent.futures import ThreadPoolExecutor
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
def get(u,tries=4):
    for i in range(tries):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=30).read().decode('utf-8','replace')
        except Exception as e:
            if getattr(e,'code',0)==404: return ''
            import time; time.sleep(2*(i+1))
    return ''
pat=re.compile(r'href="(/magazine/\d{4}/\d{2}/\d{2}/[^"?#]+)"')
def listing(p):
    s=get(f"https://www.newyorker.com/magazine/fiction?page={p}")
    # only items inside the paginated river: collect unique hrefs that have fiction rubric context; take all and filter later via article metadata
    return p, sorted(set(pat.findall(s)))
urls={}
with ThreadPoolExecutor(8) as ex:
    for p,us in ex.map(listing, range(1,1001)):
        for u in us: urls.setdefault(u,'listing')
print('listing',len(urls))
def issue(d):
    s=get(f"https://www.newyorker.com/magazine/{d:%Y/%m/%d}")
    out=[]
    for chunk in s.split('summary-item__content')[1:]:
        r=re.search(r'rubric"><span>([^<]*)</span>',chunk); h=pat.search(chunk)
        if r and h and r.group(1).strip().lower()=='fiction': out.append(h.group(1))
    return d,out,len(s)
d=datetime.date(1925,2,21); days=[]
while d<=datetime.date(1940,6,30): days.append(d); d+=datetime.timedelta(7)
n=0
with ThreadPoolExecutor(8) as ex:
    for d,us,L in ex.map(issue,days):
        for u in us:
            if u not in urls: urls[u]='issue'; n+=1
print('issue-added',n)
json.dump(urls,open('urls.json','w'),indent=0)
