import os

def check_file_structure(book_content_root):
    errors = []

    # Expected top-level directories
    expected_top_dirs = ['modules', 'shared', 'metadata']
    for dir_name in expected_top_dirs:
        path = os.path.join(book_content_root, dir_name)
        if not os.path.isdir(path):
            errors.append(f"❌ Missing top-level directory: {path}")

    # Expected shared subdirectories
    expected_shared_dirs = ['templates', 'diagrams', 'code-snippets']
    shared_path = os.path.join(book_content_root, 'shared')
    if os.path.isdir(shared_path):
        for dir_name in expected_shared_dirs:
            path = os.path.join(shared_path, dir_name)
            if not os.path.isdir(path):
                errors.append(f"❌ Missing shared subdirectory: {path}")
    
    # Expected metadata subdirectories
    expected_metadata_dirs = ['chapter-schemas', 'module-schemas']
    metadata_path = os.path.join(book_content_root, 'metadata')
    if os.path.isdir(metadata_path):
        for dir_name in expected_metadata_dirs:
            path = os.path.join(metadata_path, dir_name)
            if not os.path.isdir(path):
                errors.append(f"❌ Missing metadata subdirectory: {path}")

    # Check module structure
    modules_path = os.path.join(book_content_root, 'modules')
    if os.path.isdir(modules_path):
        for module_name in os.listdir(modules_path):
            module_dir = os.path.join(modules_path, module_name)
            if os.path.isdir(module_dir):
                # Check for _index.json
                index_json_path = os.path.join(module_dir, '_index.json')
                if not os.path.exists(index_json_path):
                    errors.append(f"❌ Module directory '{module_dir}' is missing _index.json")
                
                # Check for at least one .mdx chapter
                mdx_found = False
                for _, _, files in os.walk(module_dir):
                    for file in files:
                        if file.endswith('.mdx'):
                            mdx_found = True
                            break
                    if mdx_found:
                        break
                if not mdx_found:
                    errors.append(f"❌ Module directory '{module_dir}' contains no .mdx chapter files.")
    
    # Check for README.md in book-content root
    readme_path = os.path.join(book_content_root, 'README.md')
    if not os.path.exists(readme_path):
        errors.append(f"❌ Missing `book-content/README.md`")

    if errors:
        print("\n--- File Structure Check Summary ---")
        for error in errors:
            print(error)
        print(f"\nTotal structure errors: {len(errors)}")
        return False
    else:
        print("\nFile structure is compliant!")
        return True

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    book_content_root = os.path.abspath(script_dir) # Should be book-content/ 

    print(f"Starting file structure check in: {book_content_root}")
    success = check_file_structure(book_content_root)
    if not success:
        exit(1)
