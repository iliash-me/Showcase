# Marketplace Item Showcase Pages

Landing pages for presenting items on ThemeForest and CodeCanyon (or any marketplace): the "live preview" page that shows buyers every demo, screen and feature at a glance. Six variations share one stylesheet and one script:

| File | For | Product (sample) | Theme |
| --- | --- | --- | --- |
| `index.html` | ThemeForest: HTML site template | Nexora | Indigo |
| `admin-dashboard.html` | ThemeForest: admin dashboard template | Vantage | Sky blue (`.theme-admin`) |
| `wordpress-theme.html` | ThemeForest: WordPress theme | Aurelia | Rose (`.theme-wp`) |
| `php-ai-saas.html` | CodeCanyon: PHP/Laravel AI content SaaS script | Quillo | Violet (`.theme-ai`) |
| `php-pos-inventory.html` | CodeCanyon: PHP/Laravel POS & inventory script | Stockly | Emerald (`.theme-pos`) |
| `php-whatsapp-automation.html` | CodeCanyon: PHP/Laravel WhatsApp marketing & automation script | Replyo | Teal (`.theme-wa`) |

- **No build step.** Plain HTML, CSS and vanilla JS. Open any `.html` file or deploy the folder anywhere.
- **No dependencies.** The only external request is Google Fonts.
- **Responsive and accessible.** Mobile menu, keyboard focus styles, `prefers-reduced-motion` support, no horizontal scroll down to 320px.

Pick the page that matches your product, delete the others, and remove the **variation switcher** block (marked with a comment near the end of each page) before going live.

## What's on each page

All pages share: sticky header, hero with stats and a 3-browser showcase, tech/plugin strip, features grid, reviews, changelog, FAQ, pricing CTA and footer.

| Page | Product-specific sections |
| --- | --- |
| HTML template | Filterable demo grid, dark-mode / responsive / UI-blocks spotlights, inner pages, Lighthouse scores |
| Admin dashboard | Framework versions (HTML, React, Next.js, Vue, Angular, Laravel), filterable dashboards, **live customizer** (switch light/dark/semi-dark/horizontal and tint the brand color), apps & pages, developer-experience terminal |
| WordPress theme | Filterable starter sites, 3-step one-click demo import with importer screenshot, Elementor builder and WooCommerce spotlights, PageSpeed scores |
| AI SaaS script | **Live demo logins** with copy buttons (landing, user, admin), screens filtered by Frontend / User / Admin, AI-tools and monetization spotlights, AI provider and payment gateway integrations, server requirements and installation, **Regular vs Extended license** comparison |
| POS script | Role-based demo logins (admin, manager, cashier), modules grid, filterable screens, supported hardware, **roles & permissions matrix**, requirements, license comparison |
| WhatsApp script | Demo logins (SaaS admin, business, agent), 3-step "how it works", filterable screens (inbox, chatbot flow builder, campaign builder with phone preview, templates, widget), chatbot / inbox / campaign spotlights, app and payment integrations, requirements, license comparison, Meta trademark note in the footer |

## Project structure

```
index.html  admin-dashboard.html  wordpress-theme.html
php-ai-saas.html  php-pos-inventory.html  php-whatsapp-automation.html
assets/
  css/style.css          # all styles; design tokens in :root, per-page themes in section 16
  js/main.js             # nav, filters, reveal, counters, score rings, copy buttons, customizer, switcher
  img/
    favicon.svg
    demos/  pages/       # HTML template previews (placeholders)
    admin/               # admin dashboards, layout variants and app screens
    wp/                  # WordPress starter sites, importer and page builder
    ai/  pos/  wa/       # PHP script screens
tools/
  generate_thumbnails.py # regenerates every placeholder preview
  app_screens.py         # app/admin screen drawing (used by the script above)
```

## Customizing

### 1. Name, price and links
Search the page you're using and replace:

- The product name (`Nexora`, `Vantage`, `Aurelia`, `Quillo`, `Stockly` or `Replyo`) and the logo letter in the header and footer SVG
- Prices (`$19`, `$29`, `$59`, `$69`, `$49` and the license prices)
- `https://themeforest.net/` / `https://codecanyon.net/`: your item URL
- `demo/...` links and `https://demo.example.com/...`: your live demo URLs
- Demo credentials (`admin@example.com` / `demo1234`, etc.) in the live demo cards
- `support@example.com`, social links (`href="#"`), "Your Studio"

The stats, ratings, reviews, changelog entries, performance scores and license terms are **sample content**. Replace them with your item's real details before publishing, and check license wording against the marketplace's official terms. If your product integrates a third-party service (like WhatsApp), keep a trademark/non-affiliation note and don't use that brand's logo; the WhatsApp page shows one way to do it.

### 2. Brand colors and font
Each page sets its colors with a class on `<body>` (`theme-admin`, `theme-wp`, `theme-ai`, `theme-pos`, `theme-wa`; no class means the default indigo). Edit that theme in section 16 of `assets/css/style.css`, or add your own:

```css
.theme-mine {
  --primary: #2563eb; --primary-600: #1d4ed8; --primary-50: #eaf1ff;
  --primary-rgb: 37 99 235;          /* same color as space-separated RGB, used for shadows */
  --primary-light: #93c5fd;          /* accent text on dark sections */
  --grad: linear-gradient(120deg, #60a5fa, #2563eb 45%, #7c3aed);
  --glow-1: #2563eb; --glow-2: #7c3aed; --glow-3: #3b82f6;  /* hero background glows */
}
```

### 3. Real screenshots
Every image in `assets/img/` is a generated placeholder. Replace them with real screenshots:

- **Websites and starter sites:** full-page screenshots ~800px wide (or 1600px for retina), any height. Taller images scroll on hover.
- **Admin and app screens:** ~1200px wide desktop screenshots (or 2400px for retina).
- Save as `.webp`/`.jpg`, update each `src`, and set `width`/`height` to the real size to avoid layout shift.
- **Admin customizer:** the buttons swap between the `data-src` images, so provide a screenshot per layout (light, dark, semi-dark, horizontal). The color swatches tint the preview with `hue-rotate`; adjust each `data-hue` to suit your palette.

To change the placeholders instead, edit the definitions in `tools/generate_thumbnails.py` / `tools/app_screens.py` and run:

```bash
python3 tools/generate_thumbnails.py
```

### 4. Adding cards
Copy an `<article class="demo-card">` block and set `data-category` to one or more filter keys used by that page's filter buttons. Filter counts update automatically. To add a filter, add a `<button class="filter-btn" data-filter="key">`.

## Browser support
Latest Chrome, Edge, Firefox and Safari. The score-ring fill animation uses `@property` and theme glows use `color-mix()`; older browsers still show the final values with simpler colors.
