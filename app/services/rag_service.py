import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer

class RAGService:
    def __init__(self):
        path = os.path.join("app", "data", "knowledge.txt")
        with open(path, "r", encoding="utf-8") as f:
            self.knowledge = [line.strip() for line in f if line.strip()]

        self.model = None
        self.index = None

    def load(self):
        if self.model is None:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            embeddings = self.model.encode(self.knowledge)
            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dim)
            self.index.add(np.array(embeddings))

    def search(self, question: str):

        q = question.lower().strip()

        # -----------------------
        # HARD KEYWORD RULES
        # -----------------------

        # -----------------------------------
        # GREETINGS HANDLER
        # -----------------------------------
        greetings = ["hello", "hi", "hey", "namaste", "good morning", "good evening"]
        if any(g in q for g in greetings):
            return "Hello! How can I assist you today regarding Dr. Pooja’s Rehab & Therapy Clinic?"


        # Address
        if "address" in q or "location" in q or "where" in q:
            for line in self.knowledge:
                if "address:" in line.lower():
                    return line

        # Phone
        if "phone" in q or "contact" in q or "call" in q or "number" in q:
            for line in self.knowledge:
                if "phone:" in line.lower():
                    return line

        # Clinic name
        if "clinic" in q or "name" in q:
            for line in self.knowledge:
                if "clinic name:" in line.lower():
                    return line

        # Timings
        if "time" in q or "timing" in q or "hours" in q or "open" in q:
            for line in self.knowledge:
                if "clinic timings:" in line.lower():
                    return line

        # About doctor
        if "about" in q or "doctor" in q or "pooja" in q or "who is" in q:
            for line in self.knowledge:
                if "about dr." in line.lower():
                    return line

        # Work experience
        if "experience" in q or "worked" in q or "hospital" in q:
            for line in self.knowledge:
                if "work experience:" in line.lower():
                    return line

        # Certifications
        if "certification" in q or "qualified" in q or "degree" in q:
            for line in self.knowledge:
                if "certifications:" in line.lower():
                    return line

        # Treatments
        if "treat" in q or "therapy" in q or "services" in q:
            for line in self.knowledge:
                if "treatments:" in line.lower():
                    return line

        # -----------------------
        # FALLBACK: FAISS SEARCH
        # -----------------------
        self.load()
        q_vec = self.model.encode([question])
        D, I = self.index.search(np.array(q_vec), 1)

        threshold = 1.30
        if D[0][0] > threshold:
            return None

        return self.knowledge[I[0][0]]
