# LifeAI - Plataforma de Análise de Imagens Médicas com IA

Uma plataforma web completa para análise automatizada de radiografias de tórax usando inteligência artificial com Deep Learning.

## 🎯 Características

- ✅ **Autenticação Real**: Sistema de login e cadastro com banco de dados
- ✅ **Upload de Imagens**: Suporte para PNG, JPG, JPEG, BMP
- ✅ **Análise de IA**: Detecção automática de doenças pulmonares usando torchxrayvision
- ✅ **Banco de Dados Persistente**: SQLite com SQLAlchemy ORM
- ✅ **Dashboard em Tempo Real**: Estatísticas de exames e pacientes
- ✅ **Fila de Prioridade**: Organização inteligente de casos urgentes
- ✅ **Relatórios e Analytics**: Dados estatísticos completos

## 🚀 Instalação Rápida

### 1. Clonar/Preparar o Projeto

```bash
cd c:\Users\Arthur\Desktop\LifeAI
```

### 2. Criar Ambiente Virtual (Opcional mas recomendado)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

⚠️ **Nota**: A primeira instalação pode levar alguns minutos, especialmente devido ao download do modelo de IA (torchxrayvision).

### 4. Executar a Aplicação

```bash
python app.py
```

A aplicação estará disponível em: **http://localhost:5000**

## 🔐 Credenciais de Demonstração

Após executar `python app.py`, um usuário de demonstração é criado automaticamente:

- **Email**: `demo@lifeai.com`
- **Senha**: `demo123`

## 📁 Estrutura do Projeto

```
LifeAI/
├── app.py                 # Aplicação Flask principal (funcional 100%)
├── database.py            # Modelos de banco de dados (SQLAlchemy)
├── ai_analyzer.py         # Analisador de IA (torchxrayvision)
├── requirements.txt       # Dependências Python
├── lifeai.db             # Banco de dados SQLite (criado automaticamente)
├── uploads/              # Pasta de uploads de imagens (criada automaticamente)
├── templates/            # Templates HTML
│   ├── base.html
│   ├── login.html
│   ├── cadastro.html
│   ├── painel_controle.html
│   ├── novo_exame.html
│   ├── exames.html
│   ├── detalhes_exame.html
│   ├── fila_prioridade.html
│   ├── relatorios.html
│   ├── configuracoes.html
│   ├── perfil.html
│   ├── 404.html
│   ├── 500.html
│   └── partials/         # Componentes reutilizáveis
└── static/               # CSS, JS e imagens
    ├── css/
    ├── js/
    └── img/
```

## 🧠 Como Funciona a IA

### Modelo Utilizado
- **Framework**: TorchXRayVision (wrapper de PyTorch)
- **Modelo Base**: DenseNet121 (pré-treinado no dataset NIH)
- **Doenças Detectadas**:
  - Pneumonia ✓
  - Consolidação Pulmonar
  - Infiltração
  - Derrame Pleural
  - Atelectasia
  - Fibrose Pulmonar
  - Espessamento Pleural

### Pipeline de Análise

```
1. Upload da Imagem
   ↓
2. Validação do Arquivo
   ↓
3. Pré-processamento (Normalização, Redimensionamento)
   ↓
4. Passagem pelo Modelo de IA
   ↓
5. Cálculo de Probabilidades
   ↓
6. Classificação de Gravidade
   ↓
7. Definição de Prioridade
   ↓
8. Geração de Recomendações Médicas
   ↓
9. Armazenamento no Banco de Dados
```

## 🔧 Funcionalidades Implementadas

### ✅ Autenticação
- [x] Login com validação de credenciais
- [x] Cadastro de novos usuários
- [x] Hash de senhas (werkzeug.security)
- [x] Sessão persistente

### ✅ Gerenciamento de Exames
- [x] Upload de radiografias
- [x] Armazenamento de metadados do paciente
- [x] Análise automática com IA
- [x] Armazenamento de resultados
- [x] Visualização de detalhes

### ✅ Dashboard
- [x] Total de exames
- [x] Contagem por prioridade (Crítico, Urgente, Atenção, Normal)
- [x] Estatísticas em tempo real
- [x] Dados persistentes do banco

### ✅ Fila de Prioridade
- [x] Organização automática por gravidade
- [x] Priorização de casos críticos
- [x] Atualização em tempo real

### ✅ Relatórios
- [x] Total de exames e pacientes
- [x] Casos graves
- [x] Taxa de eficiência da IA
- [x] Tempo médio de processamento
- [x] Histórico de análises

## 📊 Exemplo de Fluxo Completo

### 1. Usuário se Cadastra
```
Acessa: /cadastro
Preenche: Nome, Email, CPF, CRM, Hospital, Senha
Sistema: Cria conta no banco de dados
```

### 2. Faz Login
```
Acessa: /login
Inserir: Email e senha
Sistema: Valida credenciais e cria sessão
```

### 3. Envia Exame
```
Acessa: /novo-exame
Upload: Seleciona radiografia em PNG/JPG
Preenchimento: Dados do paciente e sintomas
Sistema: 
  - Salva arquivo no servidor
  - Cria registro no banco de dados
  - Processa com IA (torchxrayvision)
  - Retorna resultados em tempo real
```

### 4. Visualiza Resultados
```
Análise Automática:
  - Doença detectada: Pneumonia
  - Probabilidade: 78%
  - Gravidade: Grave
  - Prioridade: URGENTE
  - Recomendação: Encaminhamento imediato
```

### 5. Acompanha no Dashboard
```
Dashboard mostra:
  - 1 novo exame analisado
  - Prioridade: URGENTE
  - Tempo de processamento: 2.3s
```

## 🐛 Troubleshooting

### Erro: "Modelo não carregado"
**Solução**: Na primeira execução, o modelo demora minutos para baixar. Aguarde.

### Erro: "Arquivo não permitido"
**Solução**: Use apenas PNG, JPG, JPEG ou BMP. Máximo 50MB.

### Erro: "Porta 5000 em uso"
**Solução**: Mude a porta em app.py: `app.run(port=5001)`

### Erro: "ModuleNotFoundError"
**Solução**: Instale as dependências: `pip install -r requirements.txt`

## 📝 Notas Importantes

1. **Primeira Execução**: Pode levar 5-10 minutos para baixar o modelo de IA
2. **Banco de Dados**: Arquivo `lifeai.db` é criado automaticamente
3. **Upload de Arquivos**: Máximo 50MB, salvos em pasta `uploads/`
4. **Produção**: Mude `app.secret_key` e desative `debug=True`
5. **IA**: Requer ~2GB de RAM para carregar o modelo

## 🚀 Próximos Passos (Sugestões)

- [ ] Adicionar autenticação por 2FA
- [ ] Integrar com PACS (Picture Archiving System)
- [ ] Adicionar exportação de relatórios (PDF)
- [ ] Integrar com WhatsApp para alertas
- [ ] Adicionar mais modelos de IA
- [ ] Implementar histórico de análises por paciente
- [ ] Adicionar gráficos mais avançados
- [ ] Integrar com prontuário eletrônico

## 📞 Suporte

Para problemas ou dúvidas, consulte os logs do console ou abra uma issue no projeto.

---

**Status**: ✅ Totalmente Funcional
**Última Atualização**: Maio 2026
