import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
import re, json, time, urllib.request, html
out=[]; page=1
while True:
    url=f"https://writingatlas.com/api/stories/get_stories/?page={page}&id=154&category=publication&sort=word_count"
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    s=urllib.request.urlopen(req).read().decode()
    blocks=s.split('class="list-infobox"')[1:]
    for b in blocks:
        g=lambda p: (m.group(1).strip() if (m:=re.search(p,b,re.S)) else None)
        out.append(dict(
          title=html.unescape(g(r'class="story-title link-text">(.*?)</a>') or ''),
          wa=g(r'href="(/story/[^"]+)"'),
          author=html.unescape(g(r'href="/author/[^"]+" class="story-info-text-metadata">(.*?)</a>') or ''),
          year=g(r'href="/year/\d+/" class="story-info-text-metadata">\s*(\d+)'),
          words=g(r'color: grey;">([\d,]+)</a>\s*words'),
          link=g(r'href="(https://www\.newyorker\.com[^"]+)"'),
          logline=html.unescape(g(r'class="story-logline">(.*?)</p>') or ''),
        ))
    if f'page={page+1}&' not in s: break
    page+=1; time.sleep(0.3)
json.dump(out,open('wa.json','w'),indent=1)
print(page,len(out))
