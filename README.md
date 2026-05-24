# LifeAI

LifeAI é uma aplicação web em Flask criada para uma esteira de triagem e apoio à decisão em diagnóstico por imagem, com foco em pneumonia e outras doenças torácicas. O projeto atual já entrega a interface completa, fluxo de navegação e uma camada de demonstração, mas ainda não está integrado de ponta a ponta com um serviço de machine learning em produção.

## Infraestrutura atual

- Backend em Python com Flask, centralizado em [app.py](app.py).
- Templates HTML com Jinja2 em [templates/](templates/).
- Assets estáticos em [static/](static/), separados em CSS, JS, imagens e logos.
- Um protótipo isolado de inferência em [MODELO/V_1.py](MODELO/V_1.py), atualmente fora do fluxo web principal.
- Estado de aplicação armazenado em memória, sem banco de dados persistente.
- Sessão do usuário mantida pelo Flask apenas durante a execução local.

## Como a aplicação funciona hoje

O fluxo atual é funcional do ponto de vista de interface, mas os dados clínicos e os resultados de IA são simulados. O app autentica o usuário, leva ao painel, permite abrir novas telas de exame e lista dados de demonstração para navegação e apresentação visual.

O backend principal está em [app.py](app.py) e roda como servidor Flask local. As páginas reutilizam componentes comuns em [templates/partials/](templates/partials/) e o visual é controlado por folhas de estilo em [static/css/](static/css/). O comportamento interativo do frontend fica em [static/js/aplicativo.js](static/js/aplicativo.js).

## O que está mockado hoje

Esta é a parte que ainda simula resultados reais. Tudo abaixo deve ser tratado como demonstração, não como integração clínica final:

- Login e cadastro usam validação simples e salvam dados em memória, sem banco de dados, sem hash de senha e sem autenticação real.
- O painel principal exibe métricas fixas ou derivadas apenas da lista em memória, não de dados clínicos persistidos.
- A página de novo exame não envia a imagem para um pipeline real de inferência. Ao submeter o formulário, o backend retorna um resultado fixo de IA com urgência, risco e recomendação predefinidos.
- A API [api/analisar-exame](app.py) devolve sempre um resultado simulado, independentemente do conteúdo recebido.
- A API [api/dados-dashboard](app.py) calcula números apenas a partir da coleção em memória, que é reiniciada quando o servidor para.
- A lista de exames em [templates/exames.html](templates/exames.html) usa registros de demonstração quando não há exames reais cadastrados.
- A fila de prioridade em [templates/fila_prioridade.html](templates/fila_prioridade.html) usa uma tabela fixa de exemplos para ilustrar diferentes níveis de prioridade.
- A tela de detalhes em [app.py](app.py) possui a rota [exames/demo](app.py) para abrir exames fictícios montados via query string.
- A página de detalhes mostra um banner explícito de demonstração quando o registro vem da rota mockada.
- O frontend possui uma simulação de análise em JavaScript em [static/js/aplicativo.js](static/js/aplicativo.js), que gera resultados aleatórios, tempo de processamento falso e notificações de sucesso sem chamar um backend de IA.
- Os cards do dashboard e de relatórios exibem números e indicadores estáticos ou calculados apenas a partir dos dados temporários da sessão atual.
- O arquivo [MODELO/V_1.py](MODELO/V_1.py) é um protótipo independente de inferência com TorchXRayVision e PyTorch, mas não está integrado ao fluxo web do Flask.

## Estado do fluxo de IA

O objetivo final do projeto é comunicar a interface web com um algoritmo de machine learning capaz de analisar imagens torácicas e estimar achados como pneumonia, derrame pleural, consolidação, edema e outras alterações pulmonares.

No estado atual:

- a interface já existe e está conectada ao Flask;
- a lógica clínica ainda não consome um serviço de ML real;
- as respostas da IA são prototipadas com valores fixos ou aleatórios;
- a persistência clínica ainda não existe;
- o modelo de ML ainda não está acoplado a uma API, fila ou serviço de inferência dedicado.

## Execução local

O projeto é executado localmente com Flask. Em termos práticos, o ambiente atual usa uma virtualenv local dentro do repositório e depende das bibliotecas listadas em [requirements.txt](requirements.txt).

Fluxo típico de uso:

1. Ativar o ambiente virtual local.
2. Instalar as dependências do [requirements.txt](requirements.txt).
3. Executar [app.py](app.py).
4. Abrir a aplicação no navegador no endereço local indicado pelo Flask.

## Estrutura do projeto

- [app.py](app.py): rotas, sessão, APIs simuladas e inicialização do Flask.
- [MODELO/](MODELO/): protótipo de inferência e artefatos relacionados ao experimento de ML.
- [static/css/](static/css/): estilos da interface.
- [static/js/](static/js/): comportamentos de tela e simulações de interação.
- [static/img/](static/img/): imagens usadas na UI.
- [static/Logo/](static/Logo/): logos e imagens de marca.
- [templates/](templates/): páginas HTML do sistema.
- [templates/partials/](templates/partials/): barra lateral, barra superior e rodapé.

## Observação importante

Este README descreve o estado atual da base como ela está hoje. Assim que a integração com o algoritmo real de machine learning for implementada, as seções de simulação deverão ser atualizadas para documentar o novo fluxo clínico, a persistência dos dados e os endpoints reais de inferência.