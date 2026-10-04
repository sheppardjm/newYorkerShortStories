import re
ARTISTS = {"roz chast","saul steinberg","james stevenson","bruce mccall","jacques de loustal","loustal","william steig",
 "jack ziegler","charles saxon","edward koren","barry blitt","edwin fotheringham","nick drnaso","richard merkin","chris ware",
 "art spiegelman","daniel clowes","ben katchor","edward sorel","george booth","lee lorenz","danny shanahan","jules feiffer",
 "charles addams","peter arno","ronald searle","ed fisher","william hamilton","r. o. blechman","j. b. handelsman","frank modell",
 "mischa richter","warren miller","robert weber","sam gross","michael crawford","jack ziegler","bob mankoff","arnie levin",
 "dana fradon","whitney darrow, jr.","joseph mirachi","donald reilly","al ross","barney tobey","mick stevens","victoria roberts",
 "w. b. park","liza donnelly","bruce eric kaplan","david sipress","mort gerberg","edward frascino","charles barsotti","eldon dedini",
 "henry martin","everett opie","stan hunt","james mulligan","jeff danziger","seth","adrian tomine","joost swarte","maira kalman",
 "william frawley","ward sutton","tom bachtell","jason polan","istvan banyai","glen baxter","edward gorey","tomi ungerer"}
VIS_TAGS = re.compile(r'\b(comic books|comics|comic strips|cartoons|cartoonists|graphic novels|drawings|illustrations|paintings|sketchbook)\b')
VIS_HEAD = re.compile(r'drawings|cartoon|illustrat|spread|cover art|panels|no captions|in color|full-color|full page', re.I)
ABSTRACT = re.compile(r'^(The New Yorker\s*,\s*\w+\.? \d{1,2}, \d{4}\s*P\.\s*\d+|Short story|Story about|Story set|Fiction about|Excerpt from|There is no abstract|Satire|Humor|Parody|A short story)', re.I)
def classify(v, c):
    """returns 'story' | 'unknown' | 'poem' | 'visual'"""
    au = (v.get('author') or '').lower()
    t = (v.get('title') or '').lower()
    if any(x.strip() in ARTISTS for x in au.split(',')) or 'cartoon' in t or 'sketchbook' in t: return 'visual'
    if not c: return 'story'
    if 'paywall-exclude' in c['ft']: return 'unknown'
    if ABSTRACT.match(c['head']) or c['bw'] < 100:
        return 'visual' if VIS_HEAD.search(c['head']) else 'unknown'
    if VIS_TAGS.search(c['tags']): return 'visual'
    if c['br'] >= 5 and c['bw'] / max(c['br'], 1) < 30: return 'poem'
    return 'story'
