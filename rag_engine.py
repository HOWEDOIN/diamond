from typing import List, Dict

try:
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
except ImportError:  # placeholders if packages aren't installed
    SentenceTransformer = None
    faiss = None
    np = None


class RAGEngine:
    """Simple retrieval engine using embeddings if available, else substring search."""

    def __init__(self, bible: Dict[str, Dict[str, List[str]]]):
        self.bible = bible
        self.verses = []  # list of (text, ref)
        for book, chapters in bible.items():
            for ch, verses in chapters.items():
                for i, verse in enumerate(verses, 1):
                    self.verses.append((verse, f"{book} {ch}:{i}"))
        self.index = None
        if SentenceTransformer and faiss:
            self.model = SentenceTransformer('BAAI/bge-m3')
            embeddings = [self.model.encode(v[0]) for v in self.verses]
            dim = len(embeddings[0])
            self.index = faiss.IndexFlatL2(dim)
            self.index.add(np.array(embeddings).astype('float32'))

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        if self.index is not None:
            q_emb = self.model.encode(query)
            dists, idxs = self.index.search(np.array([q_emb]).astype('float32'), top_k)
            return [
                {'reference': self.verses[i][1], 'text': self.verses[i][0]}
                for i in idxs[0]
            ]
        # Fallback substring search
        results = [
            {'reference': ref, 'text': verse}
            for verse, ref in self.verses
            if query.lower() in verse.lower()
        ]
        return results[:top_k]
