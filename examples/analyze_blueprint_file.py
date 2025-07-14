"""Analyze a file containing multiple blueprint strings."""

import re
from pathlib import Path
from factorio_bp_editor import BlueprintEditor, BlueprintBookEditor
from draftsman.blueprintable import get_blueprintable_from_string


def extract_blueprint_strings(file_path: Path) -> list[str]:
    """Extract all blueprint strings from a text file."""
    content = file_path.read_text()
    
    # Blueprint strings start with "0eN" and contain base64 chars
    pattern = r'0eN[A-Za-z0-9+/]+'
    matches = re.findall(pattern, content)
    
    return matches


def analyze_blueprint(blueprint_string: str, index: int) -> dict[str, any]:
    """Analyze a single blueprint string."""
    try:
        # Use draftsman to determine type
        blueprintable = get_blueprintable_from_string(blueprint_string)
        bp_type = type(blueprintable).__name__
        
        if bp_type == "Blueprint":
            editor = BlueprintEditor(blueprint_string)
            stats = editor.get_stats()
            
            return {
                "index": index,
                "type": "Blueprint",
                "label": editor.blueprint.label or "Unnamed",
                "total_entities": stats["total_entities"],
                "total_tiles": stats["total_tiles"],
                "entity_types": list(stats["entity_counts"].keys()),
                "valid": True,
                "error": None
            }
            
        elif bp_type == "BlueprintBook":
            book_editor = BlueprintBookEditor(blueprint_string)
            stats = book_editor.get_book_stats()
            
            blueprint_labels = []
            for i in range(len(book_editor.book.blueprints)):
                bp = book_editor.get_blueprint(i)
                if bp and hasattr(bp, 'label'):
                    blueprint_labels.append(bp.label or f"Blueprint {i+1}")
            
            return {
                "index": index,
                "type": "BlueprintBook",
                "label": book_editor.book.label or "Unnamed Book",
                "total_blueprints": stats["total_blueprints"],
                "total_entities": stats["total_entities"],
                "blueprint_labels": blueprint_labels,
                "valid": True,
                "error": None
            }
        else:
            return {
                "index": index,
                "type": "Unknown",
                "valid": False,
                "error": f"Unknown blueprint type: {bp_type}"
            }
            
    except Exception as e:
        return {
            "index": index,
            "type": "Error",
            "valid": False,
            "error": str(e)
        }


def print_analysis(analysis: dict[str, any]) -> None:
    """Print analysis results for a blueprint."""
    print(f"\n--- Blueprint #{analysis['index']} ---")
    
    if not analysis["valid"]:
        print(f"ERROR: {analysis['error']}")
        return
    
    print(f"Type: {analysis['type']}")
    print(f"Label: {analysis['label']}")
    
    if analysis["type"] == "Blueprint":
        print(f"Entities: {analysis['total_entities']}")
        print(f"Tiles: {analysis['total_tiles']}")
        if analysis["entity_types"]:
            print(f"Entity Types: {', '.join(analysis['entity_types'][:5])}")
            if len(analysis["entity_types"]) > 5:
                print(f"  ... and {len(analysis['entity_types']) - 5} more")
                
    elif analysis["type"] == "BlueprintBook":
        print(f"Blueprints: {analysis['total_blueprints']}")
        print(f"Total Entities: {analysis['total_entities']}")
        if analysis["blueprint_labels"]:
            print("Contained Blueprints:")
            for label in analysis["blueprint_labels"][:5]:
                print(f"  - {label}")
            if len(analysis["blueprint_labels"]) > 5:
                print(f"  ... and {len(analysis['blueprint_labels']) - 5} more")


def main():
    """Analyze blueprint file."""
    # Path to the example file
    file_path = Path("derek_blueprints.txt")
    
    if not file_path.exists():
        print(f"File not found: {file_path}")
        print("This example expects 'derek_blueprints.txt' in the examples directory.")
        return
    
    print(f"Analyzing blueprints in: {file_path}")
    
    # Extract all blueprint strings
    blueprint_strings = extract_blueprint_strings(file_path)
    print(f"\nFound {len(blueprint_strings)} blueprint strings")
    
    # Analyze each blueprint
    valid_count = 0
    blueprint_count = 0
    book_count = 0
    total_entities = 0
    
    for i, bp_string in enumerate(blueprint_strings, 1):
        analysis = analyze_blueprint(bp_string, i)
        
        # Print first few analyses
        if i <= 5:
            print_analysis(analysis)
        
        # Collect statistics
        if analysis["valid"]:
            valid_count += 1
            if analysis["type"] == "Blueprint":
                blueprint_count += 1
                total_entities += analysis["total_entities"]
            elif analysis["type"] == "BlueprintBook":
                book_count += 1
                total_entities += analysis["total_entities"]
    
    # Print summary
    print(f"\n{'='*50}")
    print("SUMMARY")
    print(f"{'='*50}")
    print(f"Total blueprint strings: {len(blueprint_strings)}")
    print(f"Valid blueprints: {valid_count}")
    print(f"Single blueprints: {blueprint_count}")
    print(f"Blueprint books: {book_count}")
    print(f"Invalid/errors: {len(blueprint_strings) - valid_count}")
    print(f"Total entities across all: {total_entities}")
    
    # Find most complex blueprint
    if blueprint_strings:
        max_entities = 0
        max_label = "Unknown"
        
        for i, bp_string in enumerate(blueprint_strings, 1):
            analysis = analyze_blueprint(bp_string, i)
            if analysis["valid"] and analysis["type"] == "Blueprint":
                if analysis["total_entities"] > max_entities:
                    max_entities = analysis["total_entities"]
                    max_label = analysis["label"]
        
        if max_entities > 0:
            print(f"\nMost complex blueprint: '{max_label}' with {max_entities} entities")


if __name__ == "__main__":
    main()