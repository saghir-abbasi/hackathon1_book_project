# Tasks: Physical AI & Humanoid Robotics Book Content

**Input**: Design documents from `specs/001-book-ai-robotics/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Content Repository Initialization)

**Purpose**: Establish the top-level content directory and core structural components.

- [x] T001 Create the top-level content directory `book-content/` at the repository root.
- [x] T002 Create the `book-content/modules/` directory.
- [x] T003 Create the `book-content/shared/` directory.
- [x] T004 Create the `book-content/metadata/` directory.
- [x] T005 Create the `book-content/shared/templates/` directory for content templates.
- [x] T006 Create the `book-content/shared/diagrams/` directory for diagrams.
- [x] T007 Create the `book-content/shared/code-snippets/` directory for code snippets.
- [x] T008 Create the `book-content/metadata/chapter-schemas/` directory for chapter metadata schemas.
- [x] T009 Create the `book-content/metadata/module-schemas/` directory for module metadata schemas.

---

## Phase 2: Foundational (Schemas & Templates)

**Purpose**: Define the structural integrity of content through JSON schemas and create reusable content templates. This phase MUST be completed before any module or chapter content can be created.

**⚠️ CRITICAL**: No content creation can begin until this phase is complete.

- [x] T010 [P] Define `chapter-schema.json` for chapter front-matter metadata based on `data-model.md` in `book-content/metadata/chapter-schemas/chapter-schema.json`.
- [x] T011 [P] Define `module-schema.json` for module metadata (`_index.json`) based on `data-model.md` in `book-content/metadata/module-schemas/module-schema.json`.
- [x] T012 [P] Create `chapter-template.mdx` with sections for Intro, Theory, Code, Simulation, Summary in `book-content/shared/templates/chapter-template.mdx`.
- [x] T013 [P] Create `code-snippet-template.mdx` for standardized code blocks in `book-content/shared/templates/code-snippet-template.mdx`.
- [x] T014 [P] Create `simulation-exercise-template.mdx` for simulation exercises in `book-content/shared/templates/simulation-exercise-template.mdx`.
- [x] T015 [P] Create `glossary-template.mdx` for glossary/definitions in `book-content/shared/templates/glossary-template.mdx`.
- [x] T016 Create `book-content/README.md` with initial content authoring guidelines, referencing schemas and templates.

**Checkpoint**: Core content structure and tools are defined.

---

## Phase 3: User Story 1 - Read a Chapter Linearly (P1) 🎯 MVP

**Goal**: Enable a reader to navigate and read the content of the book chapter by chapter in a linear fashion.

**Independent Test**: Verify that placeholder chapters for Module 1 can be accessed sequentially, and "next/previous" navigation would logically follow.

### Implementation for User Story 1 (Module 1 Content)

- [x] T017 [P] [US1] Create `book-content/modules/module-1-robotic-nervous-system/` directory.
- [x] T018 [P] [US1] Create `book-content/modules/module-1-robotic-nervous-system/_index.json` with metadata.
- [x] T019 [P] [US1] Draft `chapter-1-ros2-basics.mdx` using `chapter-template.mdx` in `book-content/modules/module-1-robotic-nervous-system/chapter-1-ros2-basics.mdx`.
- [x] T020 [P] [US1] Draft `chapter-2-urdf-fundamentals.mdx` using `chapter-template.mdx` in `book-content/modules/module-1-robotic-nervous-system/chapter-2-urdf-fundamentals.mdx`.

**Checkpoint**: User Story 1 content (Module 1 basics) is present and structured for linear reading.

---

## Phase 4: User Story 2 - Explore Content via Table of Contents (P1)

**Goal**: Allow a reader to quickly find and jump to specific chapters or sections using a table of contents.

**Independent Test**: Verify that all created modules and chapters are discoverable and linkable through a hierarchical structure (represented by metadata).

### Implementation for User Story 2 (Module 2 Content)

- [x] T021 [P] [US2] Create `book-content/modules/module-2-digital-twin/` directory.
- [x] T022 [P] [US2] Create `book-content/modules/module-2-digital-twin/_index.json` with metadata.
- [x] T023 [P] [US2] Draft `chapter-1-gazebo-physics.mdx` using `chapter-template.mdx` in `book-content/modules/module-2-digital-twin/chapter-1-gazebo-physics.mdx`.
- [x] T024 [P] [US2] Draft `chapter-2-unity-simulation.mdx` using `chapter-template.mdx` in `book-content/modules/module-2-digital-twin/chapter-2-unity-simulation.mdx`.
- [x] T025 [P] [US2] Review all `_index.json` files to ensure they contain necessary `order` attributes for hierarchical navigation.

**Checkpoint**: User Story 2 content (Module 2 basics) is present and metadata supports TOC generation.

---

## Phase 5: User Story 3 - Group Chapters by Module (P2)

**Goal**: Present chapters grouped by their respective modules to highlight thematic organization.

**Independent Test**: Verify that module-level metadata and chapter metadata are correctly linked, and chapters are logically grouped under their module.

### Implementation for User Story 3 (Module 3 & 4 Content)

- [x] T026 [P] [US3] Create `book-content/modules/module-3-ai-robot-brain/` directory.
- [x] T027 [P] [US3] Create `book-content/modules/module-3-ai-robot-brain/_index.json` with metadata.
- [x] T028 [P] [US3] Draft `chapter-1-isaac-sim-basics.mdx` using `chapter-template.mdx` in `book-content/modules/module-3-ai-robot-brain/chapter-1-isaac-sim-basics.mdx`.
- [x] T029 [P] [US3] Draft `chapter-2-vslam-navigation.mdx` using `chapter-template.mdx` in `book-content/modules/module-3-ai-robot-brain/chapter-2-vslam-navigation.mdx`.
- [x] T030 [P] [US3] Create `book-content/modules/module-4-vision-language-action/` directory.
- [x] T031 [P] [US3] Create `book-content/modules/module-4-vision-language-action/_index.json` with metadata.
- [x] T032 [P] [US3] Draft `chapter-1-cognitive-planning.mdx` using `chapter-template.mdx` in `book-content/modules/module-4-vision-language-action/chapter-1-cognitive-planning.mdx`.
- [x] T033 [P] [US3] Draft `chapter-2-whisper-integration.mdx` using `chapter-template.mdx` in `book-content/modules/module-4-vision-language-action/chapter-2-whisper-integration.mdx`.
- [x] T034 [P] [US3] Review all `_index.json` and chapter `.mdx` files for consistent module linking and ordering.

**Checkpoint**: All core modules and initial chapter content are in place, with metadata to support grouping.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Ensure overall content quality, validation, and readiness for downstream integration.

- [x] T035 Develop and implement metadata validation script using `book-content/metadata/chapter-schemas/chapter-schema.json` and `book-content/metadata/module-schemas/module-schema.json`.
- [x] T036 Develop and implement internal link checking script for all `.mdx` files.
- [x] T037 Develop and implement template compliance checking script (verifying presence of expected sections in `.mdx`).
- [x] T038 Develop and implement file structure enforcement script for `book-content/`.
- [x] T039 Integrate all validation scripts into a single `validate-content.ps1` (or similar) script.
- [x] T040 Write detailed content guidelines section in `book-content/README.md` including asset organization rules.
- [x] T041 Organize initial placeholder assets in `book-content/shared/diagrams/` and `book-content/shared/code-snippets/`.
- [x] T042 Conduct a final review of all content files for consistency, clarity, and adherence to writing rules.
- [x] T043 Verify that the entire `book-content/` folder is clean and modular, ready for Docusaurus integration.

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately.
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
-   **User Stories (Phase 3+)**: All depend on Foundational phase completion.
    -   User Story 1 (P1): Can proceed after Foundational.
    -   User Story 2 (P1): Can proceed after Foundational.
    -   User Story 3 (P2): Can proceed after Foundational.
-   **Polish (Final Phase)**: Depends on all user stories being complete.

### User Story Dependencies

-   **User Story 1 (P1)**: Can start after Foundational (Phase 2). No dependencies on other stories.
-   **User Story 2 (P1)**: Can start after Foundational (Phase 2). Integrates with US1's content.
-   **User Story 3 (P2)**: Can start after Foundational (Phase 2). Integrates with US1 and US2's content.

### Within Each User Story

-   Tasks should be performed in the listed order.
-   Drafting content for modules can happen in parallel.

### Parallel Opportunities

-   All Setup tasks (T001-T009) can run in parallel.
-   All Foundational tasks (T010-T015) can run in parallel.
-   Once Foundational phase completes, content drafting for different modules/chapters (T019-T020, T023-T024, T028-T029, T032-T033) can happen in parallel.
-   Review tasks (T025, T034) should be done after their respective content drafting.
-   All Polish phase tasks (T035-T038) involving script development can happen in parallel, leading to T039.
-   Asset organization (T041) can be done in parallel with other content tasks.

---

## Parallel Example: User Story 3 (Module 3 & 4 Content)

```bash
# Draft Module 3 chapters in parallel:
- [ ] T028 [P] [US3] Draft `chapter-1-isaac-sim-basics.mdx` using `chapter-template.mdx` in `book-content/modules/module-3-ai-robot-brain/chapter-1-isaac-sim-basics.mdx`.
- [ ] T029 [P] [US3] Draft `chapter-2-vslam-navigation.mdx` using `chapter-template.mdx` in `book-content/modules/module-3-ai-robot-brain/chapter-2-vslam-navigation.mdx`.

# Draft Module 4 chapters in parallel:
- [ ] T032 [P] [US3] Draft `chapter-1-cognitive-planning.mdx` using `chapter-template.mdx` in `book-content/modules/module-4-vision-language-action/chapter-1-cognitive-planning.mdx`.
- [ ] T033 [P] [US3] Draft `chapter-2-whisper-integration.mdx` using `chapter-template.mdx` in `book-content/modules/module-4-vision-language-action/chapter-2-whisper-integration.mdx`.
```

---

## Implementation Strategy

### MVP First (Module 1 Content)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all content creation)
3.  Complete Phase 3: User Story 1 (Module 1 content)
4.  **STOP and VALIDATE**: Run initial validation checks specifically on Module 1 content.

### Incremental Delivery

1.  Complete Setup + Foundational → Core content structure ready.
2.  Add User Story 1 (Module 1 content) → Test independently → Ready for review.
3.  Add User Story 2 (Module 2 content) → Test independently → Ready for review.
4.  Add User Story 3 (Module 3 & 4 content) → Test independently → Ready for review.
5.  Each story adds modular content without breaking previous structures.

### Parallel Team Strategy

With multiple content authors/developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    *   Content Author A: User Story 1 (Module 1 content)
    *   Content Author B: User Story 2 (Module 2 content)
    *   Content Author C: User Story 3 (Module 3 & 4 content)
    *   Developer D: Develop validation scripts (Final Phase tasks T035-T038).
3.  Content integrates and validates.

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tasks by manual review and automated validation scripts.
-   Commit after each task or logical group.
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence.
