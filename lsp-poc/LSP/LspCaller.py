import websockets.sync.client as ws
import json


class LspCaller:
    def __init__(self, host="localhost", port=5000, root_uri=None):
        self.host = host
        self.port = port
        self.root_uri = root_uri
        self.websocket = None
        self.cache = {}

    def connect(self):
        uri = f"ws://{self.host}:{self.port}"
        self.websocket = ws.connect(uri)

    def initialize(self):
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "processId": None,
                "rootUri": self.root_uri,
                "capabilities": {},
            },
        }
        self.send_request(initialize_request)

    def send_request(self, request):
        req_key = (request["method"], json.dumps(request["params"]))

        if req_key in self.cache:
            return self.cache[req_key]

        self.websocket.send(json.dumps(request))
        response = self.websocket.recv()
        response = json.loads(response)

        self.cache[req_key] = response
        return response

    def get_document_symbols(self, document_uri):
        document_symbol_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "textDocument/documentSymbol",
            "params": {"textDocument": {"uri": document_uri}},
        }
        return self.send_request(document_symbol_request).get("result")

    def get_definition(self, document_uri, position):
        definition_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "textDocument/definition",
            "params": {
                "textDocument": {"uri": document_uri},
                "position": position,
            },
        }

        result = self.send_request(definition_request).get("result")
        if result:
            return result[0]
        return None

    def get_declaration(self, document_uri, position):
        declaration_request = {
            "jsonrpc": "2.0",
            "id": 9,
            "method": "textDocument/declaration",
            "params": {
                "textDocument": {"uri": document_uri},
                "position": position,
            },
        }
        result = self.send_request(declaration_request).get("result")
        if result:
            return result[0]
        return None

    def get_references(self, document_uri, position):
        reference_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "textDocument/references",
            "params": {
                "textDocument": {"uri": document_uri},
                "position": position,
                "context": {"includeDeclaration": False},
            },
        }
        return self.send_request(reference_request).get("result")

    def get_selection_range(self, document_uri, position):
        selection_range_request = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "textDocument/selectionRange",
            "params": {
                "textDocument": {"uri": document_uri},
                "position": position,
            },
        }
        return self.send_request(selection_range_request).get("result")

    def get_document_link(self, document_uri):
        document_link_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "textDocument/documentLink",
            "params": {"textDocument": {"uri": document_uri}},
        }
        return self.send_request(document_link_request).get("result")

    def shutdown_exit_close(self):
        self.shutdown()
        self.exit()
        self.close()

    def shutdown(self):
        shutdown_request = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "shutdown",
            "params": None,
        }
        self.send_request(shutdown_request)

    def exit(self):
        exit_request = {"jsonrpc": "2.0", "method": "exit"}
        self.websocket.send(json.dumps(exit_request))

    def close(self):
        self.websocket.close()


def pretty_print(data):
    print(json.dumps(data, indent=2))


def main():
    lsp_caller = LspCaller(root_uri="file:///home/juan/devel/blar/git-webhook-tester")
    lsp_caller.connect()

    try:
        lsp_caller.initialize()
        document_uri = "file:///home/juan/devel/blar/git-webhook-tester/class1.py"

        document_symbols = lsp_caller.get_document_symbols(document_uri)

        definitions = lsp_caller.get_definition(
            document_uri, {"line": 7, "character": 8}
        )

        references = lsp_caller.get_references(
            document_uri, {"line": 7, "character": 8}
        )

        declaration = lsp_caller.get_declaration(
            document_uri, {"line": 7, "character": 8}
        )

        print("Document symbols:")
        pretty_print(document_symbols)

        print("Definitions:")
        pretty_print(definitions)

        print("References:")
        pretty_print(references)

        print("Declaration:")
        pretty_print(declaration)

        # print("Selection range:")
        # pretty_print(selection_range)

    finally:
        lsp_caller.shutdown_exit_close()


if __name__ == "__main__":
    main()
