# Factorio Blueprint Editor

A modern Python tool for editing and manipulating Factorio blueprints.

## Features

- Built on top of the powerful `factorio-draftsman` library
- Type-safe blueprint manipulation
- Modern Python 3.13+ support
- Comprehensive test coverage

## Installation

```bash
# Clone the repository
git clone https://github.com/cbusillo/factorio-bp-editor.git
cd factorio-bp-editor

# Install with uv (recommended)
uv sync --dev

# Or install with pip
pip install -e ".[dev]"
```

## Usage

```python
from factorio_bp_editor import BlueprintEditor

# Example usage coming soon
```

## Development

This project uses:
- `uv` for dependency management
- `ruff` for linting and formatting
- `mypy` for type checking
- `pytest` for testing

```bash
# Run tests
pytest

# Format code
ruff format

# Lint code
ruff check

# Type check
mypy src
```

## License

MIT License