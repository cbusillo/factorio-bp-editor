"""Examples of common blueprint operations."""

from factorio_bp_editor import BlueprintEditor, BlueprintBookEditor
from draftsman.entity import AssemblingMachine, Inserter, TransportBelt, ElectricPole
from draftsman.constants import Direction
from draftsman.tile import Tile


def example_copy_and_offset():
    """Copy all entities in a blueprint and offset them."""
    # Example blueprint string (you would use a real one)
    blueprint_string = "0eNqVkd1qwzAMhV9F6NomP3YSp95Vr8ZYMa7iBIO1jMQphZJ3n9ONQWG0o1fC4jvS0ZHWYK1adKhtQ7YGTI96C+w2tqI5Ws1rFBb7l4ZaUsxArKikyoJTqGzJkqNQ3BimNb6XFHu0BGYAF9E6otXB3eC1HvhQD0xXHazLECYQXvNwGi6m8XKWX+LIJb8lPidJQPJ5yjOa5p7H8/yWnPlEKT0PTFrqA9nfC0VFDS9VzxNlcUtdz+f7qnd+6vnRPfXgKBQ11WJ3oM7+ZzyINtQFJpDQlpoqFKqilv4RjVa7TfMqmu1hu+kPHjuGLLBf3n/6H9gP3wpnB+T4hqMP3vF1dBwd9x0fl8dx8j84+qcdx/jC8eaJY/yF+gsH4+8c"
    
    editor = BlueprintEditor(blueprint_string)
    print(f"Original blueprint has {len(editor.blueprint.entities)} entities")
    
    # Get all entities
    original_entities = editor.find_entities()
    
    # Calculate offset (move everything 10 tiles to the right)
    offset_x = 10
    offset_y = 0
    
    # Copy each entity with offset
    for entity in original_entities[:]:  # Create a copy of the list
        # Create new entity of same type
        entity_data = entity.to_dict()
        entity_data['position']['x'] += offset_x
        entity_data['position']['y'] += offset_y
        
        # Create new entity instance
        entity_class = type(entity)
        new_entity = entity_class(**entity_data)
        
        # Add to blueprint
        editor.add_entity(new_entity)
    
    print(f"After copying: {len(editor.blueprint.entities)} entities")
    
    # Update label
    original_label = editor.blueprint.label or "Blueprint"
    editor.set_metadata(label=f"{original_label} (Doubled)")
    
    return editor.to_string()


def example_filter_entities():
    """Remove all entities of a specific type from a blueprint."""
    # Create a sample blueprint
    editor = BlueprintEditor()
    
    # Add various entities
    for i in range(5):
        machine = AssemblingMachine("assembling-machine-2")
        machine.position = (i * 4, 0)
        editor.add_entity(machine)
        
        inserter = Inserter("inserter")
        inserter.position = (i * 4 + 1, 0)
        editor.add_entity(inserter)
        
        belt = TransportBelt("transport-belt")
        belt.position = (i * 4, 2)
        editor.add_entity(belt)
    
    print(f"Before filtering: {len(editor.blueprint.entities)} entities")
    stats = editor.get_stats()
    print(f"Entity types: {stats['entity_counts']}")
    
    # Remove all inserters
    inserters = editor.find_entities("inserter")
    print(f"Found {len(inserters)} inserters to remove")
    
    for inserter in inserters:
        editor.remove_entity(inserter.id)
    
    print(f"After filtering: {len(editor.blueprint.entities)} entities")
    stats = editor.get_stats()
    print(f"Entity types: {stats['entity_counts']}")
    
    return editor


def example_create_power_grid():
    """Create a blueprint with a power grid layout."""
    editor = BlueprintEditor()
    editor.set_metadata(
        label="Power Grid Template",
        description="Medium electric pole grid for maximum coverage"
    )
    
    # Medium electric poles have a wire reach of 9 tiles
    # Optimal spacing is 9 tiles for maximum coverage
    grid_size = 9
    grid_width = 5
    grid_height = 5
    
    for x in range(grid_width):
        for y in range(grid_height):
            pole = ElectricPole("medium-electric-pole")
            pole.position = (x * grid_size, y * grid_size)
            editor.add_entity(pole)
    
    # Add concrete tiles under poles
    for x in range(grid_width):
        for y in range(grid_height):
            # 3x3 concrete pad under each pole
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    tile = Tile("refined-concrete")
                    tile.position = (x * grid_size + dx, y * grid_size + dy)
                    editor.add_tile(tile)
    
    stats = editor.get_stats()
    print(f"Created power grid: {stats['total_entities']} poles, {stats['total_tiles']} tiles")
    
    return editor


def example_blueprint_book_organization():
    """Organize blueprints into a book by category."""
    book = BlueprintBookEditor()
    book.set_metadata(
        label="Factory Components",
        description="Organized blueprint collection"
    )
    
    # Create production blueprint
    production = BlueprintEditor()
    production.set_metadata(label="Iron Gear Production")
    for i in range(3):
        machine = AssemblingMachine("assembling-machine-2")
        machine.position = (i * 4, 0)
        machine.recipe = "iron-gear-wheel"
        production.add_entity(machine)
    
    # Create power blueprint
    power = example_create_power_grid()
    
    # Create logistics blueprint
    logistics = BlueprintEditor()
    logistics.set_metadata(label="Belt Balancer")
    for i in range(4):
        belt = TransportBelt("express-transport-belt")
        belt.position = (i, 0)
        belt.direction = Direction.EAST
        logistics.add_entity(belt)
    
    # Add all to book
    book.add_blueprint(production.blueprint)
    book.add_blueprint(power.blueprint)
    book.add_blueprint(logistics.blueprint)
    
    print(f"Created blueprint book with {len(book.book.blueprints)} blueprints")
    
    return book


def example_validate_and_fix():
    """Validate a blueprint and attempt to fix common issues."""
    editor = BlueprintEditor()
    
    # Create a blueprint with potential issues
    # Add overlapping entities (will generate warning)
    machine1 = AssemblingMachine("assembling-machine-2")
    machine1.position = (0, 0)
    editor.add_entity(machine1)
    
    machine2 = AssemblingMachine("assembling-machine-2")
    machine2.position = (1, 0)  # Too close, will overlap
    editor.add_entity(machine2)
    
    # Add inserter pointing at nothing
    inserter = Inserter("inserter")
    inserter.position = (10, 10)
    inserter.direction = Direction.EAST
    editor.add_entity(inserter)
    
    print("Validating blueprint...")
    errors = editor.validate()
    
    if errors:
        print(f"Found {len(errors)} validation errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Blueprint is valid!")
    
    # Get statistics
    stats = editor.get_stats()
    print(f"\nBlueprint statistics:")
    print(f"  Total entities: {stats['total_entities']}")
    print(f"  Entity types: {stats['entity_counts']}")
    
    return editor


def main():
    """Run all examples."""
    print("=== Blueprint Operations Examples ===\n")
    
    print("1. Filtering Entities")
    print("-" * 40)
    example_filter_entities()
    
    print("\n2. Creating Power Grid")
    print("-" * 40)
    power_editor = example_create_power_grid()
    print(f"Blueprint string: {power_editor.to_string()[:100]}...")
    
    print("\n3. Blueprint Book Organization")
    print("-" * 40)
    book = example_blueprint_book_organization()
    book_string = book.to_string()
    print(f"Book string: {book_string[:100]}...")
    
    print("\n4. Validation Example")
    print("-" * 40)
    example_validate_and_fix()
    
    print("\n5. Copy and Offset (requires real blueprint string)")
    print("-" * 40)
    try:
        new_string = example_copy_and_offset()
        print(f"New blueprint string: {new_string[:100]}...")
    except Exception as e:
        print(f"Example failed (expected with demo string): {e}")


if __name__ == "__main__":
    main()