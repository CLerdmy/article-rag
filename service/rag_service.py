class RAGService:
    def __init__(self, config):
        self.config = config

    def ingest(self, file):
        return f"received file: {file.filename}"

    def query(self, query: str) -> str:
        return f"mock answer for: {query}"