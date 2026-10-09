class VertexError(Exception):
    def __init__(self, message="Vertex Error"):
        super().__init__(message)

class EdgeError(Exception):
    def __init__(self, message="Edge Error"):
        super().__init__(message)


