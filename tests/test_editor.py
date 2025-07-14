"""Tests for the blueprint editor module."""

import pytest
from factorio_bp_editor import BlueprintEditor, BlueprintBookEditor
from draftsman.entity import AssemblingMachine, TransportBelt, Inserter
from draftsman.constants import Direction
from draftsman.blueprintable import Blueprint


class TestBlueprintEditor:
    """Test cases for BlueprintEditor class."""
    
    def test_create_empty_blueprint(self):
        """Test creating an empty blueprint."""
        editor = BlueprintEditor()
        assert editor.blueprint is not None
        assert len(editor.blueprint.entities) == 0
        assert len(editor.blueprint.tiles) == 0
    
    def test_add_entity(self):
        """Test adding entities to a blueprint."""
        editor = BlueprintEditor()
        
        machine = AssemblingMachine("assembling-machine-1")
        machine.position = (0, 0)
        editor.add_entity(machine)
        
        assert len(editor.blueprint.entities) == 1
        assert editor.blueprint.entities[0].name == "assembling-machine-1"
    
    def test_remove_entity(self):
        """Test removing entities from a blueprint."""
        editor = BlueprintEditor()
        
        machine = AssemblingMachine("assembling-machine-1")
        machine.position = (0, 0)
        editor.add_entity(machine)
        
        entity_id = editor.blueprint.entities[0].id
        removed = editor.remove_entity(entity_id)
        
        assert removed is True
        assert len(editor.blueprint.entities) == 0
    
    def test_remove_nonexistent_entity(self):
        """Test removing a non-existent entity."""
        editor = BlueprintEditor()
        removed = editor.remove_entity("nonexistent-id")
        assert removed is False
    
    def test_find_entities_by_type(self):
        """Test finding entities by type."""
        editor = BlueprintEditor()
        
        # Add different types of entities
        machine1 = AssemblingMachine("assembling-machine-1")
        machine1.position = (0, 0)
        editor.add_entity(machine1)
        
        machine2 = AssemblingMachine("assembling-machine-2")
        machine2.position = (3, 0)
        editor.add_entity(machine2)
        
        belt = TransportBelt("transport-belt")
        belt.position = (1, 0)
        editor.add_entity(belt)
        
        # Find specific entity type
        found = editor.find_entities("assembling-machine-1")
        assert len(found) == 1
        assert found[0].name == "assembling-machine-1"
        
        # Find all entities
        all_entities = editor.find_entities()
        assert len(all_entities) == 3
    
    def test_move_entity(self):
        """Test moving an entity."""
        editor = BlueprintEditor()
        
        machine = AssemblingMachine("assembling-machine-1")
        machine.position = (0, 0)
        editor.add_entity(machine)
        
        entity_id = editor.blueprint.entities[0].id
        moved = editor.move_entity(entity_id, 5, 3)
        
        assert moved is True
        assert editor.blueprint.entities[0].position[0] == 5
        assert editor.blueprint.entities[0].position[1] == 3
    
    def test_rotate_entity(self):
        """Test rotating an entity."""
        editor = BlueprintEditor()
        
        inserter = Inserter("inserter")
        inserter.position = (0, 0)
        inserter.direction = Direction.NORTH
        editor.add_entity(inserter)
        
        entity_id = editor.blueprint.entities[0].id
        rotated = editor.rotate_entity(entity_id, Direction.EAST)
        
        assert rotated is True
        assert editor.blueprint.entities[0].direction == Direction.EAST
    
    def test_set_metadata(self):
        """Test setting blueprint metadata."""
        editor = BlueprintEditor()
        
        editor.set_metadata(
            label="Test Blueprint",
            description="A test description"
        )
        
        assert editor.blueprint.label == "Test Blueprint"
        assert editor.blueprint.description == "A test description"
    
    def test_to_string(self):
        """Test exporting blueprint to string."""
        editor = BlueprintEditor()
        editor.set_metadata(label="Test")
        
        machine = AssemblingMachine("assembling-machine-1")
        machine.position = (0, 0)
        editor.add_entity(machine)
        
        blueprint_string = editor.to_string()
        assert isinstance(blueprint_string, str)
        assert len(blueprint_string) > 0
    
    def test_load_from_string(self):
        """Test loading a blueprint from string."""
        # First create and export a blueprint
        editor1 = BlueprintEditor()
        editor1.set_metadata(label="Original")
        
        machine = AssemblingMachine("assembling-machine-1")
        machine.position = (0, 0)
        editor1.add_entity(machine)
        
        blueprint_string = editor1.to_string()
        
        # Load the blueprint in a new editor
        editor2 = BlueprintEditor(blueprint_string)
        
        assert editor2.blueprint.label == "Original"
        assert len(editor2.blueprint.entities) == 1
        assert editor2.blueprint.entities[0].name == "assembling-machine-1"
    
    def test_get_statistics(self):
        """Test getting blueprint statistics."""
        editor = BlueprintEditor()
        
        # Add multiple entities
        for i in range(3):
            machine = AssemblingMachine("assembling-machine-1")
            machine.position = (i * 3, 0)
            editor.add_entity(machine)
        
        for i in range(2):
            belt = TransportBelt("transport-belt")
            belt.position = (i, 2)
            editor.add_entity(belt)
        
        stats = editor.get_statistics()
        
        assert stats['total_entities'] == 5
        assert stats['entity_counts']['assembling-machine-1'] == 3
        assert stats['entity_counts']['transport-belt'] == 2
        assert stats['has_label'] is False
        assert stats['has_description'] is False


class TestBlueprintBookEditor:
    """Test cases for BlueprintBookEditor class."""
    
    def test_create_empty_book(self):
        """Test creating an empty blueprint book."""
        book_editor = BlueprintBookEditor()
        assert book_editor.book is not None
        assert len(book_editor.book.blueprints) == 0
    
    def test_add_blueprint(self):
        """Test adding blueprints to a book."""
        book_editor = BlueprintBookEditor()
        
        # Create a blueprint
        blueprint = Blueprint()
        blueprint.label = "Test Blueprint"
        
        book_editor.add_blueprint(blueprint)
        
        assert len(book_editor.book.blueprints) == 1
        assert book_editor.book.blueprints[0].label == "Test Blueprint"
    
    def test_add_blueprint_at_index(self):
        """Test adding blueprint at specific index."""
        book_editor = BlueprintBookEditor()
        
        # Add multiple blueprints
        for i in range(3):
            blueprint = Blueprint()
            blueprint.label = f"Blueprint {i}"
            book_editor.add_blueprint(blueprint)
        
        # Insert a blueprint at index 1
        new_blueprint = Blueprint()
        new_blueprint.label = "Inserted Blueprint"
        book_editor.add_blueprint(new_blueprint, 1)
        
        assert len(book_editor.book.blueprints) == 4
        assert book_editor.book.blueprints[1].label == "Inserted Blueprint"
    
    def test_remove_blueprint(self):
        """Test removing a blueprint from the book."""
        book_editor = BlueprintBookEditor()
        
        # Add blueprints
        for i in range(3):
            blueprint = Blueprint()
            blueprint.label = f"Blueprint {i}"
            book_editor.add_blueprint(blueprint)
        
        # Remove the middle blueprint
        removed = book_editor.remove_blueprint(1)
        
        assert removed is not None
        assert removed.label == "Blueprint 1"
        assert len(book_editor.book.blueprints) == 2
        assert book_editor.book.blueprints[0].label == "Blueprint 0"
        assert book_editor.book.blueprints[1].label == "Blueprint 2"
    
    def test_get_blueprint(self):
        """Test getting a blueprint by index."""
        book_editor = BlueprintBookEditor()
        
        blueprint = Blueprint()
        blueprint.label = "Test Blueprint"
        book_editor.add_blueprint(blueprint)
        
        retrieved = book_editor.get_blueprint(0)
        assert retrieved is not None
        assert retrieved.label == "Test Blueprint"
        
        # Test invalid index
        assert book_editor.get_blueprint(10) is None
    
    def test_set_book_metadata(self):
        """Test setting blueprint book metadata."""
        book_editor = BlueprintBookEditor()
        
        book_editor.set_metadata(
            label="Test Book",
            description="A test blueprint book"
        )
        
        assert book_editor.book.label == "Test Book"
        assert book_editor.book.description == "A test blueprint book"
    
    def test_book_to_string(self):
        """Test exporting blueprint book to string."""
        book_editor = BlueprintBookEditor()
        book_editor.set_metadata(label="Test Book")
        
        # Add a blueprint
        blueprint = Blueprint()
        blueprint.label = "Test Blueprint"
        book_editor.add_blueprint(blueprint)
        
        book_string = book_editor.to_string()
        assert isinstance(book_string, str)
        assert len(book_string) > 0
    
    def test_get_book_statistics(self):
        """Test getting blueprint book statistics."""
        book_editor = BlueprintBookEditor()
        
        # Create blueprints with entities
        for i in range(2):
            editor = BlueprintEditor()
            editor.set_metadata(label=f"Blueprint {i}")
            
            for j in range(3):
                machine = AssemblingMachine("assembling-machine-1")
                machine.position = (j * 3, 0)
                editor.add_entity(machine)
            
            book_editor.add_blueprint(editor.blueprint)
        
        stats = book_editor.get_book_statistics()
        
        assert stats['total_blueprints'] == 2
        assert stats['total_entities'] == 6
        assert stats['total_tiles'] == 0
        assert stats['has_label'] is False