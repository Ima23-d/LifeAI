import torch
import torchxrayvision as xrv
import skimage.io
import torchvision.transforms as transforms
import numpy as np
import os

# ==========================================
# CONFIGURAÇÃO
# ==========================================

THRESHOLD = 0.50
TOP_K = 5

# Classes mais confiáveis
VALID_PATHOLOGIES = [
    "Atelectasis",
    "Consolidation",
    "Infiltration",
    "Effusion",
    "Pneumonia",
    "Fibrosis",
    "Pleural_Thickening"
]

# ==========================================
# GRAVIDADE
# ==========================================

def classificar_gravidade(score):

    if score >= 0.75:
        return "Grave"

    elif score >= 0.50:
        return "Moderada"

    else:
        return "Leve"

# ==========================================
# CARREGAR MODELO
# ==========================================

print("Carregando modelo...")

model = xrv.models.DenseNet(
    weights="densenet121-res224-nih"
)

model.eval()

print("Modelo carregado!")

# ==========================================
# CARREGAR IMAGEM
# ==========================================

img_path = os.path.join(
    os.path.dirname(__file__),
    "raio-x.png"
)

img = skimage.io.imread(img_path)

# normalização correta
img = xrv.datasets.normalize(img, 255)

# converter para escala cinza
if len(img.shape) > 2:
    img = img.mean(2)

# formato correto
img = img[None, :, :]

# preprocessamento
transform = transforms.Compose([
    xrv.datasets.XRayCenterCrop(),
    xrv.datasets.XRayResizer(224)
])

img = transform(img)

# tensor
img = torch.from_numpy(img).float().unsqueeze(0)

# ==========================================
# PREDIÇÃO
# ==========================================

with torch.no_grad():

    outputs = model(img)

# IMPORTANTE:
# Algumas versões do TorchXRayVision
# já retornam probabilidades.
# Então NÃO aplicar sigmoid novamente.

outputs = outputs[0].cpu().numpy()

# ==========================================
# RESULTADOS
# ==========================================

results = []

for pathology, score in zip(model.pathologies, outputs):

    # ignorar classes vazias
    if pathology == "":
        continue

    # ignorar classes pouco confiáveis
    if pathology not in VALID_PATHOLOGIES:
        continue

    score = float(score)

    # limitar valores
    score = np.clip(score, 0, 1)

    if score >= THRESHOLD:

        gravidade = classificar_gravidade(score)

        results.append({
            "doenca": pathology,
            "probabilidade": score,
            "gravidade": gravidade
        })

# ordenar
results = sorted(
    results,
    key=lambda x: x["probabilidade"],
    reverse=True
)

# ==========================================
# EXIBIR RESULTADOS
# ==========================================

print("\n===== RESULTADOS =====\n")

if len(results) == 0:

    print("Nenhuma alteração significativa detectada.")

else:

    for item in results[:TOP_K]:

        print(f"Doença: {item['doenca']}")
        print(
            f"Probabilidade: "
            f"{item['probabilidade']*100:.2f}%"
        )
        print(f"Gravidade: {item['gravidade']}")
        print("-" * 40)
