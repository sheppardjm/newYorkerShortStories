# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

The owner, who reads one New Yorker short story every day using a New Yorker subscription, plus friends and strangers the site is shared with. Their recurring job: on any given day, find a story that fits the time they have, often the shortest worthwhile one, and open it on newyorker.com. Visitors arriving cold need the page to explain itself without the owner present.

## Product Purpose

An independent index of The New Yorker's short fiction, ranked by word count, so a reader can always find a story that fits the day. Success means a visitor can go from "I have ten minutes" to an open story in a few seconds, and can trust that what's listed is a real short story rather than a humor piece, poem or cartoon that the archive filed as fiction.

## Positioning

The magazine's own archive files many humor pieces, poems, cartoon features and summary-only pages under "Fiction" and offers no sort by length. This list is crawled from newyorker.com's own page data, filtered for real stories (pieces under 2,500 words reviewed from their openings, authors labeled as known fiction writers or not), and ranked by word count. Writing Atlas covers about 584 New Yorker stories, with some wrong counts; this covers every story since 1940.

## Operating Context

- Stories are read on newyorker.com; every entry links out there, and a subscription is needed for full text. The site hosts no story text.
- Typical use: open the site, set a length or other filter, use "Pick one for today" or scan the list, click through.
- Used on phone and desktop.
- The data is rebuilt offline from `pipeline/` (`npm run data`) and committed. Netlify deploys from GitHub `main`.

## Capabilities and Constraints

- Static Astro site on Netlify. No backend, no accounts.
- 6,820 stories from 1940 to now, plus 111 marked "Length unknown" (the archive has only a summary online).
- Filters: length bands, decade, search by title or author, sort order, "Known fiction writers only", "1993 and later". "Pick one for today" gives a random story within the current filters. Each row has a "Hide" link (per browser) for misfiled pieces, and the full list downloads as a CSV.
- Excluded by the owner's choice: anything before 1940, flash fiction of 1,000 words or fewer (the ceiling SmokeLong Quarterly, Wigleaf and Best Small Fictions use; except Saroyan's "A Fresno Fable"), the online Flash Fiction series, poems, cartoon features, and humor/parody/essay pieces. Known fiction writers are exempt from the flash cutoff and the humor review, by the owner's rule.
- Read checkmarks have been removed at the owner's request. There's no per-story read tracking or read-based filtering. Cross-device sync is not wanted.
- Word counts come from newyorker.com page metadata and run a few percent high. Story-versus-humor labels are judgment calls; some misfiles remain.
- Terminology: "word count", "reading time" (240 words per minute), "known fiction writer", "length unknown".

## Brand Commitments

- Independent project. It must not present itself as The New Yorker or imply affiliation: no New Yorker logo, Eustace Tilley, Irvin typeface or the magazine's custom Caslon. The owner has those fonts locally, but they are proprietary and must not be served from the site.
- Visual direction, set by the owner: New York modernist (Helvetica or geometric sans, in the spirit of Paul Rand and Milton Glaser) rather than an imitation of the magazine.
- Current name: "New Yorker Fiction by Length" (page heading "New Yorker Fiction, Shortest First").

## Evidence on Hand

- `public/data.json` and `public/new_yorker_stories_by_word_count.csv`: the list.
- `pipeline/data/`: cached crawl of newyorker.com, Writing Atlas cross-check data, and story and author judgments.
- No testimonials, users or usage figures exist; none should be invented.

## Product Principles

1. Get to a story fast: the list and its filters are the product, and everything else stays out of the way.
2. Trust the list: when a filter or label is a judgment call, say so plainly on the page.
3. Send readers to the source: link every story to newyorker.com, and never copy story text.
4. Stay independent: honor the magazine without borrowing its identity.
