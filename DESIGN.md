---
name: New Yorker Fiction by Length
description: An independent index of New Yorker short fiction, set as 1970s New York subway signage where story length is the train line.
colors:
  ink: "#111111"
  ground: "#ffffff"
  ink-2: "#4a4a4a"
  rule: "#d6d6d6"
  band-ink-2: "#bdbdbd"
  hover: "#f3f3f3"
  focus: "#0039a6"
  line-1: "#ee352e"
  line-2: "#f96016"
  line-3: "#fccc0a"
  line-4: "#00933c"
  line-5: "#0039a6"
  line-6: "#b933ad"
  line-0: "#808183"
typography:
  display:
    fontFamily: "Heros, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "clamp(32px, 5vw, 56px)"
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: "-0.01em"
  station:
    fontFamily: "Heros, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "clamp(26px, 4vw, 40px)"
    fontWeight: 700
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Heros, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "clamp(22px, 3vw, 32px)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  standfirst:
    fontFamily: "Heros, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "clamp(17px, 2vw, 20px)"
    fontWeight: 400
    lineHeight: 1.35
  title:
    fontFamily: "Heros, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "19px"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Heros, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.45
  meta:
    fontFamily: "Heros, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 400
  label:
    fontFamily: "Heros, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 700
  numeral:
    fontFamily: "Heros, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "18px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.02em"
    fontFeature: "\"tnum\" 1, \"lnum\" 1"
  tag:
    fontFamily: "Heros, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "10px"
    fontWeight: 700
    letterSpacing: "0.06em"
rounded:
  none: "0px"
  circle: "50%"
spacing:
  xs: "6px"
  sm: "8px"
  md: "12px"
  lg: "18px"
  xl: "24px"
  gutter: "clamp(16px, 4vw, 40px)"
  max: "1080px"
components:
  bullet:
    backgroundColor: "{colors.line-1}"
    textColor: "{colors.ground}"
    typography: "{typography.numeral}"
    rounded: "{rounded.circle}"
    size: "44px"
  bullet-yellow:
    backgroundColor: "{colors.line-3}"
    textColor: "{colors.ink}"
  bullet-small:
    rounded: "{rounded.circle}"
    size: "22px"
  bullet-today:
    rounded: "{rounded.circle}"
    size: "64px"
  line-chip:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 12px 0 8px"
    height: "38px"
  line-chip-hover:
    backgroundColor: "{colors.hover}"
  line-chip-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ground}"
  button-pick:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ground}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 12px"
    height: "34px"
  button-pick-hover:
    backgroundColor: "{colors.focus}"
    textColor: "{colors.ground}"
  button-outline:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0 20px"
    height: "42px"
  button-outline-hover:
    backgroundColor: "{colors.hover}"
  button-read:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 14px"
    height: "38px"
  input-field:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0 10px"
    height: "38px"
  today-panel:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ground}"
    rounded: "{rounded.none}"
    padding: "30px 24px 24px"
  tag:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ground}"
    typography: "{typography.tag}"
    rounded: "{rounded.none}"
    padding: "1px 5px 0"
---

# Design System: New Yorker Fiction by Length

## Overview

**Creative North Star: "The Signage Manual"**

The system is the 1970 New York subway signage standard and the 1972 diagram, applied to a reading list. Story length is the train line: every story is a stop led by a colored route bullet carrying its reading time in minutes, and the color tells you which band of time you are riding before you read a word. Black signage bands frame the page top and bottom, each with a thin white rule just inside its top edge; between them sits a white ground of dense rows divided by hairline rules.

It is a light, flat, single-typeface world. One grotesque (TeX Gyre Heros, a license-free Helvetica clone) in two weights does all the work, and scale contrast, not color or decoration, carries the hierarchy. There are no cards, no shadows, no gradients for tone, and no rounded corners: shapes are either square or perfect circles. Color is spent almost entirely on the route bullets, where it encodes data.

The site is light-only by contract. `color-scheme: light` is declared and no dark theme exists; adding one needs the owner's approval.

**Key Characteristics:**
- Route bullets in MTA line colors, keyed to reading time at 240 words a minute.
- Black signage bands with a white top rule; one black panel inside the list (Today).
- One grotesque, Regular and Bold only, with tabular lining figures for every count.
- Dense, card-less rows on white with 1px rules; transfer signs drawn as rules.
- Flat everywhere; circles are the only curve.

## Colors

A black-and-white signage system with a seven-color route palette that exists only to say how long a story takes.

### Primary
- **Signage Black** (ink): page text, the masthead and footer bands, the Today panel, the strong 1.5–2px control borders, active line chips, the Pick button, tags, and the transfer-sign rules. The CSS names it `--ink`, `--band` and `--rule-strong`; all three are the same black.

### Secondary: the route lines
Each line color marks one reading-time band (minutes at 240 wpm) and appears only on route bullets (stop rows, filter chips, transfer signs, the footer key, the Today bullet).
- **Lexington Red** (line-1): under 5 minutes (under 1,200 words).
- **Sixth Avenue Orange** (line-2): 5 to 10 minutes (1,200 to 2,399 words).
- **Broadway Yellow** (line-3): 10 to 20 minutes (2,400 to 4,799 words). Carries a black numeral. Also the text-selection highlight.
- **Crosstown Green** (line-4): 20 to 30 minutes (4,800 to 7,199 words).
- **Eighth Avenue Blue** (line-5): 30 to 45 minutes (7,200 to 10,799 words).
- **Flushing Purple** (line-6): 45 minutes and up (10,800 words and up).
- **Shuttle Grey** (line-0): length unknown; its bullet shows a question mark.

### Tertiary
- **Signal Blue** (focus): the 2px focus outline (offset 2px) and the Pick button's hover. Same value as line-5; it reads as a signal, not as a line, because it never fills a circle.

### Neutral
- **Platform White** (ground): page ground, control strip, inputs, outline buttons, text on black.
- **Station Grey** (ink-2): secondary text on white (bylines, deks, counts in chips, word units, placeholders, guide words).
- **Hairline Grey** (rule): the 1px divider under every stop.
- **Band Grey** (band-ink-2): secondary text on black (the independence note, footer prose, Today meta).
- **Hover Grey** (hover): hover fill for chips and outline buttons.

### Named Rules
**The Line Means Length Rule.** A line color appears only as a route bullet and only to state a reading-time band. Never use a line color for decoration, emphasis, links or backgrounds. Bands are fixed: under 5, 5–10, 10–20, 20–30, 30–45, 45+ minutes, grey for unknown.

**The One Black Panel Rule.** Black fills only the masthead band, the footer band, and, inside the list, the Today panel. No other element in the list gets a black panel.

**The Numeral Color Rule.** Bullet numerals are white, except on Broadway Yellow, where they are black.

## Typography

**Display Font:** Heros (TeX Gyre Heros, self-hosted woff2, GUST Font License), with Helvetica Neue, Helvetica, Arial, sans-serif
**Body Font:** the same Heros
**Label/Mono Font:** none; numbers use Heros with tabular lining figures

**Character:** One grotesque at every size, as on the signs. Bold stands in for Helvetica Medium because the free clone ships only Regular (400) and Bold (700); display sizes are moderated and tightened slightly so Bold still reads as signage rather than shouting.

### Hierarchy
- **Display** (700, clamp(32px, 5vw, 56px), 1.02, -0.01em, balanced wrap): the masthead title only, white on the black band.
- **Station** (700, clamp(26px, 4vw, 40px), -0.02em): the word "Today" in the Today panel, like a station name.
- **Headline** (700, clamp(22px, 3vw, 32px), 1.1, -0.02em): the picked story's title in the Today panel.
- **Standfirst** (400, clamp(17px, 2vw, 20px), 1.35, max 70ch): the one-line explanation under the title.
- **Title** (700, 19px, 1.2, -0.01em; 17px under 640px): each stop's story title, a link with no underline at rest.
- **Body** (400, 16px, 1.45): base text. Deks run 15px/1.45 in Station Grey, max 68ch; footer prose 14px/1.55, max 72ch.
- **Meta** (400, 13–14px): bylines and dates (14px), status line, word units and the independence note (13px).
- **Label** (700, 14–15px): line chips, buttons, transfer signs.
- **Numeral** (700, 18px, line-height 1, -0.02em, tabular): bullet minutes. 26px in the Today bullet, 15px when three digits, 11px in small bullets, 15px in 36px mobile bullets.
- **Tag** (700, 10px, 0.06em, uppercase): the inline "Fiction writer" mark in a byline; the only uppercase text in the system.

### Named Rules
**The One Grotesque Rule.** Heros Regular and Bold only. No second family, no italics, no other weights.

**The Scale Does Hierarchy Rule.** Rank is shown by size and the Regular/Bold switch, never by color. Text color is black, Station Grey, or their on-black equivalents.

**The Tabular Figures Rule.** Every count, word total, minute and word span sets in tabular lining figures so columns of numbers hold still.

## Layout

A single centered column (max 1080px) with a fluid gutter (clamp(16px, 4vw, 40px)). Bands run full bleed; their content sits in the same column.

Page order: black masthead band; a toolbar of search, decade and sort selects and two checkboxes that scrolls away; a sticky control strip (white, 2px black bottom rule, respects the top safe-area inset) holding the line chips, the "In view: X–Y words" guide words, the story count and the Pick button; the Today panel when present; the list; a centered "Show more" button; the black footer band holding the line key and method notes.

Each stop is a three-column grid: bullet (44px) | title, byline and dek | word count and unit, right-aligned. Column gap 18px, row padding 13px, 1px Hairline Grey rule between rows. When sorted by length, a transfer sign opens each new line.

Spacing is tight and practical rather than a strict scale: 6px between chips, 8–12px inside controls, 18px between row columns, 22–24px before signs and the Today panel, 64px before the footer.

One breakpoint, 640px. Below it the masthead padding tightens; stop columns become 36px | 1fr | auto with a 12px gap; the line chips become a single edge-to-edge horizontal scroller with a hidden scrollbar; search spans both columns above the two selects; the Pick button reads "Pick one"; Hide moves under the word count; and the Today panel stacks "Today" and the actions full width.

## Elevation & Depth

Flat. There are no shadows anywhere. Depth comes only from black-versus-white surfaces and rule weight: 1px hairlines between stops, 1.5px black borders on controls, a 2px black rule under the sticky strip, a 5px black rule over transfer signs.

### Named Rules
**The Flat Signage Rule.** No box shadows, no blur, no tonal gradients. If something must stand forward, it turns black or gets a heavier rule.

## Shapes

Square corners everywhere (0px; inputs and selects are reset to 0). The one curve is the perfect circle of the route bullet (50%), in 22px, 36px, 44px and 64px sizes. Borders are 1.5px solid black on interactive controls. The select's caret is two hard-stop linear gradients forming a small chevron; that drawing technique is allowed because it renders a solid shape, not a tonal blend. The Pick and Read arrows are inline 24-unit SVG strokes (2.5px), drawn as a straight signage arrow.

**The Circle-or-Square Rule.** A shape is either square-cornered or a perfect circle. No intermediate radii, pills or rounded rectangles.

## Components

### Route Bullet
The signature element: a perfect circle in its line color holding the reading time in minutes.
- **Sizes:** 44px default (18px numeral), 22px small (no numeral in chips, signs and key), 64px in Today (26px numeral), 36px on mobile rows.
- **Color:** line color fill; white numeral, black on yellow; grey with "?" for unknown length. Three-digit minutes drop to 15px (12px on mobile).
- **Labeling:** each bullet carries an aria-label such as "12 minute read"; decorative small bullets are aria-hidden.

### Line Chips (filters)
- **Style:** square, 38px tall (34px mobile), 1.5px black border, white fill, a small bullet then the band name in Bold 14px and the count in Regular Station Grey.
- **States:** hover Hover Grey; pressed (aria-pressed) turns solid black with white text and the count at 70% opacity. The first chip, "All", has no bullet.

### Buttons
- **Shape:** square (0px).
- **Pick (primary):** solid black, white Bold 14px, 34px tall, 12px side padding, trailing signage arrow; hover turns Signal Blue. The only filled button on white.
- **Outline ("Show more"):** white, 1.5px black border, Bold 15px, 42px tall, 20px side padding; hover Hover Grey.
- **On black (Today panel):** "Read on newyorker.com" is solid white with black text and the arrow; "Pick another" is transparent with a 1.5px white border. Both 38px tall, Bold 14px.
- **Text action (Hide/Unhide, Hidden count):** Regular 12px Station Grey, underlined (offset 2px); hover turns black.
- **Focus:** every focusable element gets a 2px Signal Blue outline at 2px offset.

### Inputs / Fields
- **Style:** search and selects are 38px tall, white, 1.5px black border, square, Regular 15px, 10px side padding; placeholder in Station Grey. Selects use the hard-stop chevron.
- **Checkboxes:** 16px native boxes with black accent color, labels Regular 14px.
- **Focus:** the global Signal Blue outline.

### Control Strip (navigation)
Sticky at the top, white, closed by a 2px black rule. Holds the line chips, then a status line: guide words ("In view: 2,410–2,980 words") left in Station Grey 13px, the bold story count and the Pick button right.

### Stop Row (list item)
Bullet | body | length. Title is Bold 19px with no underline at rest and a 2px underline at 3px offset on hover; byline in 14px Station Grey with dot separators, an optional "Fiction writer" tag, and Hide; optional dek below. Right column shows the word count in Bold 16px tabular with "words" in 13px grey, or an em dash and "scan only" when length is unknown.

### Transfer Sign
A line header inside the length-sorted list, drawn with rules, not as a panel: 5px black rule above, 1px black rule below, a small bullet and the band name in Bold 15px on the white ground. Decorative (aria-hidden).

### Today Panel
The only black panel in the list. Black fill, 30px 24px 24px padding, a 2px white rule 8px below its top edge (the band rule), then "Today" in Station size, the 64px bullet, the headline and meta in Band Grey, and the two on-black buttons. It enters with a left-to-right clip-path wipe (420ms, cubic-bezier(0.16, 1, 0.3, 1)) only when reduced motion is not requested; the page then scrolls it into view under the sticky strip (instant under reduced motion).

### Signage Band
Masthead and footer: full-bleed black with a 2px white rule 10px below the top edge. White text, Band Grey for secondary text. The footer holds the line key (small bullets plus band names in 13px white) and the method notes.

### Tag
Inline black block with white Bold 10px uppercase text tracked 0.06em, 1px 5px 0 padding, nudged 1px up to sit on the byline. Used only for "Fiction writer".

## Do's and Don'ts

### Do:
- **Do** lead every story with a route bullet in its band's line color, minutes inside, computed at 240 words a minute.
- **Do** keep text to Heros Regular (400) and Bold (700), and use Bold where the signage tradition uses Medium.
- **Do** set every number in tabular lining figures.
- **Do** separate rows with 1px Hairline Grey (#d6d6d6) rules and draw line headers as rules (5px over, 1px under), not panels.
- **Do** put the thin white rule inside the top edge of every black band or panel (2px).
- **Do** use 1.5px black borders and square corners on all controls, and the 2px Signal Blue outline for focus.
- **Do** gate motion behind prefers-reduced-motion.

### Don't:
- **Don't** use a line color for anything except a reading-time bullet.
- **Don't** add a second black panel inside the list; Today is the only one.
- **Don't** use cards, shadows, tonal gradients, or any radius other than a perfect circle.
- **Don't** add a second typeface, italics or intermediate weights, or serve the magazine's proprietary fonts.
- **Don't** add a dark theme without the owner's approval; the world is light-only.
- **Don't** rank text with line colors or extra grey tints; size and weight do that, with Station Grey reserved for secondary text.
