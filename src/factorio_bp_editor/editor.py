"""Main blueprint editor class for manipulating Factorio blueprints."""

from typing import Optional, List, Dict, Any
from draftsman.blueprintable import Blueprint, BlueprintBook
from draftsman.entity import Entity
from draftsman.tile import Tile


class BlueprintEditor:
    """A high-level interface for editing Factorio blueprints."""

    def __init__(self, blueprint_string: Optional[str] = None):
        """
        Initialize a BlueprintEditor.

        Args:
            blueprint_string: Base64 encoded blueprint string to load, or None for new blueprint
        """
        if blueprint_string:
            self.blueprint = Blueprint(blueprint_string)
        else:
            self.blueprint = Blueprint()

    def add_entity(self, entity: Entity) -> None:
        """Add an entity to the blueprint."""
        self.blueprint.entities.append(entity)

    def remove_entity(self, entity_id: str) -> bool:
        """
        Remove an entity by its ID.

        Returns:
            True if entity was found and removed, False otherwise
        """
        for i, entity in enumerate(self.blueprint.entities):
            if entity.id == entity_id:
                del self.blueprint.entities[i]
                return True
        return False

    def find_entities(self, entity_type: Optional[str] = None) -> List[Entity]:
        """
        Find entities in the blueprint.

        Args:
            entity_type: Filter by entity type (e.g., 'assembling-machine-3')

        Returns:
            List of entities matching the criteria
        """
        if entity_type:
            return [e for e in self.blueprint.entities if e.name == entity_type]
        return list(self.blueprint.entities)

    def move_entity(self, entity_id: str, dx: float, dy: float) -> bool:
        """
        Move an entity by a relative offset.

        Args:
            entity_id: ID of the entity to move
            dx: X offset
            dy: Y offset

        Returns:
            True if entity was found and moved, False otherwise
        """
        for i, entity in enumerate(self.blueprint.entities):
            if entity.id == entity_id:
                # Get entity data
                entity_data = entity.to_dict()
                current_pos = entity.position

                # Update position in data
                entity_data["position"]["x"] = current_pos[0] + dx
                entity_data["position"]["y"] = current_pos[1] + dy

                # Create new entity from updated data
                entity_class = type(entity)
                new_entity = entity_class(**entity_data)

                # Replace old entity with new
                self.blueprint.entities[i] = new_entity
                return True
        return False

    def rotate_entity(self, entity_id: str, direction: int) -> bool:
        """
        Rotate an entity.

        Args:
            entity_id: ID of the entity to rotate
            direction: New direction (0, 2, 4, 6 for N, E, S, W)

        Returns:
            True if entity was found and rotated, False otherwise
        """
        for entity in self.blueprint.entities:
            if entity.id == entity_id and hasattr(entity, "direction"):
                entity.direction = direction
                return True
        return False

    def add_tile(self, tile: Tile) -> None:
        """Add a tile to the blueprint."""
        self.blueprint.tiles.append(tile)

    def set_metadata(
        self,
        label: Optional[str] = None,
        description: Optional[str] = None,
        icons: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """
        Set blueprint metadata.

        Args:
            label: Blueprint label/name
            description: Blueprint description
            icons: List of icon definitions
        """
        if label is not None:
            self.blueprint.label = label
        if description is not None:
            self.blueprint.description = description
        if icons is not None:
            self.blueprint.icons = icons

    def to_string(self) -> str:
        """Export the blueprint as a base64 encoded string."""
        return str(self.blueprint.to_string())

    def validate(self) -> List[str]:
        """
        Validate the blueprint for issues.

        Returns:
            List of validation error messages
        """
        errors = []
        try:
            # This will raise exceptions if the blueprint is invalid
            _ = self.blueprint.to_dict()
        except Exception as e:
            errors.append(str(e))

        return errors

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the blueprint.

        Returns:
            Dictionary with blueprint statistics
        """
        entity_counts: Dict[str, int] = {}
        for entity in self.blueprint.entities:
            entity_counts[entity.name] = entity_counts.get(entity.name, 0) + 1

        return {
            "total_entities": len(self.blueprint.entities),
            "total_tiles": len(self.blueprint.tiles),
            "entity_counts": entity_counts,
            "has_label": bool(self.blueprint.label),
            "has_description": bool(self.blueprint.description),
        }


class BlueprintBookEditor:
    """A high-level interface for editing Factorio blueprint books."""

    def __init__(self, book_string: Optional[str] = None):
        """
        Initialize a BlueprintBookEditor.

        Args:
            book_string: Base64 encoded blueprint book string to load, or None for new book
        """
        if book_string:
            self.book = BlueprintBook(string=book_string)
        else:
            self.book = BlueprintBook()

    def add_blueprint(self, blueprint: Blueprint, index: Optional[int] = None) -> None:
        """
        Add a blueprint to the book.

        Args:
            blueprint: Blueprint to add
            index: Position to insert at, or None to append
        """
        if index is None:
            self.book.blueprints.append(blueprint)
        else:
            self.book.blueprints.insert(index, blueprint)

    def remove_blueprint(self, index: int) -> Optional[Blueprint]:
        """
        Remove a blueprint by index.

        Args:
            index: Index of blueprint to remove

        Returns:
            The removed blueprint, or None if index is invalid
        """
        if 0 <= index < len(self.book.blueprints):
            return self.book.blueprints.pop(index)
        return None

    def get_blueprint(self, index: int) -> Optional[Blueprint]:
        """
        Get a blueprint by index.

        Args:
            index: Index of blueprint to get

        Returns:
            The blueprint, or None if index is invalid
        """
        if 0 <= index < len(self.book.blueprints):
            return self.book.blueprints[index]
        return None

    def set_metadata(
        self,
        label: Optional[str] = None,
        description: Optional[str] = None,
        icons: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """
        Set blueprint book metadata.

        Args:
            label: Book label/name
            description: Book description
            icons: List of icon definitions
        """
        if label is not None:
            self.book.label = label
        if description is not None:
            self.book.description = description
        if icons is not None:
            self.book.icons = icons

    def to_string(self) -> str:
        """Export the blueprint book as a base64 encoded string."""
        return str(self.book.to_string())

    def get_book_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the blueprint book.

        Returns:
            Dictionary with book statistics
        """
        total_entities = 0
        total_tiles = 0

        for bp in self.book.blueprints:
            if isinstance(bp, Blueprint):
                total_entities += len(bp.entities)
                total_tiles += len(bp.tiles)

        return {
            "total_blueprints": len(self.book.blueprints),
            "total_entities": total_entities,
            "total_tiles": total_tiles,
            "has_label": bool(self.book.label),
            "has_description": bool(self.book.description),
        }
