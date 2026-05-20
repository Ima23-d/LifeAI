from transformers import pipeline
from PIL import Image

# =========================
# FUNÇÃO DE GRAVIDADE
# =========================

def classificar_gravidade(score):

    if score < 0.30:
        return "Leve"

    elif score < 0.70:
        return "Moderada"

    else:
        return "Grave"


# =========================
# CARREGA O MODELO
# =========================

print("Carregando modelo...")

classifier = pipeline(
    "image-classification",
    model="HlexNC/chexvision-densenet"
)

print("Modelo carregado com sucesso!")


# =========================
# ABRE A IMAGEM
# =========================

imagem_path = "raiox.jpg"

image = Image.open(imagem_path).convert("RGB")


# =========================
# ANALISA A IMAGEM
# =========================

print("\nAnalisando imagem...\n")

results = classifier(image)


# =========================
# MOSTRA TODOS RESULTADOS
# =========================

print("===== TODOS OS RESULTADOS =====\n")

for r in results:

    label = r['label']
    score = r['score']

    porcentagem = score * 100

    gravidade = classificar_gravidade(score)

    print(f"Doença: {label}")
    print(f"Probabilidade: {porcentagem:.2f}%")
    print(f"Gravidade: {gravidade}")
    print("-" * 40)


# =========================
# MOSTRA APENAS DOENÇAS
# RELEVANTES
# =========================

print("\n===== DOENÇAS RELEVANTES =====\n")

encontrou = False

for r in results:

    if r['score'] > 0.40:

        encontrou = True

        label = r['label']
        score = r['score']

        porcentagem = score * 100

        gravidade = classificar_gravidade(score)

        print(f"Doença Detectada: {label}")
        print(f"Confiança: {porcentagem:.2f}%")
        print(f"Gravidade: {gravidade}")
        print("-" * 40)

if not encontrou:
    print("Nenhuma doença relevante encontrada.")


# =========================
# DOENÇA MAIS PROVÁVEL
# =========================

melhor_resultado = max(results, key=lambda x: x['score'])

print("\n===== DIAGNÓSTICO PRINCIPAL =====\n")

label = melhor_resultado['label']
score = melhor_resultado['score']

porcentagem = score * 100

gravidade = classificar_gravidade(score)

print(f"Doença Principal: {label}")
print(f"Probabilidade: {porcentagem:.2f}%")
print(f"Gravidade: {gravidade}")

print("\nAnálise finalizada!")