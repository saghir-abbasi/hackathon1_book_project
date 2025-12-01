# Tasks: Docusaurus Setup & Publish Book Contents

**Input**: Design documents from `specs/002-docusaurus-book-site/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, quickstart.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Docusaurus Project Initialization)

**Purpose**: Prepare the development environment and create the basic Docusaurus project.

- [x] T001 Verify Node.js version is >= 18.
- [x] T002 Install Docusaurus CLI globally (if not already present): `npm install -g @docusaurus/init`
- [ ] T003 if not already available then Create new Docusaurus project `docusaurus-book-site/` using `npx create-docusaurus@latest docusaurus-book-site classic`.
- [ ] T004 Navigate into the new Docusaurus project directory: `cd docusaurus-book-site/`.
- [ ] T005 Install project dependencies: `npm install` (or `yarn install`).
- [ ] T006 Verify the basic Docusaurus site runs locally: `npm start`.

---

## Phase 2: Foundational (Content Integration & Navigation)

**Purpose**: Integrate the external book content, configure automatic sidebar generation, and set up top navigation.

**⚠️ CRITICAL**: This phase must be complete before UI theming is fully functional or content is properly displayed.

- [ ] T007 Modify `docusaurus-book-site/docusaurus.config.js` to configure docs plugin `path` to `../book-content`.
- [ ] T008 Modify `docusaurus-book-site/docusaurus.config.js` to configure docs plugin `routeBasePath` to `/book`.
- [ ] T009 Modify `docusaurus-book-site/docusaurus.config.js` to disable `editUrl` for docs plugin.
- [ ] T010 Configure `docusaurus-book-site/docusaurus.config.js` to ensure filesystem-based sidebar generation, e.g., `sidebarPath: require.resolve('./sidebars.js')` (default), and ensure `_category_.json` files in `../book-content/modules/` are respected.
- [ ] T011 Update `docusaurus-book-site/docusaurus.config.js` navbar section to add a "Book" item: `type: 'doc', docId: 'modules/module-1-robotic-nervous-system/chapter-1-ros2-basics', position: 'left', label: 'Book'`.

**Checkpoint**: External content is integrated, and basic navigation is configured.

---

## Phase 3: User Story 1 - View Book Content as a Documentation Website (P1) 🎯 MVP

**Goal**: Readers can access and navigate the Physical AI & Humanoid Robotics book content through the Docusaurus website.

**Independent Test**: Launch Docusaurus dev server and verify all chapters from `book-content/` display correctly, and navigation works.

### Implementation for User Story 1

- [ ] T012 [US1] Run `npm start` in `docusaurus-book-site/` to verify book content displays correctly.
- [ ] T013 [US1] Check sidebar generation to ensure `book-content/` folder structure is accurately reflected in `docusaurus-book-site/`.
- [ ] T014 [US1] Verify the "Book" navigation item correctly links to the docs root (or first chapter).
- [ ] T015 [US1] Confirm relative paths within chapters (e.g., links to assets, other chapters) resolve correctly.

**Checkpoint**: Core book content display and navigation functionality is verified.

---

## Phase 4: User Story 2 - Experience a Robotics-Themed Interface (P1)

**Goal**: The documentation website presents a visually appealing, robotics-inspired theme.

**Independent Test**: Visually inspect Docusaurus site for adherence to specified color scheme, typography, and graphic elements.

### Implementation for User Story 2

- [ ] T016 [P] [US2] Import "Orbitron" font into `docusaurus-book-site/src/css/custom.css` (e.g., from Google Fonts).
- [ ] T017 [P] [US2] Import "Inter" and "Roboto" fonts into `docusaurus-book-site/src/css/custom.css` (e.g., from Google Fonts).
- [ ] T018 [P] [US2] Import "JetBrains Mono" font into `docusaurus-book-site/src/css/custom.css` (e.g., from Google Fonts or local asset).
- [ ] T019 [P] [US2] Define CSS variables for robotics color palette in `docusaurus-book-site/src/css/custom.css`: Primary (`#00A8E8`), Secondary (`#2EE8E6`), Accent (`#F6C90E`), Dark Background (`#0D0D0D`), Light Background (`#E8ECEF`).
- [ ] T020 [P] [US2] Apply typography rules in `docusaurus-book-site/src/css/custom.css`: "Orbitron" for headings, "Inter" or "Roboto" for body, "JetBrains Mono" for code blocks.
- [ ] T021 [P] [US2] Apply heading styling rules (H1 bold uppercase, H2-H4 semibold, letter-spacing) in `docusaurus-book-site/src/css/custom.css`.
- [ ] T022 [P] [US2] Implement button hover effects (neon cyan outer shadow) in `docusaurus-book-site/src/css/custom.css`.
- [ ] T023 [P] [US2] Implement link hover effects (underline + robotics yellow shift) in `docusaurus-book-site/src/css/custom.css`.
- [ ] T024 [P] [US2] Create placeholder graphic assets (favicon, logo) for `docusaurus-book-site/static/` with robotics theme.
- [ ] T025 [P] [US2] Update `docusaurus-book-site/docusaurus.config.js` to use custom favicon and logo.
- [ ] T026 [P] [US2] Implement custom CSS for geometric shapes, circuitry lines, AI-grid patterns, and circuit-track section dividers in `docusaurus-book-site/src/css/custom-elements.module.css` (if creating new CSS module).
- [ ] T027 [P] [US2] Outline custom CSS for mecha-panel buttons (soft edges + neon glow) in `docusaurus-book-site/src/css/custom-elements.module.css`.
- [ ] T028 [P] [US2] Implement subtle neon border and hover glow for sidebars in `docusaurus-book-site/src/css/custom.css`.
- [ ] T029 [P] [US2] Configure default dark mode activation in `docusaurus-book-site/docusaurus.config.js` (`themeConfig.colorMode.defaultMode: 'dark'`).
- [ ] T030 [P] [US2] Ensure light mode maintains robotics theme consistency.

**Checkpoint**: Robotics-themed UI is implemented and functional.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Finalize configuration, ensure compatibility, and document processes.

- [ ] T031 Run `npm run build` in `docusaurus-book-site/` to verify the site builds successfully without warnings or errors.
- [ ] T032 Verify that no duplication or movement of `book-content` files occurred during build.
- [ ] T033 Write developer documentation in `docusaurus-book-site/README.md` on:
    -   How to update content path.
    -   How to extend theme/customize UI.
    -   How to rebuild or serve the site locally.
- [ ] T034 Verify cross-platform compatibility (Windows, macOS, Linux - conceptual check).
- [ ] T035 Verify `npm` and `yarn` compatibility for package management.

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately.
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
-   **User Stories (Phase 3+)**: All depend on Foundational phase completion.
    -   User Story 1 (P1): Can proceed after Foundational.
    -   User Story 2 (P1): Can proceed after Foundational.
-   **Polish (Final Phase)**: Depends on all user stories being complete.

### User Story Dependencies

-   **User Story 1 (P1)**: No explicit dependencies on User Story 2. Focuses on content display.
-   **User Story 2 (P1)**: Depends on the basic Docusaurus setup from User Story 1 being functional for visual verification.

### Within Each User Story

-   Tasks should be performed in the listed order.
-   UI customization tasks can be parallelized.

### Parallel Opportunities

-   Most tasks within Phase 4 (User Story 2) marked [P] can run in parallel.
-   Setup tasks (T001-T006) can run sequentially or with some parallelism (e.g., T001 and T002-T005 are blocking prerequisites).
-   Foundational tasks (T007-T011) can be worked on with some parallelism, but some steps within `docusaurus.config.js` may have logical dependencies.

---

## Parallel Example: User Story 2 (Robotics-Themed UI Customization)

```bash
# Define color variables in parallel:
- [ ] T019 [P] [US2] Define CSS variables for robotics color palette in `docusaurus-book-site/src/css/custom.css`.

# Import fonts in parallel:
- [ ] T016 [P] [US2] Import "Orbitron" font into `docusaurus-book-site/src/css/custom.css`.
- [ ] T017 [P] [US2] Import "Inter" and "Roboto" fonts into `docusaurus-book-site/src/css/custom.css`.
- [ ] T018 [P] [US2] Import "JetBrains Mono" font into `docusaurus-book-site/src/css/custom.css`.
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all content display)
3.  Complete Phase 3: User Story 1 (Basic content display and navigation)
4.  **STOP and VALIDATE**: Test User Story 1 independently. The book content should be viewable.

### Incremental Delivery

1.  Complete Setup + Foundational → Docusaurus project initialized and content integrated.
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP for content viewing!)
3.  Add User Story 2 → Test independently → Deploy/Demo (Themed website!)
4.  Each story adds significant value.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    *   Developer A: User Story 1 (Verify content integration and basic navigation).
    *   Developer B: User Story 2 (Focus on UI/UX theming).
3.  Stories complete and integrate independently.

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tasks by running Docusaurus locally (`npm start`) and visually inspecting.
-   Commit after each task or logical group.
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence.
