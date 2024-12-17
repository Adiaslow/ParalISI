import os
from pathlib import Path
import datetime
import ast
from typing import Dict, Any

def extract_python_info(file_path: Path) -> Dict[str, Any]:
    """Extract relevant information from a Python file."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        lines = content.split('\n')

    info = {
        'functions': [],
        'total_lines': len(lines),
        'non_empty_lines': len([line for line in lines if line.strip()]),
        'header_comment': []
    }

    try:
        # Parse the Python file
        tree = ast.parse(content)

        # Get module docstring
        if ast.get_docstring(tree):
            info['header_comment'] = [line.strip() for line in ast.get_docstring(tree).split('\n')]

        # Extract function definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                info['functions'].append(node.name)

    except SyntaxError:
        pass
    except Exception:
        pass

    return info

def generate_documentation(directory: str, output_file: str = 'python_codebase_summary.md'):
    """Generate documentation for all Python files in the directory."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("# Python Codebase Summary\n\n")
        f.write(f"Generated on: {timestamp}\n\n")

        # Track total files and functions for summary
        total_files = 0
        total_functions = 0

        # Walk through directory
        for root, _, files in os.walk(directory):
            python_files = [f for f in files if f.endswith('.py')]

            if python_files:
                rel_path = os.path.relpath(root, directory)
                section_header = "\n## Root Directory\n\n" if rel_path == '.' else f"\n## Directory: {rel_path}\n\n"
                f.write(section_header)

                for file in sorted(python_files):
                    total_files += 1
                    file_path = Path(root) / file
                    info = extract_python_info(file_path)
                    total_functions += len(info['functions'])

                    # Write file information
                    f.write(f"### {file}\n")
                    f.write("**File Statistics:**\n")
                    f.write(f"- Total lines: {info['total_lines']}\n")
                    f.write(f"- Non-empty lines: {info['non_empty_lines']}\n")
                    f.write(f"- Number of functions: {len(info['functions'])}\n")

                    # Write header comments if they exist
                    if info['header_comment']:
                        f.write("**File Description:**\n")
                        f.write("\n".join(info['header_comment']))
                        f.write("\n")

                    # Write function definitions
                    if info['functions']:
                        f.write("**Functions:**\n```python\n")
                        for func in info['functions']:
                            f.write(f"def {func}\n")
                        f.write("```\n")

                    f.write("---\n\n")

        # Write summary statistics after first header
        summary = f"""## Summary Statistics
- Total Python files: {total_files}
- Total functions: {total_functions}

---
"""
        # Read the existing content
        with open(output_file, 'r') as original:
            content = original.read()

        # Write everything with summary inserted after the initial header
        with open(output_file, 'w') as final:
            parts = content.split('\n\n')
            final.write(f"{parts[0]}\n\n{parts[1]}\n\n{summary}")
            final.write('\n\n'.join(parts[2:]))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_python_directory>")
        sys.exit(1)

    directory = sys.argv[1]
    generate_documentation(directory)
    print("Documentation generated in 'python_codebase_summary.md'")
