from app.rag.vector_store import VectorStore



class Retriever:


    def __init__(self):

        self.vector_store = VectorStore()



    def search(
        self,
        query
    ):

        db = (
            self.vector_store
            .load_database()
        )


        results = db.similarity_search(
            query,
            k=3
        )


        context = "\n\n".join(
            [
                doc.page_content
                for doc in results
            ]
        )


        return context