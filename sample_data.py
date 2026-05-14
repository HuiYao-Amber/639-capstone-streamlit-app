from schemas import ConceptGraph, ConceptNode, ConceptEdge


def get_sample_graph() -> ConceptGraph:
    return ConceptGraph(
        center="Transformer",
        nodes=[
            ConceptNode(
                id="Transformer",
                definition=(
                    "A Transformer is a neural network architecture that uses attention mechanisms "
                    "to model relationships between tokens in a sequence."
                ),
                category="architecture",
            ),
            ConceptNode(
                id="Attention Mechanism",
                definition=(
                    "An attention mechanism allows a model to assign different weights to different "
                    "parts of the input when producing an output."
                ),
                category="method",
            ),
            ConceptNode(
                id="Self-Attention",
                definition=(
                    "Self-attention is an attention mechanism where each token attends to other tokens "
                    "within the same input sequence."
                ),
                category="method",
            ),
            ConceptNode(
                id="Multi-Head Attention",
                definition=(
                    "Multi-head attention runs several attention operations in parallel so the model "
                    "can capture different types of relationships."
                ),
                category="method",
            ),
            ConceptNode(
                id="Positional Encoding",
                definition=(
                    "Positional encoding adds information about token order because the Transformer "
                    "architecture itself does not process tokens sequentially."
                ),
                category="method",
            ),
            ConceptNode(
                id="RNN",
                definition=(
                    "A recurrent neural network processes sequences step by step, maintaining a hidden "
                    "state across time steps."
                ),
                category="architecture",
            ),
            ConceptNode(
                id="NLP",
                definition=(
                    "Natural language processing is a field of AI focused on computational methods "
                    "for understanding and generating human language."
                ),
                category="application",
            ),
        ],
        edges=[
            ConceptEdge(
                source="Transformer",
                target="Attention Mechanism",
                relation="uses",
                explanation="The Transformer relies on attention to model dependencies between tokens.",
            ),
            ConceptEdge(
                source="Attention Mechanism",
                target="Self-Attention",
                relation="includes",
                explanation="Self-attention is a specific form of attention used inside Transformers.",
            ),
            ConceptEdge(
                source="Transformer",
                target="Multi-Head Attention",
                relation="contains",
                explanation="Multi-head attention is one of the core components of Transformer layers.",
            ),
            ConceptEdge(
                source="Transformer",
                target="Positional Encoding",
                relation="uses",
                explanation="Positional encoding helps the Transformer represent token order.",
            ),
            ConceptEdge(
                source="Transformer",
                target="RNN",
                relation="improves upon",
                explanation="Transformers reduce the need for sequential recurrence used in RNNs.",
            ),
            ConceptEdge(
                source="Transformer",
                target="NLP",
                relation="is widely used in",
                explanation="Transformers are widely used for language modeling and other NLP tasks.",
            ),
        ],
        suggested_concepts=[
            "Encoder-Decoder Architecture",
            "BERT",
            "GPT",
            "Query-Key-Value",
            "Large Language Model",
        ],
    )