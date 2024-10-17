# pk-extractor

pk-extractor (Project Knowledge Extractor) is a tool that generates a comprehensive knowledge base from a given repository, including the project structure and file contents. It respects `.gitignore` rules and allows for additional exclusion patterns.

## Features

- Generates a markdown file containing the project structure and file contents
- Respects `.gitignore` rules
- Allows for additional file/directory exclusion via command-line arguments
- Provides progress information during processing
- Handles binary files and errors gracefully


## Easy to use
1. Install the package globally
```
$ pip install pk-extractor
$ pk-extractor .

```

2. Using pipx
```
$ pipx run pk-extractor .
```


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
