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
from factorio_bp_editor import BlueprintEditor, BlueprintBookEditor
from draftsman.entity import AssemblingMachine
from draftsman.constants import Direction

# Create a new blueprint
editor = BlueprintEditor()
editor.set_metadata(label="My Assembly Line")

# Add entities
machine = AssemblingMachine("assembling-machine-2")
machine.position = (0, 0)
machine.recipe = "iron-gear-wheel"
editor.add_entity(machine)

# Export blueprint string
blueprint_string = editor.to_string()

# Load existing blueprint
editor = BlueprintEditor(blueprint_string)
stats = editor.get_stats()
print(f"Blueprint has {stats['total_entities']} entities")
```

## Examples

- `examples/basic_usage.py` - Comprehensive introduction to the library
- `examples/blueprint_operations.py` - Common blueprint manipulation tasks
- `examples/analyze_blueprint_file.py` - Analyze files containing blueprint strings

## Development

This project uses:
- `uv` for dependency management
- `ruff` for linting and formatting
- `mypy` for type checking
- `pytest` for testing

See [CLAUDE.md](CLAUDE.md) for detailed development guidelines and code style.

```bash
# Run tests
uv run pytest

# Format code
uv run ruff format

# Lint code
uv run ruff check

# Type check
uv run mypy src
```

## License

MIT License