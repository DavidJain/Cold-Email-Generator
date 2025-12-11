import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self):
        self.client = chromadb.PersistentClient("vectorstore")
        self.collection = self.client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        df = pd.read_csv("my_portfolio.csv")

        if self.collection.count() == 0:
            for _, row in df.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        if not skills:
            return []

        result = self.collection.query(
            query_texts=skills,
            n_results=2
        )

        metadatas = result.get("metadatas", [[]])
        links = [item["links"] for item in metadatas[0]]
        return links
