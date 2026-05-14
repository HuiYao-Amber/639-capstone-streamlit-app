import os
from typing import List, Optional

import streamlit as st
from google import genai
from google.genai import types

from schemas import ConceptGraph


def get_gemini_api_key() -> str:
    """
    Read Gemini API key from Streamlit secrets or environment variables.
    """

    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key

    raise RuntimeError(
        "Missing Gemini API key. Add GEMINI_API_KEY to .streamlit/secrets.toml."
    )


def build_prompt(
    concept: str,
    existing_nodes: Optional[List[str]] = None,
    max_new_nodes: int = 7,
    mode: str = "generate",
) -> str:
    """
    Build the prompt for Gemini structured output.
    """

    existing_nodes = existing_nodes or []
    existing_node_text = ", ".join(existing_nodes) if existing_nodes else "None"

    if mode == "expand":
        task = f"Expand the existing concept graph around the selected concept: {concept}."
    else:
        task = f"Create a concept graph for the AI or computer science concept: {concept}."

    return f"""
You are helping build an educational AI/CS concept map.

Task:
{task}

Existing graph nodes:
{existing_node_text}

Requirements:
1. Return a concept graph centered around "{concept}".
2. Include the central concept as one of the nodes.
3. Generate at most {max_new_nodes} new nodes.
4. Prefer concepts useful for students learning AI, machine learning, deep learning, or computer science.
5. Use clear and concise definitions.
6. Edges should represent meaningful relationships between concepts.
7. Avoid duplicate nodes from the existing graph unless needed to connect relationships.
8. Use short node IDs, such as "Transformer", "Self-Attention", or "RNN".
9. Return valid JSON only.
10. Do not include markdown.
11. Do not include any text outside the JSON.

The output must match the provided schema.
"""


def generate_concept_graph(
    concept: str,
    existing_nodes: Optional[List[str]] = None,
    max_new_nodes: int = 7,
    temperature: float = 0.2,
    model_name: str = "gemini-2.5-flash",
    mode: str = "generate",
) -> ConceptGraph:
    """
    Call Gemini and return a validated ConceptGraph object.
    """

    api_key = get_gemini_api_key()
    client = genai.Client(api_key=api_key)

    prompt = build_prompt(
        concept=concept,
        existing_nodes=existing_nodes,
        max_new_nodes=max_new_nodes,
        mode=mode,
    )

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="application/json",
            response_schema=ConceptGraph,
        ),
    )

    return ConceptGraph.model_validate_json(response.text)