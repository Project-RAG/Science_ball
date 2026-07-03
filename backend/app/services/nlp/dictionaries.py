"""Domain dictionaries for entity extraction."""

from typing import Dict, List, Set

# Structure: { " canonical_name": {"aliases": {"alias1", "alias2"}, "type": "EntityType"} }
DOMAIN_DICTIONARY: Dict[str, Dict] = {
    # Materials
    "nickel": {
        "aliases": {"никель", "Ni", "nickel ore", "никелевая руда"},
        "type": "Material",
    },
    "copper": {
        "aliases": {"медь", "Cu", "copper ore", "медная руда"},
        "type": "Material",
    },
    "cobalt": {
        "aliases": {"кобальт", "Co"},
        "type": "Material",
    },

    # Processes
    "electrowinning": {
        "aliases": {"электроэкстракция", "electrowinning", "электролитическое извлечение"},
        "type": "Process",
    },
    "leaching": {
        "aliases": {"выщелачивание", "leaching"},
        "type": "Process",
    },
    "flotation": {
        "aliases": {"флотация", "flotation"},
        "type": "Process",
    },

    # Equipment
    "electrolyzer": {
        "aliases": {"электролизер", "electrolyzer", "electrolytic cell"},
        "type": "Equipment",
    },
    "crusher": {
        "aliases": {"дробилка", "crusher"},
        "type": "Equipment",
    },

    # Properties
    "flow_velocity": {
        "aliases": {"скорость потока", "flow velocity", "linear velocity"},
        "type": "Property",
    },
    "temperature": {
        "aliases": {"температура", "temperature"},
        "type": "Property",
    },
    "concentration": {
        "aliases": {"концентрация", "concentration", "content"},
        "type": "Property",
    },

    # Organizations
    "mining_institute": {
        "aliases": {"институт горного дела", "mining institute"},
        "type": "Organization",
    },

    # Locations
    "canada": {
        "aliases": {"Канада", "Canada"},
        "type": "Location",
    },
    "russia": {
        "aliases": {"Россия", "Russia"},
        "type": "Location",
    },
}

def get_flattened_dictionary() -> Dict[str, Dict]:
    """
    Flattens the dictionary so that every alias maps to its canonical metadata.
    Used for efficient lookup.
    """
    flat_dict = {}
    for canonical, data in DOMAIN_DICTIONARY.items():
        for alias in data["aliases"]:
            flat_dict[alias.lower()] = {
                "canonical": canonical,
                "type": data["type"],
            }
    return flat_dict
