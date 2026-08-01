import faiss
import numpy as np


class VectorStore:


    def __init__(self):

        self.index = None
        self.documents = []



    def build(
        self,
        embeddings,
        documents
    ):

        dimension = embeddings.shape[1]


        self.index = faiss.IndexFlatIP(
            dimension
        )


        self.index.add(
            np.array(embeddings)
        )


        self.documents = documents



    def search(
        self,
        query_embedding,
        top_k=2
    ):


        scores, indexes = self.index.search(
            np.array(query_embedding),
            top_k
        )


        results=[]


        for idx in indexes[0]:

            results.append(
                self.documents[idx]
            )


        return results