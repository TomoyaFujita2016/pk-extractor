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
