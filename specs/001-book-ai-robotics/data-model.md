# Data Model for Physical AI & Humanoid Robotics Book Content

## Entities:

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

## Relationships:

-   Book has many Modules (one-to-many).
-   Module has many Chapters (one-to-many).
-   Chapters can reference other Chapters or Modules (many-to-many for `prerequisites` and `relatedModules` via `id` references).