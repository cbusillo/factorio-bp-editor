# CLAUDE.md

Claude Code guidance for this repository.

## Project Overview

Factorio Blueprint Editor - A modern Python tool for editing and manipulating Factorio blueprints.

**Stack**: Python 3.13+, factorio-draftsman 2.0+, uv package manager

## Documentation

- [Style Guide](#style-guide) - Code standards based on modern Python practices
- [Testing Guide](#testing-guide) - Test patterns and examples
- [Blueprint Format](#blueprint-format) - Understanding Factorio blueprint structure

## Quick Command Reference

**Tests**: `uv run pytest -v`
- `uv run pytest tests/test_editor.py::TestBlueprintEditor` - Run specific test class
- `uv run pytest tests/test_editor.py::TestBlueprintEditor::test_move_entity` - Run specific test
- `uv run pytest --cov=src` - Run with coverage

**Format**: `uv run ruff format src tests examples`

**Lint**: `uv run ruff check src tests examples --fix`

**Type Check**: `uv run mypy src`

**Example Usage**: `cd examples && uv run python basic_usage.py`

## Development Workflow

1. **Check existing code** - Follow project patterns, use factorio-draftsman patterns
2. **Run tests** before marking tasks complete:
   - For new features: `uv run pytest -v`
   - For specific area: `uv run pytest tests/test_editor.py -v`
3. **Format and lint**: `uv run ruff format . && uv run ruff check . --fix`
4. **Type check**: `uv run mypy src`

## Architecture

**Core Modules**:
- `src/factorio_bp_editor/editor.py` - Main blueprint editor classes
- `BlueprintEditor` - High-level interface for blueprint manipulation
- `BlueprintBookEditor` - High-level interface for blueprint book manipulation

**Key Operations**:
- Entity management: add, remove, find, move, rotate
- Blueprint metadata: labels, descriptions, icons
- Import/export: base64 encoded blueprint strings
- Validation: blueprint correctness checking

## Style Guide

### Type Hints
- **Use built-in types**: `list`, `dict`, `set` instead of importing from `typing`
- **Use union operator**: `str | None` instead of `Optional[str]`
- **Never use `Any` or `object`**: Always be specific with types
- **Import specific types only when needed**: e.g., `from typing import Dict` only for complex generics

### String Formatting
- **Always use f-strings**: Even for logging and exceptions
- **No % formatting or .format()**: F-strings are the only acceptable format

### Comments and Documentation
- **NO comments**: Code should be self-documenting through:
  - Descriptive names using full words (no abbreviations)
  - Clear function/variable names that state their purpose
  - Method chains that read like sentences
- **Docstrings allowed** for public API methods only - keep them concise

### Control Flow
- **Early returns preferred**: No else after return statements
- **Clean control flow**: Make the code path obvious

### Naming Conventions
- **Full words**: `calculate_total_amount` not `calc_tot_amt`
- **Descriptive names**: Variable and function names should describe what they do
- **Boolean fields**: Use `is_` or `has_` prefix (e.g., `is_valid`, `has_entities`)
- **Constants**: UPPER_SNAKE_CASE
- **Private methods**: Single underscore prefix `_method_name`

### Line Length
- **Maximum 100 characters** per line (configured in ruff)

## Testing Guide

### Test Structure
- Tests in `tests/` directory
- Test files named `test_*.py`
- Test classes named `Test*`
- Test methods named `test_*`

### Test Patterns
```python
def test_descriptive_name(self):
    # Arrange
    editor = BlueprintEditor()
    entity = AssemblingMachine("assembling-machine-1")
    
    # Act
    editor.add_entity(entity)
    
    # Assert
    assert len(editor.blueprint.entities) == 1
```

### Running Tests
- All tests: `uv run pytest`
- Specific file: `uv run pytest tests/test_editor.py`
- Specific test: `uv run pytest tests/test_editor.py::TestBlueprintEditor::test_add_entity`
- With coverage: `uv run pytest --cov=src --cov-report=html`

## Blueprint Format

Factorio blueprints are:
1. JSON objects containing entities, tiles, and metadata
2. Compressed with zlib
3. Base64 encoded
4. Prefixed with version byte "0"

The factorio-draftsman library handles all encoding/decoding automatically.

### Example Blueprint String
```
0eNqllctugzAQRX8FeQ0VGEOAXfbddVlVFZBpYgmMZTttIsS/13m0SpVWHdsrIjw5h...
```

### Key Blueprint Components
- **Entities**: Machines, belts, inserters, etc.
- **Tiles**: Concrete, stone paths, etc.
- **Metadata**: Label, description, icons
- **Version**: Blueprint format version

## Example Files

- `examples/basic_usage.py` - Basic blueprint creation and manipulation
- `examples/derek_blueprints.txt` - Large collection of real blueprint strings (gitignored)

## Common Tasks

### Create a Blueprint
```python
editor = BlueprintEditor()
editor.set_metadata(label="My Blueprint")
machine = AssemblingMachine("assembling-machine-2")
machine.position = (0, 0)
editor.add_entity(machine)
blueprint_string = editor.to_string()
```

### Load and Modify
```python
editor = BlueprintEditor(blueprint_string)
stats = editor.get_stats()
machines = editor.find_entities("assembling-machine-2")
for machine in machines:
    editor.rotate_entity(machine.id, Direction.EAST)
```

### Blueprint Books
```python
book = BlueprintBookEditor()
book.set_metadata(label="My Blueprints")
book.add_blueprint(editor.blueprint)
book_string = book.to_string()
```

## Error Handling

The factorio-draftsman library provides detailed validation:
- **OverlappingObjectsWarning**: Entities placed in same location
- **DraftsmanError**: Invalid blueprint operations
- **Validation errors**: Blueprint import issues

## Development Tips

1. **Entity IDs**: Each entity has a unique ID for operations
2. **Positions**: Use tuples (x, y) or Vector objects
3. **Directions**: Use Direction constants (NORTH, EAST, SOUTH, WEST)
4. **Entity Types**: Use exact Factorio names (e.g., "assembling-machine-2")
5. **Validation**: Always validate blueprints before export