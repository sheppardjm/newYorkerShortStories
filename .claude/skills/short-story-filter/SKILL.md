---
name: short-story-filter
description: Review the New Yorker fiction list and exclude flash fiction and humor pieces, keeping only conventional short stories. Use when the user asks to re-run, tighten or audit the story/not-story filter, change the flash-fiction word cutoff, review newly crawled stories, or check whether a specific piece is a short story, flash fiction or a humor piece.
---

# Short-story filter

Limits the list in `public/data.json` to conventional short stories. It removes two kinds of piece that The New Yorker's archive files under "Fiction": **flash fiction** (excluded by word count) and **humor pieces** (excluded by reviewing each piece's opening). There is no official definition of a short story, so the rules below use the most conventional published standards and say so.

## The standard and where it comes from

Researched October 2026; sources were checked against each venue's own guidelines page.

- **No major magazine sets a minimum length for a short story.** The New Yorker states no fiction length limits (newyorker.com/about/contact). McSweeney's Quarterly says "Length: Is up to you." The Ploughshares Emerging Writer's Contest gives no minimum. SFWA (Nebula) and the Hugos set only a ceiling: a short story is under 7,500 words.
- **Flash fiction has a widely shared ceiling of about 1,000 words.** SmokeLong Quarterly publishes "flash narratives up to 1000 words." Wigleaf features "stories under 1000 words." Best Small Fictions looks for "pieces under 1000 words." Writing guides such as Reedsy stretch flash to 1,500, but that convention has only blog-level support.
- **Stricter option:** One Story accepts only stories of 3,000–8,000 words. That is one magazine's taste, not a field definition.
- **Humor is a separate department, not a length.** The New Yorker files humor under Shouts & Murmurs ("humorous fiction") and Daily Shouts, separately from Fiction. McSweeney's Internet Tendency caps humor at 1,200 words and favors lists, open letters and monologues. Humor runs from under 600 words to well over 1,500, so it has to be identified by its form, not its length. Before 1993 the magazine filed humor "casuals" under Fiction, which is why every piece needs reviewing.

The owner chose **1,000 words** as the flash cutoff: a piece of 1,000 words or fewer is flash and is excluded, unless its author is a known fiction writer (rule 3). The cutoff and the owner's exceptions live in `pipeline/filter_config.json`. Change the cutoff only when the owner asks, and say how many stories the change adds or removes.

## Rules

1. **Flash fiction:** `words <= flash_max_words` is excluded automatically by `pipeline/build.py`. No review is needed.
2. **Owner's exceptions:** paths in `keep` bypass every filter. Never remove one unless the owner asks.
3. **Known fiction writers are never removed by length or review.** The owner's rule: a piece whose author is labeled F (known mainly for novels or short stories, in `judgments/auth*.out.tsv` and `auth_auto.json`) skips both the flash cutoff and the story/not-story verdicts, even when the piece is very short or reads as humor. `protect_fiction_writers` in `filter_config.json` controls this. Poem and cartoon detection, the 1940 start and the online Flash Fiction series still apply to everyone. Don't queue F-author pieces for review, since a verdict can't remove them.
4. **Humor and other non-stories:** every piece from `flash_max_words` to `review_ceiling_words`, plus every piece by an author labeled H (humorist, journalist, critic, poet) at any length, gets one verdict:
   - **S (short story):** narrative fiction in which characters do something and a situation unfolds through scenes or events. Comic stories count as S when they tell a story with characters. A monologue or letter counts as S if it dramatizes a character in a situation with something at stake. Memoir-style first-person narration counts as S only when it reads as fiction rather than essay.
   - **N (not a short story):** any of the following.
     - Parody or pastiche of a borrowed format: news items, memos, ads, reports, questionnaires, calendars, catalogues, transcripts, lists, guides or how-tos.
     - Satire or opinion in essay form, or humorous commentary that riffs on a topic without a plot.
     - A playlet or script.
     - Verse.
     - Reportage, a profile or a travel sketch.
     - An editorial-"we" observation piece.
     - A personal essay or memoir that reads as nonfiction (common for Emily Hahn, H. L. Mencken, Roger Angell, Joseph Wechsberg).
   - **When unsure:** S only if the opening clearly puts a character in a scene. Otherwise N. An author's H label is supporting evidence, never the deciding factor. Thurber's "The Secret Life of Walter Mitty" is a story.

## Procedure

1. **Queue:** run `python3 pipeline/review_queue.py`. It writes `pipeline/data/review/queue-NN.tsv` batches of pieces that have no verdict yet, with columns path, title, author, year, words and opening (about 600 characters). It fetches any opening it doesn't have cached from newyorker.com. If it reports 0 queued, skip to step 4.
2. **Review:** for each batch, spawn one general-purpose subagent, running all batches in parallel in a single message. Pass it the batch path, the Rules section above verbatim, and these instructions:
   - Judge every line yourself; a script may only pair your labels with paths.
   - Write `pipeline/data/judgments/review-NN.out.tsv`, one `path<TAB>S` or `path<TAB>N` line per input line, with paths copied exactly.
   - Verify that every input path appears exactly once.
3. **Check:** confirm each `.out.tsv` has the same paths as its queue file, then spot-check about 10 random verdicts per batch against their openings. Fix clear misjudgments by editing the line. Note any you're unsure of for the owner, without guessing.
4. **Rebuild:** run `npm run data`, which regenerates `public/data.json` and the CSV, then `npm run build`.
5. **Report:** tell the owner how many pieces were reviewed and how many were dropped as N, with a few representative titles of each kind. Give the new story count. List any borderline calls. Commit only if the owner asks.

## Files

- `pipeline/filter_config.json`: the flash cutoff, the review ceiling, whether to queue H-author pieces, batch size, and the `keep` list.
- `pipeline/review_queue.py`: builds the review batches.
- `pipeline/data/judgments/*.out.tsv`: verdicts. `a*`, `b*` and `review-*` are story verdicts (S/N); `auth*` are author labels (F/H/U). `build.py` reads all of them, and a later file overrides an earlier one for the same path.
- `pipeline/build.py`: applies the 1940 start, poem and cartoon detection, the verdicts and the flash cutoff.
