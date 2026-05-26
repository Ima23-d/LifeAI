# Sistema de Diagnóstico Pulmonar com IA

Sistema de Inteligência Artificial desenvolvido em Python para análise de radiografias de tórax utilizando Deep Learning e visão computacional médica.

O projeto utiliza a biblioteca TorchXRayVision juntamente com uma rede neural convolucional DenseNet121 treinada em milhares de imagens médicas do dataset NIH ChestX-ray.

---

# Funcionalidades

- Análise automática de imagens de raio-X
- Detecção de possíveis doenças pulmonares
- Classificação por probabilidade
- Classificação de gravidade
- Filtragem de doenças mais confiáveis
- Pré-processamento automático da imagem
- Ordenação dos diagnósticos mais prováveis

---

# Tecnologias Utilizadas

| Tecnologia | Função |
|---|---|
| Python | Linguagem principal |
| PyTorch | Framework de Deep Learning |
| TorchXRayVision | Modelos médicos para raio-X |
| NumPy | Manipulação matemática |
| scikit-image | Leitura de imagens |
| torchvision | Transformações de imagem |

---

# Doenças Detectadas

O sistema foi configurado para detectar:

| Doença | Descrição |
|---|---|
| Atelectasis | Colapso parcial do pulmão |
| Consolidation | Consolidação pulmonar |
| Infiltration | Infiltração pulmonar |
| Effusion | Líquido pleural |
| Pneumonia | Pneumonia |
| Fibrosis | Fibrose pulmonar |
| Pleural_Thickening | Espessamento pleural |

---

# Modelo de Inteligência Artificial

O projeto utiliza a arquitetura:

## DenseNet121

Treinada no dataset:

## NIH ChestX-ray

Modelo utilizado:

```python
weights="densenet121-res224-nih"
```

A rede neural é especializada em:

- reconhecimento de padrões pulmonares
- análise de densidades
- detecção de manchas
- identificação de alterações torácicas
- análise automática de radiografias

---

# Fluxo do Algoritmo

```text
Imagem de Raio-X
        ↓
Pré-processamento
        ↓
Normalização
        ↓
Redimensionamento
        ↓
Rede Neural DenseNet121
        ↓
Predição das Doenças
        ↓
Filtragem
        ↓
Classificação da Gravidade
        ↓
Resultado Final
```

---

# Estrutura do Projeto

```text
projeto/
│
├── main.py
├── raio-x.png
├── requirements.txt
└── README.md
```

---

# Instalação

## 1. Clone o repositório

```bash
git clone https://github.com/seu-repositorio/projeto-raio-x.git
```

---

## 2. Entre na pasta

```bash
cd projeto-raio-x
```

---

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

# Dependências

```txt
torch
torchvision
torchxrayvision
numpy
scikit-image
```

---

# Como Executar

Coloque sua imagem de raio-X na pasta do projeto com o nome:

```text
raio-x.png
```

Depois execute:

```bash
python main.py
```

---

# Exemplo de Resultado

```text
===== RESULTADOS =====

Doença: Pneumonia
Probabilidade: 84.32%
Gravidade: Grave
--------------------------------

Doença: Effusion
Probabilidade: 63.11%
Gravidade: Moderada
--------------------------------
```

---

# Configurações do Sistema

## Limite mínimo de confiança

```python
THRESHOLD = 0.50
```

Apenas doenças com probabilidade maior que 50% serão exibidas.

---

## Quantidade máxima de resultados

```python
TOP_K = 5
```

Mostra apenas os 5 diagnósticos mais prováveis.

---

# Pré-processamento da Imagem

O sistema realiza automaticamente:

## Normalização

Converte pixels:

```text
0-255 → 0-1
```

---

## Conversão para grayscale

Transforma imagens RGB em escala de cinza.

---

## Center Crop

Remove áreas desnecessárias da imagem.

---

## Resize

Redimensiona para:

```text
224x224
```

Formato esperado pela DenseNet121.

---

# Classificação da Gravidade

| Probabilidade | Gravidade |
|---|---|
| ≥ 75% | Grave |
| ≥ 50% | Moderada |
| < 50% | Leve |

---

# Tipo de Inteligência Artificial

O sistema utiliza:

## Deep Learning

Mais especificamente:

## CNN — Convolutional Neural Network

As CNNs conseguem:

- detectar padrões complexos
- identificar alterações pulmonares
- aprender automaticamente com imagens médicas

---

# Pontos Fortes

- Análise rápida
- Automatização da triagem médica
- Fácil utilização
- Código simples e organizado
- Open Source
- Baseado em IA médica real

---

# Limitações

Este sistema:

- NÃO substitui médicos
- pode gerar falsos positivos
- pode gerar falsos negativos
- depende da qualidade da imagem
- é apenas apoio clínico

---

# Melhorias Futuras

Possíveis melhorias:

- Interface gráfica
- Upload de imagens
- Heatmap com Grad-CAM
- Histórico de exames
- Dashboard médico
- Treinamento personalizado
- Integração com banco de dados
- API REST
- Aplicativo mobile

---

# Conceitos Envolvidos

- Inteligência Artificial
- Deep Learning
- Redes Neurais Convolucionais
- Visão Computacional
- Radiologia Computacional
- Processamento de Imagens Médicas

---

# Autor

Projeto desenvolvido para estudos em:

- Inteligência Artificial
- Diagnóstico Médico Assistido por IA
- Deep Learning aplicado à saúde
- Visão computacional médica

---

# Licença

Este projeto possui finalidade educacional e de pesquisa.

Não deve ser utilizado como diagnóstico médico oficial.

---
