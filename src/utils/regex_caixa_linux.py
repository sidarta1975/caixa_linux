import argparse
import pandas as pd
import re
from datetime import datetime

REGEX_FILE = "models/regex_caixa_linux.txt"

def carregar_regex():
    print("[1/5] Carregando parâmetros regex...")
    padroes = []
    with open(REGEX_FILE, "r", encoding="utf-8") as f:
        for linha in f:
            if "##" in linha:
                expr, _ = linha.split("##", 1)
            else:
                expr = linha.strip()
            if expr:
                padroes.append(expr.strip())
    print(f"→ {len(padroes)} padrões carregados com sucesso.")
    return padroes

def aplicar_regex(texto, padroes):
    if not isinstance(texto, str):
        return ""
    resultado = texto
    for padrao in padroes:
        try:
            resultado = re.sub(padrao, "", resultado, flags=re.IGNORECASE)
        except re.error as e:
            print(f"[ERRO] Regex inválida: {padrao} — {e}")
    return resultado.strip()

def main():
    start_time = datetime.now()
    print(f"[INÍCIO] {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Arquivo TSV de entrada")
    parser.add_argument("--output", required=True, help="Arquivo TSV de saída")
    args = parser.parse_args()

    print("[2/5] Carregando arquivo de entrada...")
    df = pd.read_csv(args.input, sep="\t", dtype=str).fillna("")
    print(f"→ {len(df)} linhas carregadas.")

    while df.shape[1] <= 7:
        df[df.shape[1]] = ""

    padroes = carregar_regex()

    print("[3/5] Aplicando expressões regulares...")
    textos_originais = df.iloc[:, 6].tolist()
    textos_limpos = [aplicar_regex(t, padroes) for t in textos_originais]

    print("[4/5] Gravando resultados na coluna H...")
    for i, texto in enumerate(textos_limpos):
        df.iat[i, 7] = texto

    print("[5/5] Salvando arquivo de saída...")
    df.to_csv(args.output, sep="\t", index=False)
    print(f"→ Arquivo salvo em: {args.output}")

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"[FIM] {end_time.strftime('%Y-%m-%d %H:%M:%S')} | Duração total: {duration:.2f} segundos")

if __name__ == "__main__":
    main()
