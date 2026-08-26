from pathlib import Path
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class KnowledgeBase:

    def __init__(self, folder="knowledge-base"):
        self.folder = Path(folder)
        self.documents = []
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = None
        self.load_documents()

    def load_documents(self):
        for file_path in sorted(self.folder.glob("*.md")):
            text = file_path.read_text(encoding="utf-8")

            sections = re.split(r"\n(?=#{1,6}\s)", text)

            for section in sections:
                section = section.strip()

                if not section:
                    continue

                lines = section.splitlines()
                heading = "General"

                for line in lines:
                    if line.startswith("#"):
                        heading = line.lstrip("#").strip()
                        break

                self.documents.append({
                    "filename": file_path.name,
                    "heading": heading,
                    "content": section
                })

        if not self.documents:
            raise RuntimeError("No Markdown files found in knowledge-base/")

        texts = [document["content"] for document in self.documents]
        self.matrix = self.vectorizer.fit_transform(texts)

    def retrieve(self, query, top_k=5):
        if not query.strip():
            return []

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.matrix
        )[0]

        ranked = []

        for index, score in enumerate(scores):

            if score <= 0:
                continue

            document = self.documents[index].copy()
            filename = document["filename"].lower()

            if "current" in filename:
                score += 0.15
            elif "legacy" in filename:
                score -= 0.10
            elif "internal" in filename:
                score -= 0.15

            document["score"] = float(score)
            ranked.append(document)

        ranked.sort(
            key=lambda document: document["score"],
            reverse=True
        )

        return ranked[:top_k]
