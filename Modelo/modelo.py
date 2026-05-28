import os
import torch
import numpy as np
import skimage.io
import torchvision.transforms as transforms
import torchxrayvision as xrv

# ==========================================================
# CONFIGURAÇÕES DO SISTEMA
# ==========================================================

# Probabilidade mínima para considerar uma doença
LIMIAR_PROBABILIDADE = 0.50

# Quantidade máxima de resultados exibidos
TOTAL_RESULTADOS = 5

# Doenças consideradas mais confiáveis
DOENCAS_VALIDAS = [
    "Atelectasis",
    "Consolidation",
    "Infiltration",
    "Effusion",
    "Pneumonia",
    "Fibrosis",
    "Pleural_Thickening"
]

# ==========================================================
# FUNÇÃO DE CLASSIFICAÇÃO DA GRAVIDADE
# ==========================================================

def classificar_gravidade(probabilidade):
    """
    Classifica a gravidade com base na probabilidade.
    """

    if probabilidade >= 0.75:
        return "Grave"

    elif probabilidade >= 0.50:
        return "Moderada"

    else:
        return "Leve"


# ==========================================================
# CARREGAMENTO DO MODELO DE IA
# ==========================================================

print("Carregando modelo de inteligência artificial...")

modelo = xrv.models.DenseNet(
    weights="densenet121-res224-nih"
)

# Coloca o modelo em modo de inferência
modelo.eval()

print("Modelo carregado com sucesso!")

# ==========================================================
# CAMINHO DA IMAGEM
# ==========================================================

caminho_imagem = os.path.join(
    os.path.dirname(__file__),
    "raio-x.png"
)

# ==========================================================
# LEITURA DA IMAGEM
# ==========================================================

print("Carregando imagem do raio-X...")

imagem = skimage.io.imread(caminho_imagem)

# ==========================================================
# NORMALIZAÇÃO DA IMAGEM
# ==========================================================

# Converte os pixels de 0-255 para valores normalizados
imagem = xrv.datasets.normalize(imagem, 255)

# ==========================================================
# CONVERSÃO PARA ESCALA DE CINZA
# ==========================================================

# Caso a imagem seja RGB
if len(imagem.shape) > 2:

    # Converte para grayscale
    imagem = imagem.mean(2)

# ==========================================================
# AJUSTE DO FORMATO DA IMAGEM
# ==========================================================

# Adiciona o canal da imagem
imagem = imagem[None, :, :]

# ==========================================================
# TRANSFORMAÇÕES DA IMAGEM
# ==========================================================

transformacoes = transforms.Compose([

    # Recorta o centro da imagem
    xrv.datasets.XRayCenterCrop(),

    # Redimensiona para 224x224
    xrv.datasets.XRayResizer(224)
])

imagem = transformacoes(imagem)

# ==========================================================
# CONVERSÃO PARA TENSOR
# ==========================================================

imagem = torch.from_numpy(imagem)\
    .float()\
    .unsqueeze(0)

# ==========================================================
# REALIZAR PREDIÇÃO
# ==========================================================

print("Analisando imagem...")

with torch.no_grad():

    saidas_modelo = modelo(imagem)

# Converte para numpy
saidas_modelo = saidas_modelo[0].cpu().numpy()

# ==========================================================
# PROCESSAMENTO DOS RESULTADOS
# ==========================================================

resultados = []

for nome_doenca, probabilidade in zip(
    modelo.pathologies,
    saidas_modelo
):

    # Ignora classes vazias
    if nome_doenca == "":
        continue

    # Ignora doenças fora da lista confiável
    if nome_doenca not in DOENCAS_VALIDAS:
        continue

    # Converte para float
    probabilidade = float(probabilidade)

    # Limita entre 0 e 1
    probabilidade = np.clip(
        probabilidade,
        0,
        1
    )

    # Verifica se passou do limiar
    if probabilidade >= LIMIAR_PROBABILIDADE:

        # Classifica gravidade
        gravidade = classificar_gravidade(
            probabilidade
        )

        # Adiciona ao resultado
        resultados.append({

            "doenca": nome_doenca,

            "probabilidade": probabilidade,

            "gravidade": gravidade
        })

# ==========================================================
# ORDENAR RESULTADOS
# ==========================================================

resultados = sorted(

    resultados,

    key=lambda item: item["probabilidade"],

    reverse=True
)

# ==========================================================
# EXIBIR RESULTADOS
# ==========================================================

print("\n================ RESULTADOS ================\n")

# Nenhuma doença encontrada
if len(resultados) == 0:

    print(
        "Nenhuma alteração significativa detectada."
    )

# Exibir resultados encontrados
else:

    for resultado in resultados[:TOTAL_RESULTADOS]:

        print(f"Doença: {resultado['doenca']}")

        print(
            f"Probabilidade: "
            f"{resultado['probabilidade'] * 100:.2f}%"
        )

        print(
            f"Gravidade: "
            f"{resultado['gravidade']}"
        )

        print("-" * 45)