import os
from pathlib import Path
import datetime

def extract_matlab_info(file_path):
    """Extract relevant information from a MATLAB file."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.readlines()

    # Remove empty lines and join remaining lines
    content_clean = [line.strip() for line in content if line.strip()]

    info = {
        'functions': [],
        'header_comment': [],
        'total_lines': len(content),
        'non_empty_lines': len(content_clean)
    }

    in_header = True
    for line in content_clean:
        # Collect header comments
        if in_header and line.startswith('%'):
            info['header_comment'].append(line[1:].strip())
        elif in_header and not line.startswith('%'):
            in_header = False

        # Collect function definitions
        if line.startswith('function'):
            info['functions'].append(line.strip())

    return info

def generate_documentation(directory, output_file='docs/codebase_analysis/matlab_codebase_summary.md'):
    """Generate documentation for all MATLAB files in the directory."""
    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("# MATLAB Codebase Summary\n\n")
        f.write(f"Generated on: {timestamp}\n\n")
        f.write(f"Base directory: {directory}\n\n")

        # Track total files for summary
        total_files = 0
        total_functions = 0

        # Walk through directory
        for root, _, files in os.walk(directory):
            matlab_files = [f for f in files if f.endswith('.m')]

            if matlab_files:
                # Get relative path for cleaner output
                rel_path = os.path.relpath(root, directory)
                if rel_path != '.':
                    f.write(f"\n## Directory: {rel_path}\n\n")
                else:
                    f.write("\n## Root Directory\n\n")

                for file in matlab_files:
                    total_files += 1
                    file_path = Path(root) / file
                    info = extract_matlab_info(file_path)
                    total_functions += len(info['functions'])

                    # Write file information
                    f.write(f"### {file}\n\n")

                    # Write file statistics
                    f.write("**File Statistics:**\n")
                    f.write(f"- Total lines: {info['total_lines']}\n")
                    f.write(f"- Non-empty lines: {info['non_empty_lines']}\n")
                    f.write(f"- Number of functions: {len(info['functions'])}\n\n")

                    # Write header comments if they exist
                    if info['header_comment']:
                        f.write("**File Description:**\n")
                        f.write("\n".join(info['header_comment']))
                        f.write("\n\n")

                    # Write function definitions
                    if info['functions']:
                        f.write("**Functions:**\n```matlab\n")
                        f.write("\n".join(info['functions']))
                        f.write("\n```\n\n")

                    f.write("---\n\n")

        # Write summary at the top
        with open(output_file, 'r') as original:
            content = original.read()

        summary = f"""
## Summary Statistics
- Total MATLAB files: {total_files}
- Total functions: {total_functions}

---
"""

        with open(output_file, 'w') as final:
            # Write everything with summary inserted after the initial header
            final.write(content.split('\n\n')[0] + '\n\n' + content.split('\n\n')[1] + '\n\n' + summary + '\n'.join(content.split('\n\n')[2:]))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_matlab_directory>")
        sys.exit(1)

    directory = sys.argv[1]
    generate_documentation(directory)
    print("Documentation generated in 'matlab_codebase_summary.md'")
