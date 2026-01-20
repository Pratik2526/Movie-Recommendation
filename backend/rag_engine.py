import pandas as pd
import ast
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class MovieRAG:
    def __init__(self, csv_path):
        self.movies = pd.read_csv(csv_path, low_memory=False)
        self.movies = self.movies[['title', 'overview', 'genres']]
        self.movies.dropna(inplace=True)
        self.movies = self.movies.head(5000)

        self.movies['genres_text'] = self.movies['genres'].apply(self.extract_genres)
        self.movies['content'] = self.movies['overview'] + " " + self.movies['genres_text']

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        # Reset index to avoid KeyError when accessing by position
        self.movies = self.movies.reset_index(drop=True)
        self.embeddings = self.model.encode(self.movies['content'], show_progress_bar=True)

        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(np.array(self.embeddings))

    def extract_genres(self, genres):
        genres = ast.literal_eval(genres)
        return " ".join([g['name'] for g in genres])

    def search(self, query, k=5):
        q_emb = self.model.encode([query])
        _, idx = self.index.search(np.array(q_emb), k)
        return self.movies.iloc[idx[0]]
