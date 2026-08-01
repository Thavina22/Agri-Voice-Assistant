import json
import os


class KnowledgeBase:


    def __init__(self):

        self.path = (
            "app/data/"
            "agriculture_knowledge.json"
        )


    def load(self):

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)



    def convert_to_text(self):

        data = self.load()

        documents = []


        for item in data:

            text = f"""
Crop:
{item['crop']}

Disease:
{item['disease']}

Symptoms:
{', '.join(item['symptoms'])}

Cause:
{item['cause']}

Treatment:
{', '.join(item['treatment'])}

Prevention:
{', '.join(item['prevention'])}
"""


            documents.append(text)


        return documents