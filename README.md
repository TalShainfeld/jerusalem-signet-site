# Jerusalem Signet — Project Structure

Jerusalem Signet is a **static multi-page website** (HTML/CSS/JavaScript) with shared styling and shared UI behavior, plus a media folder for images/SVG and a PDF manual.

## Project background (business + audience)

JerusalemSignet.com is designed to be a **sales/interest funnel** for a collection of Judaica products.

- **Traffic source**: Pinterest pins redirect visitors into this site.
- **Audience strategy**: beyond product pages, the site uses content attraction via `wisdom.html` (Bible legends and ancestral wisdom) to attract the US evangelical community.
- **Legitimate entry point**: `index.html`.
- **Current phase site flow**: users should be able to navigate only to:
  - `collection.html`
  - `wisdom.html`
  - `heritage.html`
  - `connect.html`
- **Pricing flow status**: postponed for now. Collection-to-pricing calls-to-action are intentionally removed from the UI and kept only as “future restore” notes in markup.

## Quick start

- Open `index.html` in a browser.
- All pages reference the shared stylesheet at `css/style.css`.
- Some pages use shared behavior from `js/script.js` (pricing calculator, scroll-reveal animations, smooth anchor navigation).

## Repository layout

```text
JerusalemSignet-Project/
  index.html
  collection.html
  pricing.html
  connect.html
  heritage.html
  wisdom.html
  blessings.html

  content.json
  build.py
  pinterest_landing.html.j2
  pinterest_upload/
    <item_id>/
      index.html

  css/
    style.css
    style - Copy.css

  js/
    script.js

  assets/
    images/
      *.png, *.jpg
      pinterest/
        pin_<item_id>.jpg
      tribes/
        *.png
    svg/
      Jerusalemsignet.svg

  manuals/
    The_Sacred_Art_of_the_Sofer.pdf

  .idea/
  JerusalemSignet/
    .idea/
    .venv/
```

## Pages (root `*.html`)

- `index.html`: Home/landing page. Includes the global header navigation and a hero section, plus a featured grid and footer.
- `collection.html`: Product gallery/collection page. Uses shared styles and a gallery layout.
- `pricing.html`: Pricing/selection experience (uses the JavaScript pricing calculator in `js/script.js` when the required DOM elements exist).
- `heritage.html`: “Our Story” page (styled via the heritage-related CSS sections in `css/style.css`).
- `wisdom.html`: “Ancestral Wisdom” content page. Split into two in-page sections (`#kol-mitzion` and `#tribes`) with a header hamburger for quick navigation.
- `blessings.html`: Blessings content page.
- `connect.html`: Contact/connect page.
- `privacy.html`: Privacy policy page for site visitors. Uses the shared header/footer patterns and minimal page-specific styling for readable policy sections.

## Shared styling (`css/`)

- `css/style.css`: Single main stylesheet for all pages. Contains:
  - global reset + CSS variables
  - shared header/navigation styles
  - page-specific sections (e.g., “heritage page” styles)
  - responsive-friendly rules (e.g., images scale to container)
- `css/style - Copy.css`: A copy/variant stylesheet (currently unused unless referenced by a page).

## Shared scripts (`js/`)

- `js/script.js`: Shared page behaviors:
  - `calculateTotal()`: Computes and renders a grand total based on selections inside `.bespoke-builder`.
  - `handleReveal()`: Scroll-triggered reveal animations for common UI blocks.
  - Smooth scrolling for anchor links (`a[href^="#"]`).

## Mobile responsiveness (primary target: ≤992px)

This site is designed to be readable and easy to navigate on phones and tablets. The mobile baseline lives in the shared stylesheet and is applied consistently across pages.

### Viewport configuration (HTML)

To ensure correct responsive behavior on mobile browsers, the following pages include a viewport meta tag:

- `index.html`
- `wisdom.html`
- `privacy.html`
- `collection.html`
- `heritage.html`
- `connect.html`
- `blessings.html`

### Responsive baseline (CSS)

All responsive behavior is centralized in `css/style.css`.

- **CSS parsing reliability**: the “BLESSINGS-Tribes” divider is a valid `/* ... */` comment, preventing accidental stylesheet breakage.
- **≤992px baseline**:
  - header + nav readability and touch targets (logo sizing, menu sizing, link padding)
  - mobile subject-menu positioning: the dropdown is offset below the hamburger button so it doesn't overlap the menu items
  - typography scaling for large headings (hero/title sections) using `clamp(...)`
  - reduced letter-spacing on small screens for better readability
  - overflow prevention for long content (`overflow-wrap: anywhere`)
  - tightened section padding/gaps for content-heavy pages like `wisdom.html` and the collection layouts
- **≤768px refinements**:
  - header becomes vertical (centered) and footer branding wraps cleanly

Key CSS sections touched:
- Global navigation (`header`, `.site-nav-toggle`, `.site-nav-menu`, `.site-nav-link`)
- Home hero (`.hero`, `.hero h1`, `.hero-subtitle`)
- Wisdom posts (`.wisdom-post`, `.post-content`, `.pardes-list`)
- Collection layouts (`.collection-gallery`, `.gallery-item`, `.selection-gate`)
- Blessings page typography (`.verse-he`, `.verse-en`, `.blessing-icon`)

### Motion & scrolling behavior (JavaScript)

`js/script.js` handles animations and smooth anchor navigation while respecting accessibility and mobile performance.

- **Reduced motion support**: the script detects `prefers-reduced-motion: reduce`.
  - Smooth anchor scrolling uses `behavior: 'auto'` when reduced motion is requested.
  - Scroll reveal animations are disabled when reduced motion is requested.
- **Reveal animations performance**:
  - Uses `IntersectionObserver` when available to reveal elements without heavy scroll listeners.
  - Falls back to the existing scroll-position logic only if `IntersectionObserver` is unavailable.

## Assets (`assets/`)

- `assets/images/`: PNG/JPG images used across pages (product images, background images, icons).
- `assets/images/tribes/`: Tribe-related image set used where needed.
- `assets/svg/Jerusalemsignet.svg`: Primary logo/seal used in headers/footers.

## Manuals (`manuals/`)

- `manuals/The_Sacred_Art_of_the_Sofer.pdf`: Reference PDF shipped with the repo.

## Pinterest build (`build.py`, `content.json`, `pinterest_landing.html.j2`)

Wisdom and tribe narrative data live in `content.json` (`general_posts` and `tribes`). Running `python build.py` does **not** modify root `wisdom.html`. It only:

1. Renders each entry into `pinterest_upload/<id>/index.html` using the Jinja template `pinterest_landing.html.j2` (layout aligned with `test.html`: icon, title, optional Hebrew/English verses, body paragraphs, link back to `wisdom.html`).
2. Writes Pinterest JPEG pins to `assets/images/pinterest/pin_<id>.jpg`.

Landing pages load the same typography and CSS variables as the main site via `../../css/style.css` plus the same Google Fonts stack used on `index.html`. Hebrew verses use the `.verse-he` rules in `css/style.css` (including `var(--gold)`). Icons are shown in grayscale for a consistent B&W seal look.

### `build.py` — functions

- **`_asset_href_for_pinterest_landing(relative_path)`**: Prefixes repo-relative paths (e.g. `assets/svg/...`) with `../../` so images and styles resolve from `pinterest_upload/<id>/index.html`.
- **`_display_title(raw)`**: Chooses the page title from `title`, then `english_name`, then `name`, then `id` — covers posts, tribes, and Joseph.
- **`flatten_content_paragraphs(raw)`**: Walks `intro`, `symbols`, `pardes.layers`, `sections` (`callout`, `paragraphs`, `quote`, `reference`, `subsections`), `stories`, and `subsections` to produce a flat ordered `list[str]` for the template body.
- **`build_pinterest_item(raw)`**: Returns the `item` dict passed to Jinja (`icon`, `title`, `verse_he`, `verse_en`, `content`).
- **`create_pinterest_pin(item_id, title, subtitle)`**: Composites text onto `assets/images/templates/Galil_View.jfif` and saves `assets/images/pinterest/pin_<item_id>.jpg`.
- **`write_pinterest_landing(env, raw)`**: Ensures `pinterest_upload/<id>/` exists and writes `index.html` from `pinterest_landing.html.j2`.
- **`generate_site()`**: Loads `content.json`, runs `write_pinterest_landing` + `create_pinterest_pin` for every `general_posts` and `tribes` entry.

### `pinterest_landing.html.j2`

Jinja mapping: `item.icon` (resolved asset URL), `item.title`, `item.verse_he`, `item.verse_en`, `{% for p in item.content %}…{% endfor %}`.

## Notes

- `.idea/`: IDE metadata (JetBrains). Not required to run the site.
- `JerusalemSignet/.venv/`: Python virtual environment. Not used by the static site runtime in the browser; it’s a local development artifact.

