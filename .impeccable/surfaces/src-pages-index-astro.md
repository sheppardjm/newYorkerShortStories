---
version: 1
slug: "src-pages-index-astro"
primary_target: "src/pages/index.astro"
related_targets: []
---

# Surface: index (src/pages/index.astro)

Scope: the single page of the site, the ranked story list and its filters. Mode: Operate. Visitors find a story that fits the time they have and click through to newyorker.com.

Audience and job: the owner, a one-story-a-day reader, plus anyone they share it with. Task: set a length or other filter, scan or pick at random, open the story. Constraints: from PRODUCT.md (independent project, none of the magazine's identity; the read checkmarks have been removed).

Chosen direction: Subway Signage (the 1970 Vignelli/Noorda signage manual and the 1972 subway diagram), user-picked over the rolled Glaser direction.

## Direction contract

THESIS: Story lengths are subway lines. Each story is a stop led by its route bullet, so how long a story takes reads like knowing which train to catch. This refuses the category default of soft cards on a grey list.

OWN-WORLD: Signage black #111 bands with white Helvetica Medium and a thin white rule near the top edge. White ground with 1px rules. Route bullets in MTA line colors: red under 5 min, orange 5–10, yellow 10–20 (black numeral), green 20–30, blue 30–45, purple 45+, shuttle grey for unknown length. No gradients, no shadows, no radius except perfect circles. Raises: guide words name the word span in view (from the lexicon); one grotesque at every size with 1px rules (from the design annual); scale contrast does the hierarchy (from the specimen); dense rows with no cards (from the event catalog). The "Today" panel is the only black panel inside the list (from orienteering's reserved color).

STORY: The visitor sees that the color means length, filters by tapping a bullet, picks a story and leaves for newyorker.com.

FIRST VIEWPORT: A full-width black band holding the title in white Helvetica Medium at about 44–56px, a one-line standfirst and the independence note. Below it a sticky white control strip: the six band bullets plus the grey one as filter chips with counts, then search, decade, sort and the "Known fiction writers only" and "1993 and later" checkboxes, then a black "Pick one for today" button with a signage arrow. The list starts within the first viewport: bullet (minutes) | title, author, date | words | Hide.

ADAPTATIONS (recorded after finish review): The title is set in Bold, not Medium, because TeX Gyre Heros, the only freely licensed Helvetica clone that can be self-hosted, ships no Medium weight (PRODUCT.md brand commitments forbid serving proprietary fonts); size and tracking are moderated to read as signage. Search, decade, sort and the checkboxes scroll away above the sticky strip, so the strip stays short on phones; the sticky strip holds the line bullets, guide words, count and "Pick one for today", so picking stays reachable mid-list. The site is light-only, as the contract specifies a white ground; a dark theme would need the user's approval.

FORM: Subway Signage, my #1 grounded candidate (taken as IMPECCABLE’S PICK; the roll assigned #3), seed key 11cd70e5. Signature interaction: tapping a bullet filters to that line, and "Pick one for today" moves the chosen story into a black "Today" signage panel at the top of the list.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
