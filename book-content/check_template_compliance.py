import os
import re

def check_template_compliance(book_content_root):
    errors = []
    
    expected_sections = [
        "Introduction",
        "Theory",
        "Code Examples",
        "Simulation Exercises",
        "Summary"
    ]
    
    # Regex to find sections (assuming Markdown H2 headings)
    section_pattern = re.compile(r'^##\s*(.*?)\s*$', re.MULTILINE)

    modules_dir = os.path.join(book_content_root, 'modules')
    if os.path.exists(modules_dir):
        for root, _, files in os.walk(modules_dir):
            for file in files:
                if file.endswith('.mdx'):
                    mdx_path = os.path.join(root, file)
                    with open(mdx_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    found_sections = [match.group(1) for match in section_pattern.finditer(content)]
                    
                    missing_sections = [s for s in expected_sections if s not in found_sections]
                    
                    if missing_sections:
                        errors.append(f"❌ {mdx_path} - Missing expected sections: {', '.join(missing_sections)}")
                    else:
                        print(f"✅ {mdx_path} - Template compliance valid")
    
    if errors:
        print("\n--- Template Compliance Check Summary ---")
        for error in errors:
            print(error)
        print(f"\nTotal template compliance errors: {len(errors)}")
        return False
    else:
        print("\nAll chapters comply with the template structure!")
        return True

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    book_content_root = os.path.abspath(script_dir) # Should be book-content/ 

    print(f"Starting template compliance check in: {book_content_root}")
    success = check_template_compliance(book_content_root)
    if not success:
        exit(1)
