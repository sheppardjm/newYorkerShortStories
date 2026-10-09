# New Yorker Fiction by Length

Every New Yorker short story since 1940, ranked by word count, with a link to each story on newyorker.com. Built for reading one story a day: filter by length, decade, or "known fiction writers," pick a random unread one, and check stories off as you read them (saved in your browser).

## Site

Static [Astro](https://astro.build) site, deployed on Netlify.

```sh
npm install
npm run dev      # local dev server
npm run build    # outputs dist/
```

The page (`src/pages/index.astro`) loads `public/data.json` in the browser. `public/new_yorker_stories_by_word_count.csv` is the same list as a spreadsheet.

## Data pipeline (`pipeline/`)

Python 3, standard library only. Cached crawl results live in `pipeline/data/`, so `npm run data` rebuilds `public/data.json` and the CSV without re-crawling.

| Script | What it does |
| --- | --- |
| `urls.py` | Collects story URLs from the newyorker.com fiction listing (capped at 10,000 results, back to 1939) and from 1925–40 issue pages. |
| `articles.py` | Fetches each story page's metadata: title, author, date, word count. |
| `classify.py` | For short pieces, fetches body details used to spot poems, cartoon features and summary-only archive pages. |
| `rules.py` | Heuristics for those categories. |
| `authors.py` | Prepares the author list for labeling. |
| `build.py` | Applies every filter and writes `public/data.json` and the CSV. |
| `scrape.py` | Writing Atlas's New Yorker list, used as a cross-check. |

`pipeline/data/story_club.json` lists the New Yorker stories George Saunders discusses on his Substack, Story Club, with the post where each comes up. Only those marked `taught` reach the site, where they drive the "Discussed in Story Club" filter; the `recommended` and `own` entries are passing mentions kept for reference.

`pipeline/data/judgments/` holds review verdicts. `a*/b*.out.tsv` mark each piece under 2,500 words as story (S) or not (N), judged from its opening lines. `auth*.out.tsv` label authors as fiction writers (F), humorists/journalists/poets (H) or unknown (U).

### What's excluded

- Anything before 1940. The archive labels nearly every early humor piece and column as fiction.
- Flash fiction: pieces of 1,000 words or fewer, the ceiling SmokeLong Quarterly, Wigleaf and Best Small Fictions use. Known fiction writers are exempt from this cutoff and from the humor review, and so is "A Fresno Fable." The cutoff lives in `pipeline/filter_config.json`, and the `short-story-filter` skill (`.claude/skills/`) describes the full review.
- The online Flash Fiction series.
- Poems, cartoon and art features, and humor sketches, parodies and essays filed under fiction.

Word counts come from newyorker.com's page metadata and run a few percent high. Some archive stories have only a summary online; they're listed under "Length unknown."
