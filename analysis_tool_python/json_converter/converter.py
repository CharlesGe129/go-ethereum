from analysis_tool_python.json_converter import bc_to_json, cano_uncle_to_json, forked_to_json

if __name__ == '__main__':
    bc_to_json.BroadcastToJson().start()
    cano_uncle_to_json.ApiToJson().start()
    forked_to_json.ForkedToJson().start()
