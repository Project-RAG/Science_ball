from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ElasticsearchIndexManager:
    """
    Handles the creation and updating of Elasticsearch indices based on defined mappings.
    """

    def __init__(self, es_client: Any):
        self.es_client = es_client

    async def create_index_if_not_exists(self, index_name: str, settings_and_mappings: Dict[str, Any]) -> bool:
        """
        Creates an index if it does not already exist.
        Returns True if created or already exists, False otherwise.
        """
        try:
            exists = await self.es_client.indices.exists(index=index_name)
            if not exists:
                logger.info(f"Creating Elasticsearch index: {index_name}")
                await self.es_client.indices.create(
                    index=index_name,
                    body=settings_and_mappings
                )
                return True
            return True
        except Exception as e:
            logger.error(f"Error creating index {index_name}: {e}")
            return False

    async def update_index_mappings(self, index_name: str, mappings: Dict[str, Any]) -> bool:
        """
        Updates the mapping for an existing index.
        Note: In ES, some fields cannot be updated without re-indexing.
        """
        try:
            await self.es_client.indices.put_mapping(
                index=index_name,
                body={"properties": mappings}
            )
            return True
        except Exception as e:
            logger.error(f"Error updating mapping for {index_name}: {e}")
            return False

    async def setup_all_indices(self, index_configs: Dict[str, Dict[str, Any]]) -> Dict[str, bool]:
        """
        Ensures all indices defined in the config are created.
        """
        results = {}
        for index_name, config in index_configs.items():
            results[index_name] = await self.create_index_if_not_exists(index_name, config)
        return results
