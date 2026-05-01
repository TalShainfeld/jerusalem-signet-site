# README History

## 2026-05-01

- Fixed mobile subject hamburger dropdown overlap:
  - adjusted `header .site-nav-menu` `top` offset (dropdown starts below the hamburger button)
  - raised `header .site-nav-menu` `z-index` above `header .site-nav-toggle` so the button no longer renders on top of the menu choices
  - hide the hamburger toggle while the menu is open via `header .site-nav-toggle[aria-expanded="true"]` (prevents any overlap on mobile)

## 2026-04-29

- Cleaned up `privacy.html` into a valid standalone HTML page (removed pasted chat/transcript content).
- Aligned `privacy.html` navigation with the active funnel pages (`index.html` → Heritage/Collection/Wisdom/Connect) and kept the page responsive via shared styles plus minimal page-specific layout rules.
- Removed broken footer image references from `privacy.html` (logo-only branding) so the page doesn’t render missing assets.
- Added a footer link to `privacy.html` (`<a href="privacy.html">Privacy Policy</a>`) across pages that use the shared `main-footer` block.
- Added a top-of-page “Back to Main Page” link in `privacy.html` for quick navigation to `index.html`.
- Mobile-first improvements (primary target ≤992px):
  - Added missing `<meta name="viewport" ...>` to `collection.html`, `heritage.html`, `connect.html`, and `blessings.html`.
  - Fixed a CSS syntax-breaking divider near the end of `css/style.css` (the “BLESSINGS-Tribes” section header).
  - Added a shared responsive baseline in `css/style.css` (typography scaling, spacing, overflow prevention, touch-friendly nav/menu sizing).
  - Updated `js/script.js` to respect `prefers-reduced-motion` and to use `IntersectionObserver` for reveal animations when available (reduces scroll-jank on mobile).

## 2026-04-23

- Reworked `build.py` so Pinterest output is isolated under `pinterest_upload/<id>/index.html` via Jinja template `pinterest_landing.html.j2`, without overwriting root `wisdom.html` or emitting root `wisdom_*.html` from this script.
- Added `flatten_content_paragraphs()` / `build_pinterest_item()` so each landing injects the full narrative from `content.json` (intro, symbols, PARDES layers, section types, stories, Joseph subsections) into `item.content`, with verses and titles mapped for the template.
- Documented the build pipeline and function responsibilities in `README.md`.

## 2026-04-22

- Added initial root `README.md` documenting the repository structure and the purpose of key folders/files (`*.html`, `css/`, `js/`, `assets/`, `manuals/`).
- Updated `README.md` with project background (Pinterest traffic, audience strategy via `wisdom.html`) and the current intended navigation flow (`index.html` → Collection/Wisdom/Heritage/Connect), with pricing postponed.
- Updated `wisdom.html` to expose two anchored sections (`#kol-mitzion`, `#tribes`) and a header hamburger menu for quick in-page navigation.
- Updated the header ribbon across active pages to display the page’s primary section label beside the logo (moved from hero labels) and increased navigation link size while keeping the existing visual style.
- Added a subject-ribbon hamburger navigation on active pages for easier navigation between site subjects on smaller screens.

