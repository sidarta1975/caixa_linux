import argparse
import pandas as pd
from src.classification.preprocessor import preprocess_text
from src.classification.bm25_engine import BM25Classifier
from src.classification.parallel_runner import run_parallel

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Arquivo TSV de entrada")
    parser.add_argument("--output", required=True, help="Arquivo TSV de saída")
    args = parser.parse_args()

    df_input = pd.read_csv(args.input, sep="\t", dtype=str).fillna("")
    df_modelos = pd.read_excel("models/classif_caixa_linux.xlsx", dtype=str).fillna("")

    modelos_ids = df_modelos.iloc[:, 0].tolist()
    modelos_labels = df_modelos.iloc[:, 1].tolist()
    modelos_txt = [preprocess_text(t) for t in df_modelos.iloc[:, 2].tolist()]

    classifier = BM25Classifier(modelos_ids, modelos_labels, modelos_txt, b=0.7)
    textos_entrada = df_input.iloc[:, 7].tolist()

    resultados = run_parallel(textos_entrada, classifier, num_threads=12)

    # Garante que o DataFrame tenha ao menos 11 colunas
    while df_input.shape[1] < 11:
        df_input[df_input.shape[1]] = ""

    for i, (classificacao, modelo, score) in enumerate(resultados):
        df_input.iat[i, 8] = classificacao
        df_input.iat[i, 9] = modelo
        df_input.iat[i, 10] = score

    df_input.to_csv(args.output, sep="\t", index=False)

if __name__ == "__main__":
    main()
