from multiprocessing import Pool
from tqdm import tqdm
from src.classification.preprocessor import preprocess_text

def classify_line(args):
    text, classifier = args
    if not text.strip():
        return ("n/a", "n/a", "n/a")
    tokens = preprocess_text(text)
    return classifier.classify(tokens)

def run_parallel(texts, classifier, num_threads=12):
    with Pool(processes=num_threads) as pool:
        return list(tqdm(pool.imap(classify_line, [(t, classifier) for t in texts]), total=len(texts)))
