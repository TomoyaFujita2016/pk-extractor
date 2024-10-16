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
