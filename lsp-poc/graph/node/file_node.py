from graph.node import NodeLabels
from .types.definition_node import DefinitionNode


class FileNode(DefinitionNode):
    def __init__(self, **kwargs):
        super().__init__(label=NodeLabels.FILE, **kwargs)