# Project structure

```
pk-extractor/
│   pyproject.toml
│   .gitignore
│   README.md
│   .flake8
│   LICENCE
├── tests/
├── │   __init__.py
├── .github/
│   ├── workflows/
│   ├── │   publish.yml
├── pk_extractor/
├── │   __init__.py
├── │   logger.py
├── │   generator.py
├── │   cli.py```



# File contents

- /pyproject.toml
```
[tool.poetry]
name = "pk-extractor"
version = "0.2.1"
description = "Project Knowledge Extractor"
authors = ["TomoyaFujita2016 <fujita.t.2016c@gmail.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"
gitignore-parser = "^0.1.11"
tqdm = "^4.66.5"

[tool.poetry.group.dev.dependencies]
black = "^24.10.0"
flake8 = "^7.1.1"
isort = "^5.13.2"
mypy = "^1.12.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"


[tool.poetry.scripts]
generate = "pk_extractor.cli:main"
```

- /.gitignore
```
__pycache__/
.venv/
.mypy_cache/
poetry.lock
```

- /README.md
```
# pk-extractor

pk-extractor (Project Knowledge Extractor) is a tool that generates a comprehensive knowledge base from a given repository, including the project structure and file contents. It respects `.gitignore` rules and allows for additional exclusion patterns.

## Features

- Generates a markdown file containing the project structure and file contents
- Respects `.gitignore` rules
- Allows for additional file/directory exclusion via command-line arguments
- Provides progress information during processing
- Handles binary files and errors gracefully

## Installation

You can install pk-extractor using pip:

```
pip install pk-extractor
```

```
poetry add pk-extractor
```


## Usage

After installation, you can run pk-extractor from the command line:

```
pk-extractor <root_dir> [--output_file OUTPUT_FILE] [--exclude [EXCLUDE [EXCLUDE ...]]]
```

or

```
pipx run pk-extractor <root_dir> [--output_file OUTPUT_FILE] [--exclude [EXCLUDE [EXCLUDE ...]]]
```

### Arguments:

- `root_dir`: Path to the repository you want to analyze (required)
- `--output_file`: Path to the output file (default: "knowledge.md")
- `--exclude`: Patterns to exclude (e.g., "*.pyc" "venv/*")

### Examples:

1. Generate knowledge for a repository:
   ```
   pk-extractor /path/to/your/repo
   ```

2. Specify an output file:
   ```
   pk-extractor /path/to/your/repo --output_file my_knowledge.md
   ```

3. Exclude specific patterns:
   ```
   pk-extractor /path/to/your/repo --exclude "*.pyc" "venv/*" "*.log"
   ```


## Output

The script generates a markdown file containing:

1. Project structure
2. File contents

## Development

To set up the development environment:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/pk-extractor.git
   cd pk-extractor
   ```

2. Install dependencies:
   ```
   poetry install
   ```


Now you can run the tool or tests within this environment.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

- /.flake8
```
[flake8]
ignore = E226,E302,E41
max-line-length = 160
exclude = tests/*
max-complexity = 10
```

- /LICENCE
```
MIT License

Copyright (c) 2024 [TomoyaFujita2016]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- /tests/__init__.py
```

```

- /.github/workflows/publish.yml
```
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'  # タグが v で始まる場合にトリガー

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install poetry
    - name: Build package
      run: poetry build
    - name: Publish package
      uses: pypa/gh-action-pypi-publish@27b31702a0e7fc50959f5ad993c78deac1bdfc29
      with:
        user: __token__
        password: ${{ secrets.PYPI_API_TOKEN }}
```

- /pk_extractor/__init__.py
```

```

- /pk_extractor/logger.py
```
import os
from logging import DEBUG, Formatter, StreamHandler, getLogger

"""ロギング関係
"""

log = getLogger(__name__)
formatter = Formatter(
    "[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s"
)

handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(formatter)

log.addHandler(handler)
log.setLevel(DEBUG)
log.propagate = False
```

- /pk_extractor/generator.py
```
import os
from fnmatch import fnmatch
from pathlib import Path

from gitignore_parser import parse_gitignore
from tqdm import tqdm

from .logger import log


def get_gitignore_funcs(root_dir):
    gitignore_funcs = []
    for dirpath, _, filenames in os.walk(root_dir):
        if ".gitignore" in filenames:
            gitignore_path = os.path.join(dirpath, ".gitignore")
            try:
                ignore_func = parse_gitignore(gitignore_path)
                gitignore_funcs.append(ignore_func)
            except Exception as e:
                log.warning(f"Error parsing .gitignore at {gitignore_path}: {e}")
    return gitignore_funcs


def should_ignore(path, gitignore_funcs, root_dir, exclude_patterns):
    path = Path(path)
    if ".git" in path.parts:
        return True

    # Check exclude patterns
    for pattern in exclude_patterns:
        if fnmatch(str(path.relative_to(root_dir)), pattern):
            return True

    for ignore_func in gitignore_funcs:
        try:
            path = path.resolve()
            if ignore_func(path):
                return True
        except ValueError:
            pass
    return False


def generate_knowledge(root_dir, output_file, exclude_patterns=None):
    root_dir = Path(root_dir).resolve()
    gitignore_funcs = get_gitignore_funcs(root_dir)
    exclude_patterns = exclude_patterns or []
    structure = []
    file_contents = []
    content_count = 0
    ignore_count = 0

    total_files = sum([len(files) for _, _, files in os.walk(root_dir)])

    with tqdm(total=total_files, desc="Analyzing files", unit="file") as pbar:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirpath = Path(dirpath)
            rel_path = dirpath.relative_to(root_dir)

            if should_ignore(dirpath, gitignore_funcs, root_dir, exclude_patterns):
                _file_count = sum([len(files) for _, _, files in os.walk(dirpath)])
                ignore_count += _file_count
                pbar.update(_file_count)
                dirnames[:] = []
                continue

            level = len(rel_path.parts)
            indent = "│   " * (level - 1) + "├── " if level > 0 else ""
            structure.append(f"{indent}{dirpath.name}/")

            for filename in filenames:
                file_path = dirpath / filename
                if not should_ignore(
                    file_path, gitignore_funcs, root_dir, exclude_patterns
                ):
                    structure.append(f"{indent}│   {filename}")
                    content_count += 1
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        file_contents.append(
                            f"- /{file_path.relative_to(root_dir)}\n```\n{content.strip()}\n```"
                        )
                    except UnicodeDecodeError:
                        file_contents.append(
                            f"- /{file_path.relative_to(root_dir)}\n```\n[Binary file not shown]\n```"
                        )
                    except Exception as e:
                        log.error(f"Error reading file {file_path}: {e}")
                        file_contents.append(
                            f"- /{file_path.relative_to(root_dir)}\n```\n[Error reading file: {e}]\n```"
                        )
                else:
                    ignore_count += 1
                pbar.update(1)

    log.info(f"Processed {content_count} files.")
    log.info(f"{ignore_count} files were ignored.")

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# Project structure\n\n")
            f.write("```\n")
            f.write("\n".join(structure))
            f.write("```\n")
            f.write("\n\n\n")
            f.write("# File contents\n\n")
            f.write("\n\n".join(file_contents))
        log.info(f"Project knowledge generated and saved to `{output_file}`")
    except Exception as e:
        log.error(f"Error writing to output file {output_file}: {e}")

    return "\n".join(structure), "\n\n".join(file_contents)


if __name__ == "__main__":
    root_dir = "."
    output_file = "project_knowledge.md"

    structure, contents = generate_knowledge(root_dir, output_file)
    print("Project structure:")
    print(structure)
    print("\nFile contents have been saved to the output file.")
```

- /pk_extractor/cli.py
```
import argparse

from .generator import generate_knowledge
from .logger import log


def main():
    parser = argparse.ArgumentParser(description="Generate knowledge from a repository")
    parser.add_argument("root_dir", help="Path to the repository")
    parser.add_argument(
        "--output_file", help="Path to the output file", default="knowledge.md"
    )
    parser.add_argument(
        "--exclude", nargs="*", help='Patterns to exclude (e.g., "*.pyc" "venv/*")'
    )
    args = parser.parse_args()

    generate_knowledge(
        args.root_dir,
        args.output_file,
        args.exclude,
    )


if __name__ == "__main__":
    main()
```