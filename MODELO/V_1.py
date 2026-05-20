import torch
import torchxrayvision as xrv
import skimage.io
import torchvision.transforms as transforms

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
# CARREGA MODELO
# =========================

print("Carregando modelo...")

model = xrv.models.DenseNet(weights="densenet121-res224-nih")

print("Modelo carregado!")


# =========================
# CARREGA IMAGEM
# =========================

img = skimage.io.imread("raiox.jpg")

# Converte para escala cinza
img = xrv.datasets.normalize(img, 255)

if len(img.shape) > 2:
    img = img.mean(2)

img = img[None, :, :]

transform = transforms.Compose([
    xrv.datasets.XRayCenterCrop(),
    xrv.datasets.XRayResizer(224)
])

img = transform(img)

img = torch.from_numpy(img).unsqueeze(0)


# =========================
# FAZ PREDIÇÃO
# =========================

outputs = model(img)

results = dict(zip(model.pathologies, outputs[0].detach().numpy()))

print("\n===== RESULTADOS =====\n")

for pathology, score in results.items():

    score = float(score)

    if score > 0.4:

        gravidade = classificar_gravidade(score)

        print(f"Doença: {pathology}")
        print(f"Probabilidade: {score*100:.2f}%")
        print(f"Gravidade: {gravidade}")
        print("-" * 40)
