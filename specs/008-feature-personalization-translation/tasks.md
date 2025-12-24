# Tasks: Personalization & Translation UI

**Feature Branch**: `008-feature-personalization-translation`
**Date**: 2025-12-22
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Summary

This document outlines the actionable, dependency-ordered tasks for implementing the "Personalization & Translation UI" feature. Tasks are organized by user story to enable independent implementation and testing.

## Dependency Graph (User Story Completion Order)

```
Phase 1: Setup
    ↓
Phase 2: Foundational (useUserPreferences hook + base components)
    ↓
    ├── US1: Personalize Content (can start after Phase 2)
    │
    └── US2: Translate to Urdu (can start after Phase 2, parallel with US1)
    ↓
Phase 5: Polish & Integration
```

## Parallel Execution Opportunities

- **Phase 2**: T004 and T005 can run in parallel (different files)
- **US1 & US2**: Can be implemented in parallel after Phase 2 (independent features)
- **Within US1**: T008, T009, T010 can run in parallel (different components)
- **Within US2**: T014 and T015 can run in parallel (different files)

## Implementation Strategy

**MVP-First Approach**: Complete US1 (Personalization) first for core value, then add US2 (Translation).

---

## Phase 1: Setup

- [x] T001 Add Noto Nastaliq Urdu font to `docusaurus-book-site/docusaurus.config.ts` headTags for Urdu RTL support
- [x] T002 Create directory structure `docusaurus-book-site/src/components/ChapterToolbar/`
- [x] T003 Create directory `docusaurus-book-site/src/hooks/` if not exists

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Create shared hooks and types needed by both user stories.

- [x] T004 [P] Create `useUserPreferences.ts` hook in `docusaurus-book-site/src/hooks/useUserPreferences.ts` implementing UserPreferences interface with localStorage read/write
- [x] T005 [P] Create TypeScript types file `docusaurus-book-site/src/components/ChapterToolbar/types.ts` with TransformationState, ChapterMetadata, and ContentTransformRequest interfaces
- [x] T006 Swizzle DocItem/Layout by running `npm run swizzle @docusaurus/theme-classic DocItem/Layout -- --wrap --typescript` and modify `docusaurus-book-site/src/theme/DocItem/Layout/index.tsx` to wrap children with ChapterToolbar
- [x] T007 Create base `ChapterToolbar/index.tsx` component in `docusaurus-book-site/src/components/ChapterToolbar/index.tsx` that renders toolbar container with slots for buttons

---

## Phase 3: User Story 1 - Personalize Content (Priority: P1)

**Goal**: As a user, I want to click a "Personalize" button to adapt the chapter content to my background (Software or Hardware), so that the explanations are more relevant to my expertise.

**Independent Test**: Click Personalize button on any chapter → select background → verify content is rewritten with background-specific analogies.

### UI Components

- [x] T008 [P] [US1] Create `BackgroundModal.tsx` component in `docusaurus-book-site/src/components/ChapterToolbar/BackgroundModal.tsx` with Software/Hardware selection options and confirm button
- [x] T009 [P] [US1] Create `PersonalizeButton.tsx` component in `docusaurus-book-site/src/components/ChapterToolbar/PersonalizeButton.tsx` with neon-themed button that checks useUserPreferences and shows modal if background not set
- [x] T010 [P] [US1] Create `ContentOverlay.tsx` component in `docusaurus-book-site/src/components/ChapterToolbar/ContentOverlay.tsx` to display streaming transformed content with close button and loading state

### Styling

- [x] T011 [US1] Create `styles.module.css` in `docusaurus-book-site/src/components/ChapterToolbar/styles.module.css` with robotics/neon theme for toolbar, buttons, modal, and overlay

### Agent Integration

- [x] T012 [US1] Implement personalization logic in `PersonalizeButton.tsx` that extracts chapter content, builds PERSONALIZE_SOFTWARE_PROMPT or PERSONALIZE_HARDWARE_PROMPT, and calls AgentBridge.sendChatMessage with streaming callbacks
- [x] T013 [US1] Integrate PersonalizeButton and ContentOverlay into ChapterToolbar/index.tsx, managing TransformationState

---

## Phase 4: User Story 2 - Translate to Urdu (Priority: P1)

**Goal**: As a user, I want to click a "Translate to Urdu" button, so that I can read the chapter content in Urdu.

**Independent Test**: Click "اردو میں ترجمہ" button on any chapter → verify Urdu translation streams in RTL format.

### UI Components

- [x] T014 [P] [US2] Create `TranslateButton.tsx` component in `docusaurus-book-site/src/components/ChapterToolbar/TranslateButton.tsx` with Urdu label "اردو میں ترجمہ" and neon styling
- [x] T015 [P] [US2] Add RTL styling to `styles.module.css` for `.urdu-content` class with `direction: rtl`, Noto Nastaliq Urdu font, and appropriate line-height

### Agent Integration

- [x] T016 [US2] Implement translation logic in `TranslateButton.tsx` that extracts chapter content, builds TRANSLATE_URDU_PROMPT, and calls AgentBridge.sendChatMessage with streaming callbacks
- [x] T017 [US2] Update ContentOverlay.tsx to detect Urdu content and apply RTL styling class
- [x] T018 [US2] Integrate TranslateButton into ChapterToolbar/index.tsx

---

## Phase 5: Polish & Cross-Cutting Concerns

- [x] T019 Add loading spinner animation to ContentOverlay while status is 'loading' or 'streaming'
- [x] T020 Add error handling UI to ContentOverlay showing error message with retry button
- [x] T021 Add keyboard accessibility (Escape to close overlay, Enter to confirm modal)
- [ ] T022 Update `specs/008-feature-personalization-translation/quickstart.md` with final testing checklist
- [ ] T023 Manual end-to-end testing: Personalization flow (Software background)
- [ ] T024 Manual end-to-end testing: Personalization flow (Hardware background)
- [ ] T025 Manual end-to-end testing: Translation flow (Urdu)
- [ ] T026 Manual end-to-end testing: Preference persistence across page reloads
- [ ] T027 Mobile responsiveness testing for toolbar and overlay

---

## Task Summary

| Phase | Tasks | Parallelizable |
|-------|-------|----------------|
| Setup | 3 | 0 |
| Foundational | 4 | 2 |
| US1: Personalize | 6 | 3 |
| US2: Translate | 5 | 2 |
| Polish | 9 | 0 |
| **Total** | **27** | **7** |

## MVP Scope

**Recommended MVP**: Complete Phase 1-3 (Setup + Foundational + US1 Personalization)
- Delivers core value: Content personalization based on user background
- 13 tasks total for MVP
- US2 (Translation) can be added incrementally after MVP validation
