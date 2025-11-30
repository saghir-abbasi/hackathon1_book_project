# Implementation Plan: Docusaurus Setup & Publish Book Contents

**Branch**: `002-docusaurus-book-site` | **Date**: 2025-11-30 | **Spec**: [specs/002-docusaurus-book-site/spec.md](specs/002-docusaurus-book-site/spec.md)
**Input**: Feature specification from `/specs/002-docusaurus-book-site/spec.md`

## Summary

This implementation plan outlines the strategy for setting up a Docusaurus project to serve as the documentation website for the "Physical AI & Humanoid Robotics" book content. The core objective is to initialize a Docusaurus site, seamlessly integrate the external `book-content/` directory without duplication, automatically generate navigation sidebars based on the content structure, configure top-level navigation, and apply a comprehensive robotics-themed visual design. The plan strictly adheres to the principle of only reading, loading, and presenting existing content, explicitly excluding any content generation or modification within the Docusaurus project itself.

## Technical Context

**Language/Version**: Node.js >= 18, JavaScript (for Docusaurus configuration), React (for custom theming components).  
**Primary Dependencies**: Docusaurus 3.x (`@docusaurus/init`, `@docusaurus/preset-classic`), `npm` (or `yarn`).  
**Storage**: Local Filesystem (Docusaurus project files, referencing external `book-content/`).  
**Testing**:
-   `npm run start`: Verify local development server functionality and content rendering.
-   `npm run build`: Verify successful static site generation without errors or warnings.
-   Visual inspection: Confirm UI/UX theme adherence.
-   Functional testing: Verify navigation, sidebar generation, and content display.
**Target Platform**: Web browser (static site).  
**Project Type**: Web Application (Static Site Generator).  
**Performance Goals**: Sidebar loading < 200ms for up to 500 files, smooth site loading on low-end devices.  
**Constraints**:
-   Docusaurus project directory MUST be separate from `book-content/`.
-   `book-content/` files MUST NOT be duplicated or moved into the Docusaurus project.
-   No remote script execution within Docusaurus config or integrated content.
-   Absolute file paths MUST NOT be exposed in Docusaurus logs or configuration.
-   Maintain full compatibility with Windows, macOS, and Linux.
-   Support both `npm` and `yarn`.
**Scale/Scope**: Publish all existing content from 4 modules, 8 chapters (expandable up to 500 files for performance). Future extensibility for deployment, search, etc., must be considered without refactoring.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   **Article I — Library-First & Modular Design**: PASSED. Docusaurus project will be a separate, modular component, consuming the `book-content/` as an external library.
-   **Article II — Spec-Driven & Test-First Workflow**: PASSED. Plan is derived from spec and includes clear validation steps (build/run checks).
-   **Article III — Documentation, Content & Code Quality Standards**: PASSED. Docusaurus configuration will be clean, minimal, and well-commented, promoting maintainability.
-   **Article IV — Content & Deployment Standard (Book + UI)**: PASSED. Directly implements the constitutional requirement for a static site via Docusaurus for the book, and maintains separation of static content from dynamic components.
-   **Article V — RAG & AI Integrations: Privacy, Security & Data Handling**: PASSED. Constraints explicitly forbid remote script execution and exposure of absolute file paths, addressing security.
-   **Article VI — Reusable Intelligence: Subagents & Agent Skills**: N/A for this phase.
-   **Article VII — Internationalization & Personalization Support**: PASSED. Docusaurus provides robust i18n support, and the design will accommodate future personalization based on existing content metadata.
-   **Article VIII — Simplicity & Minimalism**: PASSED. Focus is strictly on Docusaurus setup and content integration, avoiding over-engineering.
-   **Article IX — Version Control, Release & Traceability**: PASSED. All Docusaurus configuration and custom theme code will be version-controlled.

## Project Structure

### Documentation (this feature)

```text
specs/002-docusaurus-book-site/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (N/A for this feature)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
docusaurus-book-site/ # New Docusaurus project directory
├── blog/
├── docs/ # Configured to point to ../book-content/
├── src/
│   ├── css/ # Custom CSS for theme
│   ├── theme/ # Custom theme components (e.g., Navbar, Footer)
│   └── pages/ # Custom pages (e.g., landing page)
├── static/ # Favicon, logo, other static assets
├── docusaurus.config.js
├── sidebars.js # Auto-generated from filesystem
├── package.json
├── yarn.lock (or package-lock.json)
└── ... (other Docusaurus boilerplate files)

book-content/ # Existing directory (external to Docusaurus project)
└── ... (modules, chapters, metadata, shared assets)
```

**Structure Decision**: The Docusaurus project will reside in a new `docusaurus-book-site/` directory at the repository root, ensuring clear separation from the `book-content/` directory. The `docusaurus.config.js` will be configured to point its docs source to `../book-content/`. Custom theme elements will reside in `src/css/` and `src/theme/` within the Docusaurus project.

## High-Level Goal

Initialize a Docusaurus project (`docusaurus-book-site/`), configure it to seamlessly integrate and publish content from the external `book-content/` directory. Apply a custom robotics-themed UI, ensure automatic sidebar generation, add top-level navigation, and confirm successful build and local serving, all while maintaining strict content/presentation separation.

## Breakdown of Major Workstreams

1.  **Docusaurus Project Initialization**: Create the Docusaurus project with the official template.
2.  **Content Integration & Navigation Setup**: Configure Docusaurus to link to `book-content/`, auto-generate sidebars, and set up top navigation.
3.  **Robotics-Themed UI Customization**: Implement the specified color scheme, typography, and graphic elements using custom CSS and Docusaurus theming features.
4.  **Build & Runtime Verification**: Ensure the site builds successfully and serves content correctly in development mode.

## Detailed Steps for Each Workstream

### 1. Docusaurus Project Initialization

-   Create new Docusaurus project: `npx create-docusaurus@latest docusaurus-book-site classic` in the repository root.
-   Verify Node.js version is >= 18.

### 2. Content Integration & Navigation Setup

-   Modify `docusaurus-book-site/docusaurus.config.js`:
    -   Update `docs` plugin configuration to point `path` to `../book-content`.
    -   Configure `routeBasePath` for the docs plugin (e.g., `/book`).
    -   Ensure `editUrl` is disabled or correctly configured to point to the `book-content` GitHub repo if applicable.
-   Configure `sidebars.js` (or integrate a plugin for automatic filesystem-based sidebar generation):
    -   Set up `sidebar` entry for `docs` to read from the content directory.
    -   Ensure subfolders appear as collapsible categories.
    -   Ensure root-level files appear as top-level items.
-   Update `docusaurus-book-site/docusaurus.config.js` `navbar` section:
    -   Add a `type: 'doc'`, `docId: 'book-content/modules/module-1-robotic-nervous-system/chapter-1-ros2-basics'` (or similar first chapter), `position: 'left'`, `label: 'Book'` item.

### 3. Robotics-Themed UI Customization

-   **Color Scheme**:
    -   Modify `docusaurus-book-site/src/css/custom.css` (or equivalent theme file):
        -   Define CSS variables for primary (`--ifm-color-primary: #00A8E8;`), secondary (`--ifm-color-secondary: #2EE8E6;`), accent (`--ifm-color-accent: #F6C90E;`), dark background (`--ifm-background-dark: #0D0D0D;`), light background (`--ifm-background-light: #E8ECEF;`).
        -   Implement hover effects for buttons (neon cyan outer shadow) and links (underline + robotics yellow shift) using CSS.
-   **Typography**:
    -   Import "Orbitron", "Inter", "Roboto", and "JetBrains Mono" fonts. This might involve:
        -   Adding `@import` rules in `custom.css` (from Google Fonts or local files).
        -   Updating `docusaurus-book-site/src/css/custom.css` to apply fonts:
            -   `h1, h2, h3, h4, h5, h6 { font-family: 'Orbitron', sans-serif; }`
            -   `body { font-family: 'Inter', 'Roboto', sans-serif; }`
            -   `code, pre { font-family: 'JetBrains Mono', monospace; }`
    -   Apply specific styling rules for headings (bold, uppercase, letter-spacing for H1-H4).
-   **Graphics & UI Elements**:
    -   Create custom CSS modules or components (e.g., `docusaurus-book-site/src/css/custom-elements.module.css`) for:
        -   Circuit-pattern section dividers.
        -   Mecha-panel buttons with soft edges and neon glow (via box-shadow).
        -   Subtle neon border and hover glow for sidebars.
        -   Optional faint AI-mesh background patterns (e.g., via `background-image` in `custom.css`).
    -   Replace default Docusaurus favicon and logo in `docusaurus-book-site/static/` with robotics-themed equivalents.
-   **Layout Behavior**:
    -   Adjust Docusaurus theme configuration (e.g., `themeConfig.docs.sidebar.width`) and `custom.css` for wide layout and generous horizontal padding.
-   **Dark Mode**:
    -   Configure `docusaurus-book-site/docusaurus.config.js` `themeConfig.colorMode.defaultMode: 'dark'`.
    -   Ensure light mode theme is also consistent with robotics styling.

### 4. Sidebar & Navigation Strategy

-   Utilize Docusaurus's built-in filesystem-based sidebar generation for the docs plugin. This might involve setting `sidebarPath: 'autogenerated'`, or custom plugin configuration if manual override is needed.
-   Ensure `_category_.json` files (or similar Docusaurus conventions) are respected within `book-content/modules/` to define collapsible categories.
-   Add top `navbar` item as described in Workstream 2.

### 5. Integration Constraints

-   Content integration will use Docusaurus's `docs` plugin `path` configuration, referencing `../book-content/`, thereby avoiding file duplication or movement.
-   The Docusaurus project `docusaurus-book-site/` will be physically separate from `book-content/`.
-   All configuration will adhere to cross-platform compatibility for Windows, macOS, Linux, and support `npm` and `yarn`.

## Tools, Commands, and Dependencies

-   **Node.js**: Version 18.x or higher.
-   **npm** (or **yarn**): Package manager.
-   **Docusaurus CLI**: `npx create-docusaurus@latest`, `npm start`, `npm build`.
-   **Required Docusaurus Plugins**: `@docusaurus/preset-classic` (contains docs, blog, pages plugins). Potentially `@docusaurus/plugin-content-docs` if custom configuration is extensive.
-   **Paths**:
    -   Docusaurus project root: `docusaurus-book-site/`
    -   Book content root: `book-content/` (external)
    -   Custom CSS: `docusaurus-book-site/src/css/custom.css`
    -   Custom Theme Components: `docusaurus-book-site/src/theme/` (if extending/swizzling components)
    -   Static assets: `docusaurus-book-site/static/`

## Validation Plan

-   Execute `npm run start` in `docusaurus-book-site/` and:
    -   Verify all `book-content/` pages load correctly.
    -   Confirm sidebar reflects the exact `book-content/` folder structure (collapsible categories, top-level items).
    -   Check that the top navigation includes a working "Book" or "Documentation" link.
    -   Visually inspect the site to ensure the robotics theme (colors, typography, graphic elements) is applied globally and consistently across UI elements in both dark and light modes.
    -   Verify relative paths within content (e.g., links between chapters, asset references) resolve correctly.
-   Execute `npm run build` in `docusaurus-book-site/` and:
    -   Confirm the build completes without warnings or errors.
    -   Verify that no duplication or movement of `book-content` files occurred.
-   Perform browser compatibility checks (conceptual).

## Deliverables

-   A completed `plan.md` describing all implementation steps for the Docusaurus setup.
-   Clear mapping of tasks to specific configuration files and file updates.
-   No actual implementation will be performed in this planning phase.
-   `research.md` will contain the font import strategies.
-   `quickstart.md` will outline how to setup the Docusaurus site locally.

## Phase 0: Outline & Research

### Research Tasks

The plan heavily relies on Docusaurus's theming capabilities and font integration. While Docusaurus is well-documented, specific research might be needed for optimal implementation of the detailed UI/UX requirements.

1.  **Docusaurus Theming Best Practices**: Research the most effective and maintainable ways to customize Docusaurus 3.x's classic theme to achieve the specified robotics aesthetic (color scheme, typography, graphic elements) using custom CSS, `themeConfig`, and potentially component swizzling.
    *   **Decision**: Prioritize custom CSS variables (`custom.css`) and `themeConfig` for colors and basic typography. Use `src/theme/` for swizzling components only if necessary for complex UI elements like custom buttons or sidebar effects.
    *   **Rationale**: Minimizes maintenance overhead and maximizes compatibility with future Docusaurus updates.
    *   **Alternatives considered**: Extensive component swizzling (more powerful but higher maintenance); using a third-party theme (might not match specific robotics aesthetic).

2.  **Web Font Integration**: Research the most reliable and performant methods for integrating custom fonts ("Orbitron", "Inter", "Roboto", "JetBrains Mono") into a Docusaurus site, ensuring compatibility and graceful fallback.
    *   **Decision**: Utilize Google Fonts `@import` for "Orbitron", "Inter", "Roboto". "JetBrains Mono" can be served locally if not available via Google Fonts or a similar CDN. Ensure `font-display: swap` for performance.
    *   **Rationale**: Google Fonts provides ease of use and performance. Local hosting provides control.
    *   **Alternatives considered**: Hosting all fonts locally (more control but potential performance impact); using only system fonts (misses aesthetic requirements).

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

Not applicable for this feature. The feature consumes existing data (book content) and does not introduce new persistent data models.

### API Contracts (`contracts/`)

Not applicable for this feature. This feature is about static site generation and UI, not API development.

### Quickstart Guide (`quickstart.md`)

This guide will provide instructions for setting up the Docusaurus development environment and running the site locally.

**Outline**:
1.  **Setup**:
    *   Ensure Node.js (>=18) and npm/yarn are installed.
    *   Clone the repository.
    *   Navigate to `docusaurus-book-site/`.
    *   Install dependencies: `npm install` (or `yarn`).
2.  **Running the Site**:
    *   Start development server: `npm start` (or `yarn start`).
    *   Access the site in browser (typically `http://localhost:3000`).
3.  **Building the Site**:
    *   Generate static build: `npm run build` (or `yarn build`).
    *   Serve the built site locally (e.g., `npm run serve`).

### Agent Context Update

The primary technology introduced in this phase is Docusaurus, Node.js, and associated web development tools. I will update the agent's context to reflect this new capability.

```text
# .specify/memory/constitution.md (excerpt)
# ... (existing content)
# Ensure to preserve this file manually. Do not overwrite.
```