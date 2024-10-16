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
                ignore_count += sum([len(files) for _, _, files in os.walk(dirpath)])
                pbar.update(len(filenames))
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

    log.info(f"Total files: {total_files}.")
    log.info(f"Ignored {ignore_count} files.")
    log.info(f"Processed {content_count} files.")

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# Project structure\n\n")
            f.write("\n".join(structure))
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
