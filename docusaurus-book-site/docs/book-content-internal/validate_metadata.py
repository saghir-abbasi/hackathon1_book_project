import json
import os
import re
from jsonschema import validate, ValidationError

def load_schema(schema_path):
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_front_matter(mdx_content):
    match = re.match(r'---\n(.*?)\n---', mdx_content, re.DOTALL)
    if match:
        front_matter_str = match.group(1)
        # Basic YAML to JSON conversion for front matter (simplified)
        # This is a very basic parsing; a proper YAML parser would be better.
        data = {}
        for line in front_matter_str.split('\n'):
            line = line.strip()
            if ': ' in line:
                key, value = line.split(': ', 1)
                key = key.strip()
                value = value.strip()
                # Attempt to convert basic types
                if value.startswith('"') and value.endswith('"'):
                    data[key] = value[1:-1]
                elif value.lower() == 'true':
                    data[key] = True
                elif value.lower() == 'false':
                    data[key] = False
                elif value.isdigit():
                    data[key] = int(value)
                elif value.startswith('[') and value.endswith(']'):
                    data[key] = [item.strip().strip('"') for item in value[1:-1].split(',') if item.strip()]
                elif value.startswith('{') and value.endswith('}'):
                    # Simple object parsing
                    obj_data = {}
                    for item in value[1:-1].split(','):
                        if ': ' in item:
                            k, v = item.split(': ', 1)
                            obj_data[k.strip().strip('"')] = v.strip().strip('"')
                    data[key] = obj_data
                else:
                    data[key] = value
            elif line.startswith('- ') and data: # Array item for last key
                last_key = list(data.keys())[-1]
                if isinstance(data[last_key], list):
                    data[last_key].append(line[2:].strip())
        return data
    return None

def validate_metadata(book_content_root):
    chapter_schema = load_schema(os.path.join(book_content_root, 'metadata', 'chapter-schemas', 'chapter-schema.json'))
    module_schema = load_schema(os.path.join(book_content_root, 'metadata', 'module-schemas', 'module-schema.json'))

    errors = []

    # Validate module _index.json files
    modules_dir = os.path.join(book_content_root, 'modules')
    if os.path.exists(modules_dir):
        for module_name in os.listdir(modules_dir):
            module_path = os.path.join(modules_dir, module_name)
            if os.path.isdir(module_path):
                index_json_path = os.path.join(module_path, '_index.json')
                if os.path.exists(index_json_path):
                    try:
                        module_metadata = load_schema(index_json_path)
                        validate(instance=module_metadata, schema=module_schema)
                        print(f"✅ {index_json_path} - Valid")
                    except ValidationError as e:
                        errors.append(f"❌ {index_json_path} - Invalid: {e.message}")
                    except json.JSONDecodeError:
                        errors.append(f"❌ {index_json_path} - Invalid JSON format")
                else:
                    errors.append(f"❌ {module_path} - Missing _index.json")

    # Validate chapter .mdx front-matter
    for root, _, files in os.walk(modules_dir):
        for file in files:
            if file.endswith('.mdx'):
                mdx_path = os.path.join(root, file)
                with open(mdx_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                front_matter = extract_front_matter(content)
                if front_matter:
                    try:
                        validate(instance=front_matter, schema=chapter_schema)
                        print(f"✅ {mdx_path} - Front-matter Valid")
                    except ValidationError as e:
                        errors.append(f"❌ {mdx_path} - Front-matter Invalid: {e.message}")
                    except Exception as e:
                        errors.append(f"❌ {mdx_path} - Front-matter Parsing/Validation Error: {e}")
                else:
                    errors.append(f"❌ {mdx_path} - Missing or invalid front-matter")

    if errors:
        print("\n--- Validation Summary ---")
        for error in errors:
            print(error)
        print(f"\nTotal errors: {len(errors)}")
        return False
    else:
        print("\nAll metadata validated successfully!")
        return True

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    book_content_root = os.path.abspath(script_dir)
    
    print(f"Starting metadata validation in: {book_content_root}")
    success = validate_metadata(book_content_root)
    if not success:
        exit(1)
