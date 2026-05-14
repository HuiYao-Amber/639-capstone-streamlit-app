import html
from typing import Dict, List, Optional, Tuple

from pyvis.network import Network

from schemas import ConceptGraph, ConceptNode, ConceptEdge


CATEGORY_COLORS = {
    "architecture": "#9ecae1",
    "model": "#a1d99b",
    "method": "#fdae6b",
    "task": "#fdd0a2",
    "dataset": "#c7b9e8",
    "paper": "#f2b6c6",
    "evaluation": "#bcbddc",
    "math": "#c7e9c0",
    "system": "#bdbdbd",
    "application": "#fdd49e",
    "other": "#d9d9d9",
}


def normalize_node_id(node_id: str) -> str:
    return " ".join(node_id.strip().split())


def merge_graphs(
    existing: Optional[ConceptGraph],
    new: ConceptGraph,
) -> ConceptGraph:
    """
    Merge a new concept graph into the existing graph.
    """

    if existing is None:
        return new

    node_map: Dict[str, ConceptNode] = {}

    for node in existing.nodes + new.nodes:
        clean_id = normalize_node_id(node.id)
        key = clean_id.lower()

        node_map[key] = ConceptNode(
            id=clean_id,
            definition=node.definition.strip(),
            category=node.category.strip().lower() if node.category else "other",
        )

    edge_map: Dict[Tuple[str, str, str], ConceptEdge] = {}

    for edge in existing.edges + new.edges:
        source = normalize_node_id(edge.source)
        target = normalize_node_id(edge.target)
        relation = edge.relation.strip()

        if source.lower() in node_map and target.lower() in node_map:
            key = (source.lower(), target.lower(), relation.lower())
            edge_map[key] = ConceptEdge(
                source=node_map[source.lower()].id,
                target=node_map[target.lower()].id,
                relation=relation,
                explanation=edge.explanation.strip(),
            )

    suggestions = []
    seen = set()

    for item in existing.suggested_concepts + new.suggested_concepts:
        clean = normalize_node_id(item)
        key = clean.lower()
        if key and key not in seen and key not in node_map:
            suggestions.append(clean)
            seen.add(key)

    return ConceptGraph(
        center=existing.center,
        nodes=list(node_map.values()),
        edges=list(edge_map.values()),
        suggested_concepts=suggestions[:12],
    )


def get_node_names(graph: ConceptGraph) -> List[str]:
    return sorted([node.id for node in graph.nodes])


def get_node_by_id(graph: ConceptGraph, node_id: str) -> Optional[ConceptNode]:
    for node in graph.nodes:
        if node.id == node_id:
            return node
    return None


def get_neighbor_edges(graph: ConceptGraph, node_id: str) -> List[ConceptEdge]:
    return [
        edge
        for edge in graph.edges
        if edge.source == node_id or edge.target == node_id
    ]


def category_color(category: str) -> str:
    return CATEGORY_COLORS.get(category.lower().strip(), CATEGORY_COLORS["other"])


def graph_to_html(
    graph: ConceptGraph,
    selected_node: Optional[str] = None,
    height: str = "620px",
) -> str:
    """
    Convert a ConceptGraph into an interactive pyvis HTML graph.
    """

    net = Network(
        height=height,
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="#222222",
        cdn_resources="in_line",
    )

    net.barnes_hut(
        gravity=-2500,
        central_gravity=0.3,
        spring_length=140,
        spring_strength=0.03,
        damping=0.09,
    )

    for node in graph.nodes:
        is_center = node.id == graph.center
        is_selected = node.id == selected_node

        size = 34 if is_center else 28
        if is_selected:
            size = 38

        color = "#ffcc66" if is_center else category_color(node.category)
        if is_selected:
            color = "#ff9999"

        title = (
            f"<b>{html.escape(node.id)}</b><br>"
            f"<i>{html.escape(node.category)}</i><br><br>"
            f"{html.escape(node.definition)}"
        )

        net.add_node(
            node.id,
            label=node.id,
            title=title,
            color=color,
            size=size,
            borderWidth=3 if is_selected else 1,
        )

    valid_nodes = {node.id for node in graph.nodes}

    for edge in graph.edges:
        if edge.source in valid_nodes and edge.target in valid_nodes:
            edge_title = (
                f"<b>{html.escape(edge.relation)}</b><br>"
                f"{html.escape(edge.explanation)}"
            )

            net.add_edge(
                edge.source,
                edge.target,
                label=edge.relation,
                title=edge_title,
                arrows="to",
            )

    net.set_options(
        """
        var options = {
          "nodes": {
            "shape": "dot",
            "font": {
              "size": 16,
              "face": "arial"
            }
          },
          "edges": {
            "font": {
              "size": 12,
              "align": "middle"
            },
            "color": {
              "color": "#888888",
              "highlight": "#333333"
            },
            "smooth": {
              "type": "dynamic"
            }
          },
          "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": true
          },
          "physics": {
            "enabled": true,
            "stabilization": {
              "iterations": 150
            }
          }
        }
        """
    )

    return net.generate_html(notebook=False)