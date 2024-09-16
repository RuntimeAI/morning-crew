from mindsdb_sdk import MindsDB
from config.settings import (
    MINDSDB_API_KEY,
    MINDSDB_NAME,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB
)

class MindsDBWrapper:
    def __init__(self):
        self.server = MindsDB(login=MINDSDB_API_KEY)
        self.project = self.server.get_or_create_project(MINDSDB_NAME)
        self._setup_database()

    def _setup_database(self):
        # Create the document_embeddings table if it doesn't exist
        self.project.query("""
        CREATE TABLE IF NOT EXISTS document_embeddings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            file_path TEXT,
            content TEXT,
            embedding FLOAT[],
            metadata JSON
        );
        """)

    def store_embedding(self, file_path: str, content: str, embedding: list, metadata: dict):
        query = f"""
        INSERT INTO document_embeddings (file_path, content, embedding, metadata)
        VALUES ('{file_path}', '{content}', ARRAY{embedding}, '{json.dumps(metadata)}');
        """
        self.project.query(query)

    def search_similar_documents(self, query_embedding: list, limit: int = 5):
        query = f"""
        SELECT file_path, content, metadata,
               cosine_similarity(embedding, ARRAY{query_embedding}) as similarity
        FROM document_embeddings
        ORDER BY similarity DESC
        LIMIT {limit};
        """
        return self.project.query(query)

    def get_document(self, file_path: str):
        query = f"""
        SELECT * FROM document_embeddings
        WHERE file_path = '{file_path}'
        LIMIT 1;
        """
        result = self.project.query(query)
        return result.fetch() if result else None

    def update_document(self, file_path: str, content: str, embedding: list, metadata: dict):
        query = f"""
        UPDATE document_embeddings
        SET content = '{content}',
            embedding = ARRAY{embedding},
            metadata = '{json.dumps(metadata)}'
        WHERE file_path = '{file_path}';
        """
        self.project.query(query)

    def delete_document(self, file_path: str):
        query = f"""
        DELETE FROM document_embeddings
        WHERE file_path = '{file_path}';
        """
        self.project.query(query)

    def get_collection_stats(self):
        query = "SELECT COUNT(*) as count FROM document_embeddings;"
        result = self.project.query(query)
        return {"count": result.fetch()[0]['count'], "name": "document_embeddings"}

