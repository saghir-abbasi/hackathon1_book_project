# Implementation Plan: Physical AI & Humanoid Robotics Book Content

**Branch**: `001-book-ai-robotics` | **Date**: 2025-11-30 | **Spec**: [specs/001-book-ai-robotics/spec.md](specs/001-book-ai-robotics/spec.md)
**Input**: Feature specification from `/specs/001-book-ai-robotics/spec.md`

## Summary

This implementation plan details the creation of a dedicated content repository for the "Physical AI & Humanoid Robotics" course. The core objective is to produce clean, modular Markdown/MDX content structured around defined modules and chapters, incorporating rich metadata and reusable templates. The plan includes establishing a clear folder hierarchy, defining metadata schemas for chapters and modules, developing content templates, outlining content-generation workflows for each module, and specifying requirements for automated content validation checks. The output will be a fully validated content folder, ready for seamless integration with a Docusaurus static-site generator in a separate, downstream phase.

## Technical Context

**Language/Version**: Markdown, MDX (compatible with CommonMark and Docusaurus parsing)  
**Primary Dependencies**: Not applicable for content generation itself (focus is on raw content files). Future dependency: Docusaurus.  
**Storage**: Local Filesystem (Git repository)  
**Testing**: Custom validation scripts (e.g., PowerShell/Python for metadata, link checks, template compliance)  
**Target Platform**: Not applicable for content generation. Content is platform-agnostic Markdown/MDX.  
**Project Type**: Content repository / Documentation source  
**Performance Goals**: Efficient content authoring and automated validation (validation runtime < 5 minutes for full book).  
**Constraints**:
- Content files MUST NOT contain UI-specific components or Docusaurus-specific markup beyond standard MDX features.
- Content MUST be modular and reusable across potential future contexts (e.g., RAG chatbot).
- The scope is limited to content generation and validation; Docusaurus integration is explicitly out of scope for this plan.
**Scale/Scope**: 4 core modules, approximately 4-6 chapters per module (total 16-24 chapters), each with intro, theory, code, simulation, and summary sections. Comprehensive metadata for each chapter.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   **Article I — Library-First & Modular Design**: PASSED. The plan emphasizes modular content (modules, chapters, templates) with clear boundaries.
-   **Article II — Spec-Driven & Test-First Workflow**: PASSED. This plan is derived from a clear specification. It incorporates "automated checks" as a form of testing for content quality.
-   **Article III — Documentation, Content & Code Quality Standards**: PASSED. Explicitly defines structured chapter metadata, content boundaries, and writing rules that ensure readability and consistency.
-   **Article IV — Content & Deployment Standard (Book + UI)**: PASSED. Content is designed to be compatible with Docusaurus and static site generation, adhering to the principle of keeping core content static.
-   **Article V — RAG & AI Integrations: Privacy, Security & Data Handling**: N/A (Directly related to content creation, not RAG/AI integration logic at this stage). However, the metadata schema allows for personalization flags which aligns with future data handling needs.
-   **Article VI — Reusable Intelligence: Subagents & Agent Skills**: PASSED. Structured content, templates, and clear metadata facilitate future reuse by AI agents and subagents.
-   **Article VII — Internationalization & Personalization Support**: PASSED. The metadata schema explicitly includes language variants and personalization flags.
-   **Article VIII — Simplicity & Minimalism**: PASSED. The plan strictly focuses on content generation, avoiding premature optimization or integration details for Docusaurus.
-   **Article IX — Version Control, Release & Traceability**: PASSED. The entire content repository will be version-controlled.

## Project Structure

### Documentation (this feature)

```text
specs/001-book-ai-robotics/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (API schemas, if any - N/A for this content-focused plan)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
book-content/
├── modules/
│   ├── module-1-robotic-nervous-system/
│   │   ├── chapter-1-ros2-basics.mdx
│   │   ├── chapter-2-urdf-fundamentals.mdx
│   │   └── _index.json # Module metadata
│   ├── module-2-digital-twin/
│   │   ├── chapter-1-gazebo-physics.mdx
│   │   ├── chapter-2-unity-simulation.mdx
│   │   └── _index.json # Module metadata
│   ├── module-3-ai-robot-brain/
│   │   ├── chapter-1-isaac-sim-basics.mdx
│   │   ├── chapter-2-vslam-navigation.mdx
│   │   └── _index.json # Module metadata
│   └── module-4-vision-language-action/
│       ├── chapter-1-cognitive-planning.mdx
│       ├── chapter-2-whisper-integration.mdx
│       └── _index.json # Module metadata
├── shared/
│   ├── templates/
│   │   ├── chapter-template.mdx
│   │   ├── code-snippet-template.mdx
│   │   ├── simulation-exercise-template.mdx
│   │   └── glossary-template.mdx
│   ├── diagrams/
│   │   ├── diagram-1-ros-arch.svg
│   │   └── ...
│   └── code-snippets/
│       ├── ros2-publisher-py.txt
│       └── ...
├── metadata/
│   ├── chapter-schemas/
│   │   └── chapter-schema.json # JSON schema for chapter front-matter
│   └── module-schemas/
│       └── module-schema.json # JSON schema for module metadata
└── README.md # Explains content structure and authoring guidelines
```

**Structure Decision**: The "book-content/" directory will serve as the top-level container. Modules are organized into subdirectories (`modules/`), each containing their chapters and a module-level metadata file (`_index.json`). Shared assets (templates, diagrams, generic code snippets) are centralized under `shared/`. Dedicated `metadata/` directories will house JSON schemas for structural validation of chapter front-matter and module metadata. This structure is a custom single-project layout.

## Phase 0: Outline & Research

### Research Tasks

The plan for content generation is largely prescriptive based on the user's detailed request. There are no explicit "NEEDS CLARIFICATION" markers in the plan so far. The key technical choices (Markdown/MDX, Docusaurus compatibility) are well-defined as constraints or future integrations, not unknowns requiring research at this stage of content generation.

However, implicit research will be required during the definition of metadata schemas and templates:

1.  **Metadata Schema Best Practices**: Research best practices for defining robust and extensible JSON schemas for content metadata, particularly for Markdown/MDX front-matter. This includes exploring existing standards or patterns for technical book metadata.
    *   **Decision**: Will use JSON Schema Draft 2020-12 (or latest stable) for metadata definition.
    *   **Rationale**: Provides strong validation capabilities and is widely supported.
    *   **Alternatives considered**: YAML schemas (less strict validation, harder for programmatic parsing); custom parsing (high development overhead).

2.  **MDX Template Design**: Research effective ways to design MDX templates that are flexible, support various content types (code, simulation, glossary), and maintain content/presentation separation, while remaining compatible with a static site generator like Docusaurus without tightly coupling.
    *   **Decision**: Will use standard Markdown/MDX syntax for content and structure, with explicit comment markers (e.g., `<!-- section: code-example -->`) or custom MDX components for structured sections, defined later during Docusaurus integration.
    *   **Rationale**: Offers a balance of flexibility and structure, avoiding premature Docusaurus coupling.
    *   **Alternatives considered**: Over-reliance on Docusaurus-specific components (premature coupling); pure Markdown (less structured content).

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

This phase will focus on formalizing the content structure and metadata.

**Entities**:

1.  **Book**:
    *   Description: The entire collection of educational content.
    *   Attributes:
        *   `id`: string (unique identifier for the book)
        *   `title`: string (e.g., "Physical AI & Humanoid Robotics")
        *   `version`: string (e.g., "1.0.0")
        *   `authors`: array of strings
        *   `coverImage`: string (path to cover image asset)
        *   `description`: string (short summary of the book)
2.  **Module**:
    *   Description: A thematic grouping of chapters. Each module corresponds to a core area (e.g., Robotic Nervous System).
    *   Attributes (defined in `_index.json` within each module folder):
        *   `id`: string (e.g., `module-1-ros2`)
        *   `title`: string (e.g., "Robotic Nervous System")
        *   `order`: integer (sequential order of modules)
        *   `description`: string (short summary of the module)
        *   `prerequisites`: array of strings (e.g., "Basic Python", "Linear Algebra")
        *   `learningObjectives`: array of strings
3.  **Chapter**:
    *   Description: A fundamental unit of content within a module.
    *   Attributes (defined as front-matter in each chapter's `.mdx` file):
        *   `id`: string (e.g., `chapter-1-ros2-basics`)
        *   `title`: string (e.g., "Introduction to ROS 2 Nodes and Topics")
        *   `module`: string (reference to the parent module's `id`)
        *   `order`: integer (sequential order within its module)
        *   `difficulty`: enum (`beginner`, `intermediate`, `advanced`)
        *   `prerequisites`: array of strings (e.g., "Python Basics", "Module 1 - Chapter 1")
        *   `tags`: array of strings (e.g., "ROS2", "Robotics", "Fundamentals")
        *   `personalizationFlags`: object (key-value pairs for personalization, e.g., `{"background": "beginner-python"}`)
        *   `languageVariants`: array of strings (e.g., `["en", "ur"]`)
        *   `assetReferences`: array of strings (paths to diagrams, code snippets, etc., used in the chapter)
        *   `authors`: array of strings (if different from book authors)
        *   `version`: string (version of this specific chapter)
        *   `lastUpdated`: date (ISO 8601 format)

**Relationships**:
-   Book has many Modules (one-to-many).
-   Module has many Chapters (one-to-many).
-   Chapters can reference other Chapters or Modules (many-to-many for `prerequisites` and `relatedModules` via `id` references).

### API Contracts (`contracts/`)

Not applicable for this plan phase. This phase focuses purely on raw content and its structure. API contracts would be defined during a later phase when building a content-serving API or integrating with a backend.

### Quickstart Guide (`quickstart.md`)

This guide will provide instructions for setting up the content development environment, authoring new chapters, and running local validation checks.

**Outline**:
1.  **Setup**:
    *   Clone the repository.
    *   Install validation tools (e.g., Node.js for markdown-lint, Python for custom scripts).
2.  **Authoring a New Chapter**:
    *   Choose target module.
    *   Copy `shared/templates/chapter-template.mdx`.
    *   Fill in front-matter metadata (referencing `metadata/chapter-schemas/chapter-schema.json`).
    *   Write content, adhering to writing rules.
    *   Embed code snippets/diagrams using specified patterns.
3.  **Running Validation**:
    *   Command to validate metadata.
    *   Command to check internal links.
    *   Command to check template compliance.
    *   Command to verify file structure.

### Agent Context Update

The primary technology introduced in this phase is structured Markdown/MDX content with JSON Schemas for metadata validation. I will update the agent's context to reflect this new capability.

```text
# .specify/memory/constitution.md (excerpt)
# ... (existing content)
# Ensure to preserve this file manually. Do not overwrite.
```

## Task Breakdown

The plan outlines the following tasks, which will be detailed further in a `/sp.tasks` phase:

1.  **Define and implement JSON Schemas**:
    *   `chapter-schema.json`
    *   `module-schema.json`
2.  **Create content templates**:
    *   `chapter-template.mdx` (including sections for Intro, Theory, Code, Simulation, Summary)
    *   `code-snippet-template.mdx`
    *   `simulation-exercise-template.mdx`
    *   `glossary-template.mdx`
3.  **Establish content writing guidelines**:
    *   Detailed instructions for authors on content boundaries, Markdown/MDX usage, and metadata population.
4.  **Develop automated validation tools**:
    *   Script for metadata validation against schemas.
    *   Script for internal link checking (e.g., chapter-to-chapter, asset references).
    *   Script for template compliance (e.g., verifying presence of expected sections).
    *   Script for file structure enforcement.
5.  **Populate initial module/chapter content**:
    *   For each of the 4 modules, create placeholder `.mdx` and `_index.json` files, following templates and guidelines.
    *   Module 1: Robotic Nervous System (ROS 2 nodes, topics, services, URDF).
    *   Module 2: Digital Twin (Gazebo/Unity physics, sensors, digital twin modeling).
    *   Module 3: AI-Robot Brain (NVIDIA Isaac Sim, Isaac ROS, VSLAM, navigation stack).
    *   Module 4: Vision-Language-Action (Cognitive planning, Whisper examples).

## Risks and Constraints

*   **Risk**: Inconsistent application of metadata or templates by content authors.
    *   **Mitigation**: Robust automated validation checks and clear, concise authoring guidelines.
*   **Risk**: Over-engineering templates or metadata schemas, leading to complexity.
    *   **Mitigation**: Start with a minimal viable schema/template and iterate based on actual content needs, adhering to Simplicity & Minimalism constitution.
*   **Risk**: Misalignment with future Docusaurus integration requirements if not adequately considered.
    *   **Mitigation**: Regular review of Docusaurus best practices for Markdown/MDX content, ensuring pure content is always prioritized.
*   **Constraint**: Docusaurus integration is out of scope for this plan; content must be Docusaurus-agnostic where possible.
*   **Constraint**: No UI components or complex rendering logic within `.mdx` files.

## Final Deliverables and Acceptance Criteria

**Deliverables**:

1.  A `book-content/` directory at the repository root containing:
    *   `modules/` with 4 module subdirectories, each containing chapter `.mdx` files and `_index.json` metadata.
    *   `shared/` directory with `templates/`, `diagrams/`, and `code-snippets/` subdirectories.
    *   `metadata/` directory with `chapter-schemas/chapter-schema.json` and `module-schemas/module-schema.json`.
    *   `README.md` for content authoring guidelines.
2.  A set of automated scripts/tools for content validation.

**Acceptance Criteria**:

1.  All `.mdx` chapters and `_index.json` module files in `book-content/` adhere to their respective JSON schemas without validation errors.
2.  Automated checks report no broken internal references within the content (e.g., links to other chapters, asset paths).
3.  All chapters utilize the defined templates and include all mandatory sections (Intro, Theory, Code, Simulation, Summary).
4.  The `book-content/` directory structure strictly follows the proposed hierarchy.
5.  All content files (Markdown/MDX) are free of Docusaurus-specific UI components or markup, ensuring portability.