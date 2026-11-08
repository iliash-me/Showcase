# Nexora — ThemeForest Template Showcase

A landing page for presenting a multipurpose HTML template on ThemeForest (or any marketplace): the item's "live preview" home that shows buyers every demo, inner page and feature at a glance.

- **No build step.** Plain HTML, CSS and vanilla JS. Open `index.html` or deploy the folder anywhere.
- **No dependencies.** The only external request is Google Fonts.
- **Responsive and accessible.** Mobile menu, keyboard focus styles, `prefers-reduced-motion` support, no horizontal scroll down to 320px.

## Sections

| Section | Anchor | Notes |
| --- | --- | --- |
| Hero | `#top` | Headline, CTAs, rating, animated stats, 3-browser showcase |
| Tech strip | — | "Built with" chips |
| Demos | `#demos` | Filterable grid (counts are calculated automatically), scroll-on-hover previews, New/Popular/Dark badges |
| Spotlight | `#highlights` | Dark mode, responsive devices, UI blocks |
| Inner pages | `#pages` | 16 page previews and an element chip list |
| Features | `#features` | 16 feature cards with inline SVG icons |
| Performance | `#performance` | Animated Lighthouse score rings |
| Reviews | `#reviews` | Rating summary and review cards |
| Changelog | `#changelog` | Release timeline with collapsible older releases |
| FAQ | `#faq` | Native `<details>` accordion |
| CTA and footer | — | Pricing card, purchase links |

## Project structure

```
index.html
assets/
  css/style.css          # all styles; design tokens at the top (:root)
  js/main.js             # nav, filter, reveal, counters, score rings
  img/
    favicon.svg
    demos/*.svg          # homepage previews (placeholders)
    pages/*.svg          # inner-page previews (placeholders)
tools/
  generate_thumbnails.py # regenerates the placeholder previews
```

## Customizing

### 1. Name, price and links
Search `index.html` for these and replace them:

- `Nexora`: your template name
- `$19` / `$49`: your price
- `https://themeforest.net/`: your item URL, e.g. `https://themeforest.net/item/your-item/12345678`
- `demo/index-*.html` and `demo/*.html`: URLs of your live demos and inner pages
- `support@example.com`, social links (`href="#"`), "Your Studio"

The stats, ratings, reviews, changelog entries and Lighthouse scores are **sample content**. Replace them with your item's real numbers before publishing.

### 2. Brand colors and font
Edit the tokens at the top of `assets/css/style.css`:

```css
:root {
  --primary: #5b5bf7;
  --grad: linear-gradient(120deg, #7c6bff 0%, #5b5bf7 45%, #22c3ee 100%);
  --font: "Plus Jakarta Sans", ...;
}
```

### 3. Real screenshots
The previews in `assets/img/demos` and `assets/img/pages` are generated placeholders. Replace them with **full-page screenshots** of your template:

- Width ~800px (or 1600px for retina), any height. Taller images scroll on hover.
- Save as `.webp`/`.jpg`, update each `src`, and set the `width`/`height` attributes to the real size to avoid layout shift.

Want different placeholder styles or colors? Edit `DEMOS` / `PAGES` in `tools/generate_thumbnails.py` and run:

```bash
python3 tools/generate_thumbnails.py
```

### 4. Adding a demo
Copy a `<article class="demo-card">` block in `index.html` and set `data-category` to one or more filter keys (`business agency saas landing portfolio shop`). The filter counts update automatically. To add a new filter, add a `<button class="filter-btn" data-filter="key">`.

## Browser support
Latest Chrome, Edge, Firefox and Safari. The score-ring fill animation uses `@property`; browsers without it still show the final value.
