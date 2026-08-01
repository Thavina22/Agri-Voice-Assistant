from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings


class VectorStore:


    def __init__(self):

        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=
            "BAAI/bge-m3"
        )


        self.db = None



    def create_database(
        self,
        documents
    ):

        self.db = Chroma.from_documents(
            documents,
            self.embeddings,
            persist_directory=
            "app/vector_db"
        )


        return self.db



    def load_database(self):

        self.db = Chroma(
            persist_directory=
            "app/vector_db",
            embedding_function=
            self.embeddings
        )


        return self.db