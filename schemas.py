from typing import List
from pydantic import BaseModel, Field


class ConceptNode(BaseModel):
    id: str = Field(
        description="A short, human-readable concept name. This must be unique within the graph."
    )
    definition: str = Field(
        description="A concise explanation of the concept in 1 to 3 sentences."
    )
    category: str = Field(
        description=(
            "A broad category such as model, method, architecture, task, dataset, "
            "paper, evaluation, math, system, application, or other."
        )
    )


class ConceptEdge(BaseModel):
    source: str = Field(description="The source concept node id.")
    target: str = Field(description="The target concept node id.")
    relation: str = Field(
        description="A short relationship phrase, such as uses, contains, improves upon, or is used for."
    )
    explanation: str = Field(
        description="One sentence explaining why this relationship is meaningful."
    )


class ConceptGraph(BaseModel):
    center: str = Field(description="The central concept that the graph is built around.")
    nodes: List[ConceptNode] = Field(description="Concept nodes in the graph.")
    edges: List[ConceptEdge] = Field(description="Directed relationships between concept nodes.")
    suggested_concepts: List[str] = Field(
        description="Additional related concepts that the user may want to explore next."
    )