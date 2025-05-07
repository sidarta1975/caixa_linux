from rank_bm25 import BM25Okapi

class BM25Classifier:
    def __init__(self, ids, labels, docs, b=0.7):
        self.ids = ids
        self.labels = labels
        self.docs = docs
        self.bm25 = BM25Okapi(docs, b=b)

    def classify(self, tokens):
        scores = self.bm25.get_scores(tokens)
        top_score = max(scores)
        idxs = [i for i, s in enumerate(scores) if s == top_score and s >= 0.8 * max(scores)]
        if top_score < 0.8:
            return ("n/a", "n/a", "n/a")

        nomes = [self.labels[i] for i in idxs]
        textos = [" ".join(self.docs[i]) for i in idxs]
        max_possible = sum(self.bm25.idf.values())
        percentual = round((top_score / max_possible) * 100, 2) if max_possible else 0

        return (
            " | ".join(nomes),
            " | ".join(textos),
            percentual
        )

