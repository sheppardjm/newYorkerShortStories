import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
import json,collections,re
d=json.load(open('../../public/data.json')); wa=json.load(open('wa.json'))
def main(a): return re.split(r',\s*|\s+and\s+',a or '')[0].strip()
norm=lambda s: re.sub(r'[^a-z]','',s.lower())
wa_auth={norm(x['author']) for x in wa}
by=collections.defaultdict(list)
for r in d: by[main(r[1])].append(r)
auto={}
for a,rs in by.items():
    if any(r[2]>=1993 for r in rs): auto[a]='F93'
    elif norm(a) in wa_auth: auto[a]='FWA'
json.dump(auto,open('auth_auto.json','w'))
todo=sorted([a for a in by if a not in auto and a],key=lambda a:-len(by[a]))
size=-(-len(todo)//2)
for i in range(2):
    with open(f'judgments/auth{i}.tsv','w') as f:
        for a in todo[i*size:(i+1)*size]:
            rs=by[a]; ys=[r[2] for r in rs]
            titles='; '.join(r[0] for r in sorted(rs,key=lambda r:-(r[4] or 0))[:4])
            f.write(f"{a}\t{len(rs)}\t{min(ys)}-{max(ys)}\t{titles}\n")
print(len(by),len(auto),len(todo))
