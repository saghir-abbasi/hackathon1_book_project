import os
import re

def check_internal_links(book_content_root):
    errors = []
    
    # Regex to find Markdown links: [text](path)
    # This specifically looks for relative paths or paths starting with /
    # It might miss links that are purely external, which is fine for "internal" link check
    link_pattern = re.compile(r'\[.*?\]\((?!https?://)(.*?)\)')

    for root, _, files in os.walk(book_content_root):
        for file in files:
            if file.endswith('.mdx'):
                mdx_path = os.path.join(root, file)
                with open(mdx_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for match in link_pattern.finditer(content):
                    linked_path = match.group(1)
                    # Resolve path relative to the current MDX file
                    absolute_linked_path = os.path.abspath(os.path.join(os.path.dirname(mdx_path), linked_path))
                    
                    # Remove .mdx extension for checking directory existence if it's a chapter link
                    if linked_path.endswith('.mdx'):
                        check_path = absolute_linked_path
                    else:
                        check_path = absolute_linked_path # assuming internal links point to files
                    
                    if not os.path.exists(check_path):
                        errors.append(f"❌ {mdx_path}: Broken link '{linked_path}' (resolved to {check_path})")
    
    if errors:
        print("\n--- Internal Link Check Summary ---")
        for error in errors:
            print(error)
        print(f"\nTotal broken links: {len(errors)}")
        return False
    else:
        print("\nAll internal links are valid!")
        return True

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    book_content_root = os.path.abspath(script_dir) # Should be book-content/ 

    print(f"Starting internal link check in: {book_content_root}")
    success = check_internal_links(book_content_root)
    if not success:
        exit(1)
