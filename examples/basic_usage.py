"""Basic usage examples for the Factorio Blueprint Editor."""

from factorio_bp_editor import BlueprintEditor, BlueprintBookEditor
from draftsman.entity import AssemblingMachine, TransportBelt, Inserter
from draftsman.constants import Direction


def create_simple_blueprint():
    """Create a simple blueprint with assembling machines and belts."""
    editor = BlueprintEditor()
    
    editor.set_metadata(
        label="Simple Assembly Line",
        description="A basic assembly line setup"
    )
    
    for i in range(3):
        machine = AssemblingMachine("assembling-machine-2")
        machine.position = (i * 4, 0)
        machine.recipe = "iron-gear-wheel"
        editor.add_entity(machine)
        
        inserter_in = Inserter("fast-inserter")
        inserter_in.position = (i * 4 - 1, 0)
        inserter_in.direction = Direction.EAST
        editor.add_entity(inserter_in)
        
        inserter_out = Inserter("fast-inserter")
        inserter_out.position = (i * 4 + 1, 0)
        inserter_out.direction = Direction.WEST
        editor.add_entity(inserter_out)
    
    for x in range(-2, 11):
        belt_in = TransportBelt("express-transport-belt")
        belt_in.position = (x, -2)
        belt_in.direction = Direction.EAST
        editor.add_entity(belt_in)
        
        belt_out = TransportBelt("express-transport-belt")
        belt_out.position = (x, 2)
        belt_out.direction = Direction.EAST
        editor.add_entity(belt_out)
    
    return editor


def modify_existing_blueprint(blueprint_string: str):
    """Example of modifying an existing blueprint."""
    editor = BlueprintEditor(blueprint_string)
    
    print("Before modification:")
    stats = editor.get_statistics()
    print(f"  Total entities: {stats['total_entities']}")
    print(f"  Entity types: {stats['entity_counts']}")
    
    machines = editor.find_entities("assembling-machine-2")
    print(f"\nFound {len(machines)} assembling machines")
    
    for machine in machines:
        editor.remove_entity(machine.id)
        
        new_machine = AssemblingMachine("assembling-machine-3")
        new_machine.position = machine.position
        new_machine.recipe = machine.recipe
        editor.add_entity(new_machine)
    
    print("\nAfter modification:")
    stats = editor.get_statistics()
    print(f"  Total entities: {stats['total_entities']}")
    print(f"  Entity types: {stats['entity_counts']}")
    
    return editor


def create_blueprint_book():
    """Create a blueprint book with multiple blueprints."""
    book_editor = BlueprintBookEditor()
    
    book_editor.set_metadata(
        label="Factory Blueprints",
        description="Collection of useful factory setups"
    )
    
    for i in range(3):
        editor = BlueprintEditor()
        editor.set_metadata(label=f"Blueprint {i+1}")
        
        for j in range(2):
            machine = AssemblingMachine("assembling-machine-1")
            machine.position = (j * 3, i * 3)
            editor.add_entity(machine)
        
        book_editor.add_blueprint(editor.blueprint)
    
    stats = book_editor.get_book_statistics()
    print(f"Blueprint book contains {stats['total_blueprints']} blueprints")
    print(f"Total entities across all blueprints: {stats['total_entities']}")
    
    return book_editor


def main():
    """Run the examples."""
    print("Creating a simple blueprint...")
    editor = create_simple_blueprint()
    
    blueprint_string = editor.to_string()
    print(f"\nBlueprint string (first 100 chars): {blueprint_string[:100]}...")
    
    stats = editor.get_statistics()
    print(f"\nBlueprint statistics:")
    print(f"  Total entities: {stats['total_entities']}")
    print(f"  Entity breakdown: {stats['entity_counts']}")
    
    errors = editor.validate()
    if errors:
        print(f"\nValidation errors: {errors}")
    else:
        print("\nBlueprint is valid!")
    
    print("\n" + "="*50 + "\n")
    
    print("Creating a blueprint book...")
    book_editor = create_blueprint_book()
    book_string = book_editor.to_string()
    print(f"\nBook string (first 100 chars): {book_string[:100]}...")


if __name__ == "__main__":
    main()