from typing import List, Dict, Any, Optional
from uuid import UUID
from dataclasses import dataclass

@dataclass
class EntitySpan:
    """Represents a found entity in text."""
    start: int
    end: int
    text: str
    canonical_name: str
    entity_type: str


class EntityExtractor:
    """Deterministic entity extraction using domain dictionaries."""

    def __init__(self, dictionary: Dict[str, Any]):
        # We use the flattened version for O(1) lookup of aliases
        self.lookup = dictionary

    def extract(self, text: str) -> List[EntitySpan]:
        """
        Extracts entities from text based on dictionary matching.
        Implements a simple longest-match-first strategy to avoid partial overlaps.
        """
        if not text:
            return []

        text_lower = text.lower()
        found_spans = []

        # To implement longest-match-first, we sort all possible keys by length descending
        all_aliases = sorted(self.lookup.keys(), key=len, reverse=True)

        # Track which parts of the text are already 'consumed' by an entity
        consumed = [False] * len(text)

        for alias in all_aliases:
            start_search = 0
            while True:
                idx = text_lower.find(alias, start_search)
                if idx == -1:
                    break

                end = idx + len(alias)
                # Check if this span overlaps with any already consumed part
                if any(consumed[i] for i in range(idx, end)):
                    start_search = idx + 1
                    continue

                # Mark as consumed
                for i in range(idx, end):
                    consumed[i] = True

                meta = self.lookup[alias]
                found_spans.append(EntitySpan(
                    start=idx,
                    end=end,
                    text=text[idx:end],
                    canonical_name=meta["canonical"],
                    entity_type=meta["type"]
                ))
                start_search = end

        # Return sorted by start position
        return sorted(found_spans, key=lambda x: x.start)
