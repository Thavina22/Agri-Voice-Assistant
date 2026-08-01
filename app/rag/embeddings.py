from sentence_transformers import SentenceTransformer


class EmbeddingService:


    def __init__(self):

        self.model = SentenceTransformer(
            "BAAI/bge-m3"
        )


    def create_embeddings(
        self,
        documents
    ):

        embeddings = self.model.encode(
            documents,
            normalize_embeddings=True
        )

        return embeddings



    def embed_query(
        self,
        query
    ):

        return self.model.encode(
            [query],
            normalize_embeddings=True
        )