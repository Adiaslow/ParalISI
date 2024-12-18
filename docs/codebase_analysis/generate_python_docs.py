#
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

def generate_documentation(directory: str, output_file: str = 'docs/codebase_analysis/python_codebase_summary.md'):
    """Generate documentation for all Python files in the directory."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Track total files and functions for summary
    total_files = 0
    total_functions = 0

    # Generate the main content first
    main_content = []

    # Walk through directory
    for root, _, files in os.walk(directory):
        python_files = [f for f in files if f.endswith('.py')]

        if python_files:
            rel_path = os.path.relpath(root, directory)
            section_header = "\n## Root Directory\n\n" if rel_path == '.' else f"\n## Directory: {rel_path}\n\n"
            main_content.append(section_header)

            for file in sorted(python_files):
                total_files += 1
                file_path = Path(root) / file
                info = extract_python_info(file_path)
                total_functions += len(info['functions'])

                # Write file information
                main_content.append(f"### {file}")
                main_content.append("**File Statistics:**")
                main_content.append(f"- Total lines: {info['total_lines']}")
                main_content.append(f"- Non-empty lines: {info['non_empty_lines']}")
                main_content.append(f"- Number of functions: {len(info['functions'])}")
                main_content.append("")

                # Write header comments if they exist
                if info['header_comment']:
                    main_content.append("**File Description:**")
                    main_content.extend(info['header_comment'])
                    main_content.append("")

                # Write function definitions
                if info['functions']:
                    main_content.append("**Functions:**")
                    main_content.append("```python")
                    for func in info['functions']:
                        main_content.append(f"def {func}")
                    main_content.append("```")

                main_content.append("---")
                main_content.append("")

    # Create the complete document structure
    document_parts = [
        "# Python Codebase Summary",
        "",
        f"Generated on: {timestamp}",
        "",
        "## Summary Statistics",
        f"- Total Python files: {total_files}",
        f"- Total functions: {total_functions}",
        "",
        "---",
        "",
        *main_content
    ]

    # Write everything to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(document_parts))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_python_directory>")
        sys.exit(1)

    directory = sys.argv[1]
    generate_documentation(directory)
    print("Documentation generated in 'python_codebase_summary.md'")
