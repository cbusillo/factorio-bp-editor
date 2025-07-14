from typing import Optional, List, Dict, Any
from draftsman.blueprintable import Blueprint, BlueprintBook
from draftsman.entity import Entity
from draftsman.tile import Tile


class BlueprintEditor:
    def __init__(self, blueprint_string: Optional[str] = None):
        if blueprint_string:
            self.blueprint = Blueprint(blueprint_string)
        else:
            self.blueprint = Blueprint()

    def add_entity(self, entity: Entity) -> None:
        self.blueprint.entities.append(entity)

    def remove_entity(self, entity_id: str) -> bool:
        for index, entity in enumerate(self.blueprint.entities):
            if entity.id == entity_id:
                del self.blueprint.entities[index]
                return True
        return False

    def find_entities(self, entity_type: Optional[str] = None) -> List[Entity]:
        if entity_type:
            return [entity for entity in self.blueprint.entities if entity.name == entity_type]
        return list(self.blueprint.entities)

    def move_entity(self, entity_id: str, x_offset: float, y_offset: float) -> bool:
        for index, entity in enumerate(self.blueprint.entities):
            if entity.id == entity_id:
                entity_data = entity.to_dict()
                current_position = entity.position

                entity_data["position"]["x"] = current_position[0] + x_offset
                entity_data["position"]["y"] = current_position[1] + y_offset

                entity_class = type(entity)
                new_entity = entity_class(**entity_data)

                self.blueprint.entities[index] = new_entity
                return True
        return False

    def rotate_entity(self, entity_id: str, direction: int) -> bool:
        for entity in self.blueprint.entities:
            if entity.id == entity_id and hasattr(entity, "direction"):
                entity.direction = direction
                return True
        return False

    def add_tile(self, tile: Tile) -> None:
        self.blueprint.tiles.append(tile)

    def set_metadata(
        self,
        label: Optional[str] = None,
        description: Optional[str] = None,
        icons: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        if label is not None:
            self.blueprint.label = label
        if description is not None:
            self.blueprint.description = description
        if icons is not None:
            self.blueprint.icons = icons

    def to_string(self) -> str:
        return str(self.blueprint.to_string())

    def validate(self) -> List[str]:
        validation_errors = []
        try:
            _ = self.blueprint.to_dict()
        except Exception as exception:
            validation_errors.append(str(exception))

        return validation_errors

    def get_statistics(self) -> Dict[str, Any]:
        entity_counts_by_type: Dict[str, int] = {}
        for entity in self.blueprint.entities:
            entity_counts_by_type[entity.name] = entity_counts_by_type.get(entity.name, 0) + 1

        return {
            "total_entities": len(self.blueprint.entities),
            "total_tiles": len(self.blueprint.tiles),
            "entity_counts": entity_counts_by_type,
            "has_label": bool(self.blueprint.label),
            "has_description": bool(self.blueprint.description),
        }


class BlueprintBookEditor:
    def __init__(self, book_string: Optional[str] = None):
        if book_string:
            self.book = BlueprintBook(string=book_string)
        else:
            self.book = BlueprintBook()

    def add_blueprint(self, blueprint: Blueprint, insertion_index: Optional[int] = None) -> None:
        if insertion_index is None:
            self.book.blueprints.append(blueprint)
        else:
            self.book.blueprints.insert(insertion_index, blueprint)

    def remove_blueprint(self, blueprint_index: int) -> Optional[Blueprint]:
        if 0 <= blueprint_index < len(self.book.blueprints):
            return self.book.blueprints.pop(blueprint_index)
        return None

    def get_blueprint(self, blueprint_index: int) -> Optional[Blueprint]:
        if 0 <= blueprint_index < len(self.book.blueprints):
            return self.book.blueprints[blueprint_index]
        return None

    def set_metadata(
        self,
        label: Optional[str] = None,
        description: Optional[str] = None,
        icons: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        if label is not None:
            self.book.label = label
        if description is not None:
            self.book.description = description
        if icons is not None:
            self.book.icons = icons

    def to_string(self) -> str:
        return str(self.book.to_string())

    def get_book_statistics(self) -> Dict[str, Any]:
        total_entity_count = 0
        total_tile_count = 0

        for blueprint in self.book.blueprints:
            if isinstance(blueprint, Blueprint):
                total_entity_count += len(blueprint.entities)
                total_tile_count += len(blueprint.tiles)

        return {
            "total_blueprints": len(self.book.blueprints),
            "total_entities": total_entity_count,
            "total_tiles": total_tile_count,
            "has_label": bool(self.book.label),
            "has_description": bool(self.book.description),
        }