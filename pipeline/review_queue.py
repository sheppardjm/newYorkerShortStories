"""Write review batches for the short-story filter skill.

Queues every listed piece that has no story/not-story verdict yet and is either
(a) between flash_max_words and review_ceiling_words long, or
(b) by an author labeled H (humorist, journalist, poet) in judgments/auth*.out.tsv.
Pieces at or under flash_max_words are excluded by build.py and never queued.

Usage: python3 pipeline/review_queue.py   ->  pipeline/data/review/queue-NN.tsv
"""
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
import json, glob, re, html, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

cfg = json.load(open('../filter_config.json'))
rows = json.load(open('../../public/data.json'))
cls = json.load(open('cls.json'))

judged = set()
for fn in glob.glob('judgments/[a-z]*.out.tsv'):
    if os.path.basename(fn).startswith('auth'): continue
    for line in open(fn):
        judged.add(line.split('\t')[0])
authlab = {}
for fn in glob.glob('judgments/auth*.out.tsv'):
    for line in open(fn):
        p = line.rstrip('\n').split('\t')
        if len(p) == 2: authlab[p[0]] = p[1].strip()
def main_author(a): return re.split(r',\s*|\s+and\s+', a or '')[0].strip()
authlab_all = {n: 'F' for n in json.load(open('auth_auto.json'))}
authlab_all.update(authlab)

queue = []
for t, a, y, d, w, path, dek, f in rows:
    if path in judged or path in cfg['keep'] or w is None: continue
    if cfg.get('protect_fiction_writers', True) and authlab_all.get(main_author(a)) == 'F': continue
    in_band = cfg['flash_max_words'] < w <= cfg['review_ceiling_words']
    humorist = cfg['review_humorist_authors'] and authlab.get(main_author(a)) == 'H'
    if in_band or humorist: queue.append((path, t, a, y, w))

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
def opening(path):
    if path in cls and cls[path] and cls[path].get('head'): return path, cls[path]['head']
    for i in range(4):
        try:
            s = urllib.request.urlopen(urllib.request.Request("https://www.newyorker.com" + path, headers={'User-Agent': UA}), timeout=30).read().decode('utf-8', 'replace')
            break
        except Exception:
            time.sleep(3 * (i + 1)); s = ''
    j = s.find('class="body__inner-container'); body = s[j:j + 300000] if j >= 0 else ''
    txt = ' '.join(html.unescape(re.sub('<[^>]+>', ' ', x)) for x in re.findall(r'<p[^>]*>(.*?)</p>', body, re.S))
    txt = re.sub(r'\s+', ' ', txt).replace('View this story as it originally appeared »', '').strip()
    return path, txt[:600]

with ThreadPoolExecutor(8) as ex:
    heads = dict(ex.map(opening, [q[0] for q in queue]))

for fn in glob.glob('review/queue-*.tsv'): os.remove(fn)
n = cfg['batch_size']
for i in range(0, len(queue), n):
    with open(f'review/queue-{i // n:02d}.tsv', 'w') as f:
        for path, t, a, y, w in queue[i:i + n]:
            h = heads.get(path, '').replace('\t', ' ').replace('\n', ' ')[:600]
            f.write(f"{path}\t{t}\t{a}\t{y}\t{w}\t{h}\n")
print(f"queued {len(queue)} pieces in {-(-len(queue) // n)} batch(es) under pipeline/data/review/")
