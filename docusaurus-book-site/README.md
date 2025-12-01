# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator, to present the "Physical AI & Humanoid Robotics" book content.

## Installation

```bash
npm install
# or
yarn install
```

## Local Development

```bash
npm start
# or
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
npm run build
# or
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

## Developer Documentation

### Content Management

The book content is located in the `docs/book-content-internal/` directory within this project. To update the book content:
1.  Place your Markdown/MDX files within `docs/book-content-internal/`.
2.  Ensure `_category_.json` files are correctly used in module subdirectories for proper sidebar generation.
3.  The Docusaurus build process will automatically pick up changes.

### Theme Customization

The robotics theme is primarily defined in `src/css/custom.css` and `src/css/custom-elements.module.css`.
*   **Fonts**: Updated in `src/css/custom.css` to Orbitron (headings), Inter/Roboto (body), JetBrains Mono (code).
*   **Colors**: Defined as CSS variables in `src/css/custom.css`'s `:root` selector.
*   **Components**: Custom styles for buttons, links, and sidebars are in `src/css/custom.css`. Advanced elements like circuit-line dividers and AI-grid backgrounds are in `src/css/custom-elements.module.css`.
To extend the theme, modify these CSS files directly.

### Rebuilding the Site

After any content or theme changes, run `npm run build` (or `yarn build`) to generate the updated static site.

---
