import os
import torch
import numpy as np
import skimage.io
import torchvision.transforms as transforms
import torchxrayvision as xrv
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================================================
# CONFIGURAÇÕES DO SISTEMA
# ==========================================================

LIMIAR_PROBABILIDADE = 0.35  # 35% de probabilidade mínima
TOTAL_RESULTADOS = 5

DOENCAS_VALIDAS = [
    "Atelectasis",
    "Consolidation",
    "Infiltration",
    "Effusion",
    "Pneumonia",
    "Fibrosis",
    "Pleural_Thickening"
]

# Mapeamento de doenças para descrições em português
MAPEAMENTO_DOENCAS = {
    "Atelectasis": "Atelectasia (colapso alveolar)",
    "Consolidation": "Consolidação (infiltrado)",
    "Infiltration": "Infiltração pulmonar",
    "Effusion": "Derrame pleural",
    "Pneumonia": "Pneumonia",
    "Fibrosis": "Fibrose pulmonar",
    "Pleural_Thickening": "Espessamento pleural"
}

# ==========================================================
# CLASSIFICAÇÃO DE GRAVIDADE E PRIORIDADE
# ==========================================================

def classificar_gravidade(probabilidade):
    """Classifica a gravidade com base na probabilidade."""
    if probabilidade >= 0.75:
        return "Grave"
    elif probabilidade >= 0.50:
        return "Moderada"
    else:
        return "Leve"


def classificar_prioridade(probabilidade, doenca):
    """Determina o nível de prioridade."""
    # Doenças mais críticas têm prioridade mais alta
    doencas_criticas = ["Pneumonia", "Consolidation", "Effusion"]
    
    if probabilidade >= 0.80 and doenca in doencas_criticas:
        return "CRÍTICO"
    elif probabilidade >= 0.75:
        return "URGENTE"
    elif probabilidade >= 0.50:
        return "ATENÇÃO"
    else:
        return "NORMAL"


def gerar_recomendacao(doenca, probabilidade):
    """Gera recomendação médica com base na detecção."""
    recomendacoes = {
        "Pneumonia": "Encaminhamento imediato para pneumologia. Iniciar antibioticoterapia empírica conforme protocolo institucional.",
        "Consolidation": "Investigação complementar necessária. Considerar tomografia de tórax para melhor avaliação.",
        "Infiltration": "Acompanhamento clínico. Correlacionar com apresentação clínica do paciente.",
        "Effusion": "Possível derrame pleural. Avaliar indicação de ultrassom torácico.",
        "Atelectasis": "Avaliar possível colapso alveolar. Manobras de reexpansão pulmonar podem ser necessárias.",
        "Fibrosis": "Possível fibrose pulmonar. Encaminhamento para especialista recomendado.",
        "Pleural_Thickening": "Espessamento pleural detectado. Seguimento periódico recomendado."
    }
    
    return recomendacoes.get(doenca, "Correlacionar com apresentação clínica do paciente.")


# ==========================================================
# CARREGAMENTO DO MODELO
# ==========================================================

modelo_carregado = None
dispositivo = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def carregar_modelo():
    """Carrega o modelo de IA na primeira execução."""
    global modelo_carregado
    
    if modelo_carregado is not None:
        return modelo_carregado
    
    try:
        logger.info("🤖 Carregando modelo de inteligência artificial...")
        
        modelo = xrv.models.DenseNet(weights="densenet121-res224-nih")
        modelo = modelo.to(dispositivo)
        modelo.eval()
        
        logger.info("✓ Modelo carregado com sucesso!")
        modelo_carregado = modelo
        return modelo
    
    except Exception as e:
        logger.error(f"✗ Erro ao carregar modelo: {str(e)}")
        raise


# ==========================================================
# ANALISADOR DE IMAGEM
# ==========================================================

def analisar_imagem(caminho_imagem):
    """
    Analisa uma imagem de raio-X e retorna os resultados.
    
    Retorna:
    {
        'sucesso': bool,
        'doenca_principal': str,
        'probabilidade': float,
        'gravidade': str,
        'prioridade': str,
        'confianca': float,
        'recomendacao': str,
        'resultados_completos': list,
        'tempo_processamento': float,
        'erro': str (opcional)
    }
    """
    
    inicio = datetime.utcnow()
    
    try:
        # Carregar modelo
        modelo = carregar_modelo()
        
        # Carregar imagem
        logger.info(f"📥 Carregando imagem: {caminho_imagem}")
        
        if not os.path.exists(caminho_imagem):
            return {
                'sucesso': False,
                'erro': f'Arquivo não encontrado: {caminho_imagem}'
            }
        
        imagem = skimage.io.imread(caminho_imagem)
        
        # Normalizar imagem
        imagem = xrv.datasets.normalize(imagem, 255)
        
        # Converter para grayscale se necessário
        if len(imagem.shape) > 2:
            imagem = imagem.mean(2)
        
        # Adicionar canal
        imagem = imagem[None, :, :]
        
        # Aplicar transformações
        transformacoes = transforms.Compose([
            xrv.datasets.XRayCenterCrop(),
            xrv.datasets.XRayResizer(224)
        ])
        
        imagem = transformacoes(imagem)
        
        # Converter para tensor
        imagem = torch.from_numpy(imagem).float().unsqueeze(0).to(dispositivo)
        
        # Executar predição
        logger.info("🔍 Analisando imagem...")
        
        with torch.no_grad():
            saidas_modelo = modelo(imagem)
        
        saidas_modelo = saidas_modelo[0].cpu().numpy()
        
        # Processar resultados
        resultados = []
        
        for nome_doenca, probabilidade in zip(modelo.pathologies, saidas_modelo):
            if nome_doenca == "":
                continue
            
            if nome_doenca not in DOENCAS_VALIDAS:
                continue
            
            probabilidade = float(probabilidade)
            probabilidade = np.clip(probabilidade, 0, 1)
            
            if probabilidade >= LIMIAR_PROBABILIDADE:
                gravidade = classificar_gravidade(probabilidade)
                
                resultados.append({
                    'doenca': nome_doenca,
                    'doenca_pt': MAPEAMENTO_DOENCAS.get(nome_doenca, nome_doenca),
                    'probabilidade': round(probabilidade * 100, 2),
                    'gravidade': gravidade
                })
        
        # Ordenar por probabilidade
        resultados = sorted(
            resultados,
            key=lambda x: x['probabilidade'],
            reverse=True
        )
        
        tempo_processamento = (datetime.utcnow() - inicio).total_seconds()
        
        if resultados:
            doenca_principal = resultados[0]['doenca']
            probabilidade_principal = resultados[0]['probabilidade'] / 100
            prioridade = classificar_prioridade(probabilidade_principal, doenca_principal)
            recomendacao = gerar_recomendacao(doenca_principal, probabilidade_principal)
            
            logger.info(f"✓ Análise concluída: {doenca_principal} ({resultados[0]['probabilidade']}%)")
            
            return {
                'sucesso': True,
                'doenca_principal': resultados[0]['doenca_pt'],
                'doenca_original': doenca_principal,
                'probabilidade': round(probabilidade_principal * 100, 2),
                'gravidade': resultados[0]['gravidade'],
                'prioridade': prioridade,
                'confianca': round(probabilidade_principal * 100, 2),
                'recomendacao': recomendacao,
                'resultados_completos': resultados[:TOTAL_RESULTADOS],
                'tempo_processamento': round(tempo_processamento, 2)
            }
        else:
            logger.warning("⚠ Nenhuma doença detectada acima do limiar")
            
            return {
                'sucesso': True,
                'doenca_principal': 'Sem achados significativos',
                'doenca_original': 'Normal',
                'probabilidade': 0,
                'gravidade': 'Leve',
                'prioridade': 'NORMAL',
                'confianca': 0,
                'recomendacao': 'Imagem dentro dos limites normais. Acompanhamento de rotina recomendado.',
                'resultados_completos': [],
                'tempo_processamento': round(tempo_processamento, 2)
            }
    
    except Exception as e:
        logger.error(f"✗ Erro na análise: {str(e)}")
        return {
            'sucesso': False,
            'erro': str(e),
            'tempo_processamento': (datetime.utcnow() - inicio).total_seconds()
        }


if __name__ == '__main__':
    # Teste
    print("Testando carregamento do modelo...")
    modelo = carregar_modelo()
    print("✓ Modelo carregado com sucesso!")
