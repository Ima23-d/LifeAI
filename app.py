from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime
from urllib.parse import quote as url_quote
import json

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui_mudar_em_producao'

# Filtro Jinja2 para codificar valores em URLs
app.jinja_env.filters['urlencode'] = lambda v: url_quote(str(v)) if v else ''


# ==========================================
# DADOS DE EXEMPLO (Substituir por banco de dados real)
# ==========================================

usuarios_autenticados = {}
exames_armazenados = []
fila_prioridade = []

# ==========================================
# ROTAS DE AUTENTICAÇÃO
# ==========================================

@app.route('/')
def indice():
    """Página inicial - redireciona para login se não autenticado"""
    if 'usuario_id' in session:
        return redirect(url_for('painel_controle'))
    return redirect(url_for('pagina_login'))


@app.route('/login', methods=['GET', 'POST'])
def pagina_login():
    """Página de login"""
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Validação simples (substituir por banco de dados real)
        if email and senha:
            session['usuario_id'] = email
            session['nome_usuario'] = 'Dr. João Silva'
            session['crm'] = '123456/SP'
            session['hospital'] = 'Hospital Clínico Central'
            return redirect(url_for('painel_controle'))
        
        return render_template('login.html', erro='Email ou senha inválidos')
    
    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def pagina_cadastro():
    """Página de cadastro"""
    if request.method == 'POST':
        nome_completo = request.form.get('nome_completo')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        crm = request.form.get('crm')
        hospital = request.form.get('hospital')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        # Validação
        if not all([nome_completo, email, cpf, crm, hospital, senha, confirmar_senha]):
            return render_template('cadastro.html', erro='Preencha todos os campos')
        
        if senha != confirmar_senha:
            return render_template('cadastro.html', erro='As senhas não coincidem')
        
        # Registrar usuário (substituir por banco de dados real)
        usuarios_autenticados[email] = {
            'nome': nome_completo,
            'cpf': cpf,
            'crm': crm,
            'hospital': hospital,
            'senha': senha
        }
        
        session['usuario_id'] = email
        session['nome_usuario'] = nome_completo
        session['crm'] = crm
        session['hospital'] = hospital
        
        return redirect(url_for('painel_controle'))
    
    return render_template('cadastro.html')


@app.route('/sair')
def sair():
    """Fazer logout"""
    session.clear()
    return redirect(url_for('pagina_login'))


# ==========================================
# ROTAS PRINCIPAIS
# ==========================================

@app.route('/painel-controle')
def painel_controle():
    """Dashboard principal"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    # Dados de exemplo
    contexto = {
        'total_exames': 8,
        'urgentes': 3,
        'atenção': 6,
        'normais': 45,
        'ia_ativa': 1,
        'pacientes_fila': 75,
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'crm': session.get('crm'),
    }
    
    return render_template('painel_controle.html', **contexto)


@app.route('/novo-exame', methods=['GET', 'POST'])
def novo_exame():
    """Página para upload de novo exame"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    if request.method == 'POST':
        # Processar upload de exame
        nome_paciente = request.form.get('nome_paciente')
        cpf_paciente = request.form.get('cpf_paciente')
        data_nascimento = request.form.get('data_nascimento')
        sexo = request.form.get('sexo')
        hospital = request.form.get('hospital')
        sintomas = request.form.get('sintomas')
        observacoes = request.form.get('observacoes')
        
        # Simular análise de IA (substituir por API real)
        resultado_analise = {
            'gravidade': 'Urgente',
            'percentual_risco': 78,
            'prioridade': 'URGENTE',
            'recomendacao': 'Encaminhamento imediato para pneumologia',
            'tempo_estimado': '15 minutos'
        }
        
        novo_registro = {
            'id': len(exames_armazenados) + 1,
            'nome_paciente': nome_paciente,
            'cpf': cpf_paciente,
            'data_nascimento': data_nascimento,
            'sexo': sexo,
            'hospital': hospital,
            'sintomas': sintomas,
            'observacoes': observacoes,
            'data_registro': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'resultado': resultado_analise
        }
        
        exames_armazenados.append(novo_registro)
        
        return render_template('novo_exame.html', 
                             resultado_analise=resultado_analise,
                             dados_paciente=novo_registro,
                             usuario=session.get('nome_usuario'))
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
    }
    
    return render_template('novo_exame.html', **contexto)


@app.route('/exames')
def lista_exames():
    """Lista de todos os exames realizados"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'exames': exames_armazenados,
        'total_exames': len(exames_armazenados),
    }
    
    return render_template('exames.html', **contexto)


@app.route('/exames/<int:id_exame>')
def detalhes_exame(id_exame):
    """Página de detalhes de um exame específico"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    exame = next((e for e in exames_armazenados if e['id'] == id_exame), None)
    
    if not exame:
        return redirect(url_for('lista_exames'))
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'exame': exame,
    }
    
    return render_template('detalhes_exame.html', **contexto)


@app.route('/exames/demo')
def detalhes_exame_demo():
    """Página de detalhes para exames de demonstração (sem banco de dados)"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))

    # Monta um objeto exame a partir dos query params passados pelos botões de olho
    exame_demo = {
        'id': request.args.get('id', 'EXM-2025-0524-0001'),
        'nome_paciente': request.args.get('paciente', 'Paciente Demonstração'),
        'sexo': request.args.get('sexo', 'Não informado'),
        'cpf': request.args.get('cpf', '***.***.***-**'),
        'data_nascimento': request.args.get('nascimento', '—'),
        'hospital': session.get('hospital', 'Hospital Clínico Central'),
        'sintomas': request.args.get('sintomas', 'Dificuldade respiratória, tosse persistente'),
        'observacoes': request.args.get('obs', 'Exame de demonstração gerado automaticamente pelo sistema LifeAI.'),
        'data_registro': request.args.get('data', '24/05/2025 10:32'),
        'imagem_url': 'img/chest_xray.png',
        'resultado': {
            'gravidade': request.args.get('doenca', 'Pneumonia'),
            'percentual_risco': int(request.args.get('prob', '78').replace('%', '')),
            'prioridade': request.args.get('prioridade', 'ALTA'),
            'recomendacao': 'Encaminhamento imediato para pneumologia. Iniciar antibioticoterapia empírica conforme protocolo institucional.',
            'tempo_estimado': '15 minutos',
        }
    }

    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'exame': exame_demo,
        'is_demo': True,
    }

    return render_template('detalhes_exame.html', **contexto)


@app.route('/fila-prioridade')
def fila_prioridade():
    """Página da fila de prioridade hospitalar"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    # Ordenar exames por prioridade
    prioridades = {'CRÍTICO': 0, 'URGENTE': 1, 'ATENÇÃO': 2, 'NORMAL': 3}
    exames_ordenados = sorted(exames_armazenados, 
                              key=lambda x: prioridades.get(x['resultado'].get('prioridade', 'NORMAL'), 4))
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'exames_fila': exames_ordenados,
        'total_fila': len(exames_ordenados),
    }
    
    return render_template('fila_prioridade.html', **contexto)


@app.route('/relatorios')
def pagina_relatorios():
    """Página de relatórios e analytics"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'total_exames': len(exames_armazenados),
        'total_pacientes': len(exames_armazenados),
        'casos_graves': sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') in ['CRÍTICO', 'URGENTE']),
        'tempo_medio_atendimento': '12 minutos',
        'eficiencia_ia': '94.5%',
    }
    
    return render_template('relatorios.html', **contexto)


@app.route('/configuracoes')
def pagina_configuracoes():
    """Página de configurações"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'crm': session.get('crm'),
    }
    
    return render_template('configuracoes.html', **contexto)


@app.route('/perfil')
def pagina_perfil():
    """Página de perfil do usuário"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'crm': session.get('crm'),
        'email': session.get('usuario_id'),
        'total_exames_realizados': len(exames_armazenados),
    }
    
    return render_template('perfil.html', **contexto)


# ==========================================
# ROTAS API (AJAX)
# ==========================================

@app.route('/api/analisar-exame', methods=['POST'])
def api_analisar_exame():
    """API para análise de exame com IA"""
    dados = request.json
    
    # Simular análise de IA
    resultado = {
        'sucesso': True,
        'gravidade': 'Urgente',
        'percentual_risco': 78,
        'prioridade': 'URGENTE',
        'recomendacao': 'Encaminhamento imediato para pneumologia',
        'tempo_estimado': '15 minutos'
    }
    
    return jsonify(resultado)


@app.route('/api/dados-dashboard')
def api_dados_dashboard():
    """API para dados do dashboard em tempo real"""
    dados = {
        'total_exames': len(exames_armazenados),
        'urgentes': sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') == 'URGENTE'),
        'atenção': sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') == 'ATENÇÃO'),
        'normais': sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') == 'NORMAL'),
        'criticos': sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') == 'CRÍTICO'),
    }
    return jsonify(dados)


# ==========================================
# TRATAMENTO DE ERROS
# ==========================================

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    """Página 404"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def erro_interno(erro):
    """Página 500"""
    return render_template('500.html'), 500


# ==========================================
# INICIAR APLICAÇÃO
# ==========================================

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
