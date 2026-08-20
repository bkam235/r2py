"""Parse R source via tree-sitter-language-pack, return an AstNode tree."""
from __future__ import annotations

from .entities import AstNode


def parse(source: str) -> AstNode:
    """Parse R source text and return the root AstNode."""
    import tree_sitter_language_pack as lp
    parser = lp.get_parser("r")
    src_bytes = source.encode("utf-8")
    tree = parser.parse_bytes(src_bytes)
    root_ts = tree.root_node()
    return _to_ast_node(root_ts, src_bytes)


def _to_ast_node(ts_node: object, src_bytes: bytes) -> AstNode:
    """Recursively convert a tree-sitter-language-pack Node to AstNode."""
    start_pos = ts_node.start_position()
    end_pos = ts_node.end_position()
    start_byte = ts_node.start_byte()
    end_byte = ts_node.end_byte()
    text = src_bytes[start_byte:end_byte].decode("utf-8", errors="replace")

    node = AstNode(
        kind=ts_node.kind(),
        text=text,
        start=(start_pos.row, start_pos.column),
        end=(end_pos.row, end_pos.column),
        start_byte=start_byte,
        end_byte=end_byte,
        is_named=ts_node.is_named(),
        _ts_node=ts_node,
    )
    node.children = [
        _to_ast_node(ts_node.child(i), src_bytes)
        for i in range(ts_node.child_count())
    ]
    return node
