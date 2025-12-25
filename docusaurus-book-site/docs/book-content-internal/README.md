---
displayed_sidebar: null
sidebar_class_name: hidden
---

# Book Content - Authoring Guidelines

This directory contains all the content for the "Physical AI & Humanoid Robotics" book. It is structured to be modular, maintainable, and compatible with static-site generators like Docusaurus (though Docusaurus integration is handled downstream).

## Structure Overview

-   `book-content/modules/`: Contains subdirectories for each module (e.g., `module-1-ros2/`), which in turn hold individual chapter `.mdx` files and a module-level `_index.json` metadata file.
-   `book-content/shared/`: Contains reusable assets and templates:
    -   `templates/`: Standardized templates for chapters, code snippets, etc.
    -   `diagrams/`: Image files for diagrams.
    -   `code-snippets/`: Standalone code files referenced in chapters.
-   `book-content/metadata/`: Contains JSON schemas for validating chapter and module metadata.

## Authoring a New Chapter

1.  **Locate Module**: Navigate to the appropriate module directory (e.g., `book-content/modules/module-1-ros2/`).
2.  **Copy Template**: Copy `book-content/shared/templates/chapter-template.mdx` to your module directory and rename it (e.g., `chapter-new-topic.mdx`).
3.  **Fill Front-Matter**: Update the YAML front-matter section at the top of the `.mdx` file.
    *   **Refer to**: `book-content/metadata/chapter-schemas/chapter-schema.json` for required fields and data types.
    *   Ensure `id`, `title`, `module`, `order`, `difficulty`, `prerequisites`, `tags`, and `languageVariants` are correctly filled.
    *   `module` should match the `id` from the parent module's `_index.json`.
4.  **Write Content**: Fill in the `Introduction`, `Theory`, `Code Examples`, `Simulation Exercises`, and `Summary` sections.
    *   **Adhere to Writing Rules**:
        *   Use clear, concise language.
        *   Break down complex topics into digestible sections.
        *   Use standard Markdown/MDX syntax.
        *   **CRITICAL**: Do NOT include Docusaurus-specific UI components or complex rendering logic directly in the `.mdx` files. The content should remain pure and portable.
    *   **Code Snippets**: For code examples longer than a few lines, consider placing them in `book-content/shared/code-snippets/` and referencing them from your chapter. Use the `code-snippet-template.mdx` for guidance on formatting.
    *   **Simulation Exercises**: Structure exercises using the guidance in `simulation-exercise-template.mdx`.
    *   **Glossary Terms**: If defining new terms, consider using `glossary-template.mdx` for consistency.
5.  **Asset References**: Place diagrams in `book-content/shared/diagrams/` and update `assetReferences` in chapter front-matter if new assets are used.
6.  **Internal Links**: Use standard Markdown `[Link Text](path/to/other-chapter.mdx)` for cross-linking chapters. Ensure paths are relative and correct.

## Module Metadata (`_index.json`)

Each module directory contains an `_index.json` file.
*   **Refer to**: `book-content/metadata/module-schemas/module-schema.json` for required fields.
*   Ensure `id`, `title`, `order`, and `description` are correctly filled.

## Asset Organization

Assets (diagrams, code snippets) should be organized as follows:

-   **Diagrams**: Place all image files (e.g., `.svg`, `.png`, `.jpg`) for diagrams in the `book-content/shared/diagrams/` directory. Reference them in your `.mdx` files using relative paths from the `book-content/` root (e.g., `![Alt Text](/shared/diagrams/my-diagram.svg)`).
-   **Code Snippets**: For standalone code files, place them in the `book-content/shared/code-snippets/` directory. Reference them in your `.mdx` files either directly or by embedding their content using a mechanism supported by MDX (e.g., import statements or specific plugins that will be configured later in Docusaurus). Ensure file extensions are appropriate (e.g., `.py`, `.cpp`, `.xml`).

## Internal Link Planning

When creating internal links (cross-chapter references):
-   Use relative paths to the target `.mdx` file.
-   The link text should be descriptive.
-   Example: `[Introduction to ROS 2 Nodes and Topics](../module-1-robotic-nervous-system/chapter-1-ros2-basics.mdx)`

## Content Validation

Before committing, ensure your content passes validation checks:
*   **Metadata Validation**: Check chapter front-matter and module `_index.json` files against their respective JSON schemas. Run `python validate_metadata.py`.
*   **Internal Link Checking**: Verify all internal links within `.mdx` files are valid. Run `python check_links.py`.
*   **Template Compliance**: Ensure chapters adhere to the expected structure defined by `chapter-template.mdx`. Run `python check_template_compliance.py`.
*   **File Structure Enforcement**: Confirm the content follows the `book-content/` hierarchy. Run `python check_structure.py`.

A combined validation script `validate-content.ps1` is available in the `book-content/` root to run all checks.

## Contribution

Please ensure all changes are reviewed for accuracy, clarity, and adherence to these guidelines.
