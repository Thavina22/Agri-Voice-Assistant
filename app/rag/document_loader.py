import os

from langchain_community.document_loaders import TextLoader


class DocumentLoader:

    def __init__(self):
        self.path = "app/documents/agriculture_docs"


    def load_documents(self):

        documents = []

        if not os.path.exists(self.path):
            raise FileNotFoundError(
                f"Document folder not found: {self.path}"
            )


        for file in os.listdir(self.path):

            if file.endswith(".txt"):

                file_path = os.path.join(
                    self.path,
                    file
                )

                loader = TextLoader(
                    file_path,
                    encoding="utf-8"
                )

                docs = loader.load()

                documents.extend(docs)


        return documents