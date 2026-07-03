from __future__ import annotations
from typing import List

from app.services.nlp.entity_extractor import EntityExtractor

__all__ = ["EntityExtractor"]

# We expose the extractor here for easier imports in other services
# although usually we use a dedicated service class.
