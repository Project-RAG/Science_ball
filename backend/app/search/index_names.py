from dataclasses import dataclass

@dataclass(frozen=True)
class ESIndexNames:
    DOCS = "rd_docs_v1"
    CHUNKS = "rd_chunks_v1"
    ENTITIES = "rd_entities_v1"
    FACTS = "rd_facts_v1"
    EXPERIMENTS = "rd_experiments_v1"
    EXPERTS = "rd_experts_v1"
