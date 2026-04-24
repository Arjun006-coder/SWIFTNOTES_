import json

with open('graphify-out/.graphify_ast.json', 'r') as f:
    ast = json.load(f)

with open('graphify-out/.graphify_semantic.json', 'r') as f:
    semantic = json.load(f)

merged_nodes = ast['nodes'] + semantic['nodes']

merged_edges = ast['edges'] + semantic['edges']

merged = {
    'nodes': merged_nodes,
    'edges': merged_edges,
    'input_tokens': ast.get('input_tokens', 0) + semantic.get('input_tokens', 0),
    'output_tokens': ast.get('output_tokens', 0) + semantic.get('output_tokens', 0)
}

with open('graphify-out/graph.json', 'w') as f:
    json.dump(merged, f, indent=2)

print(f'Merged graph: {len(merged_nodes)} nodes, {len(merged_edges)} edges')