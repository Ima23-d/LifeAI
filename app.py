from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from urllib.parse import quote as url_quote
import os
import json

from database import db, Usuario, Exame, Analise, init_db
from ai_analyzer import analisar_imagem

# ==========================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ==========================================

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_muito_segura_mudar_em_producao_2024'

# Configuração do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "lifeai.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração de upload
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'dcm'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Inicializar banco de dados
db.init_app(app)

# Filtro Jinja2
app.jinja_env.filters['urlencode'] = lambda v: url_quote(str(v)) if v else ''


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def arquivo_permitido(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def login_requerido(f):
    """Decorator para verificar autenticação"""
    def decorator(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('pagina_login'))
        return f(*args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator


def obter_usuario_atual():
    """Obtém o usuário autenticado"""
    if 'usuario_id' in session:
        return Usuario.query.get(session['usuario_id'])
    return None

# ==========================================
# ROTAS DE AUTENTICAÇÃO
# ==========================================

@app.route('/')
def indice():
    """Página inicial"""
    if 'usuario_id' in session:
        return redirect(url_for('painel_controle'))
    return redirect(url_for('pagina_login'))


@app.route('/login', methods=['GET', 'POST'])
def pagina_login():
    """Página de login"""
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['nome_usuario'] = usuario.nome
            session['crm'] = usuario.crm
            session['hospital'] = usuario.hospital
            session['email'] = usuario.email
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
        
        if Usuario.query.filter_by(email=email).first():
            return render_template('cadastro.html', erro='Email já cadastrado')
        
        if Usuario.query.filter_by(cpf=cpf).first():
            return render_template('cadastro.html', erro='CPF já cadastrado')
        
        # Criar novo usuário
        novo_usuario = Usuario(
            nome=nome_completo,
            email=email,
            cpf=cpf,
            crm=crm,
            hospital=hospital,
            senha=generate_password_hash(senha)
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        session['usuario_id'] = novo_usuario.id
        session['nome_usuario'] = novo_usuario.nome
        session['crm'] = novo_usuario.crm
        session['hospital'] = novo_usuario.hospital
        session['email'] = novo_usuario.email
        
        return redirect(url_for('painel_controle'))
    
    return render_template('cadastro.html')


@app.route('/sair')
def sair():
    """Logout"""
    session.clear()
    return redirect(url_for('pagina_login'))


# ==========================================
# ROTAS PRINCIPAIS
# ==========================================

@app.route('/painel-controle')
@login_requerido
def painel_controle():
    """Dashboard principal com dados reais"""
    usuario = obter_usuario_atual()
    
    # Contar exames por prioridade
    exames_usuario = Exame.query.filter_by(usuario_id=usuario.id).all()
    
    total_exames = len(exames_usuario)
    urgentes = sum(1 for e in exames_usuario if e.prioridade == 'URGENTE')
    criticos = sum(1 for e in exames_usuario if e.prioridade == 'CRÍTICO')
    atencao = sum(1 for e in exames_usuario if e.prioridade == 'ATENÇÃO')
    normais = sum(1 for e in exames_usuario if e.prioridade == 'NORMAL')
    
    # Exames pendentes de análise
    pendentes = sum(1 for e in exames_usuario if e.status == 'PENDENTE')
    
    contexto = {
        'total_exames': total_exames,
        'urgentes': urgentes,
        'criticos': criticos,
        'atenção': atencao,
        'normais': normais,
        'pendentes': pendentes,
        'pacientes_fila': total_exames,
        'usuario': usuario.nome,
        'hospital': usuario.hospital,
        'crm': usuario.crm,
    }
    
    return render_template('painel_controle.html', **contexto)


@app.route('/novo-exame', methods=['GET', 'POST'])
@login_requerido
def novo_exame():
    """Página para upload de novo exame com análise de IA"""
    usuario = obter_usuario_atual()
    
    if request.method == 'POST':
        # Validar campos obrigatórios
        nome_paciente = request.form.get('nome_paciente')
        cpf_paciente = request.form.get('cpf_paciente')
        data_nascimento = request.form.get('data_nascimento')
        sexo = request.form.get('sexo')
        hospital = request.form.get('hospital')
        sintomas = request.form.get('sintomas')
        observacoes = request.form.get('observacoes')
        
        if not all([nome_paciente, cpf_paciente, data_nascimento, sexo, hospital]):
            return render_template('novo_exame.html', 
                                 erro='Preencha todos os campos obrigatórios',
                                 usuario=usuario.nome,
                                 hospital=usuario.hospital)
        
        # Verificar se usa imagem padrão ou arquivo enviado
        usar_padrao = request.form.get('usar_imagem_padrao') == '1'
        arquivo = request.files.get('imagem')
        arquivo_enviado = arquivo and arquivo.filename != ''

        if not arquivo_enviado and not usar_padrao:
            return render_template('novo_exame.html',
                                 erro='Nenhuma imagem foi enviada',
                                 usuario=usuario.nome,
                                 hospital=usuario.hospital)

        if arquivo_enviado:
            if not arquivo_permitido(arquivo.filename):
                return render_template('novo_exame.html',
                                     erro='Tipo de arquivo não permitido. Use: PNG, JPG, JPEG, BMP',
                                     usuario=usuario.nome,
                                     hospital=usuario.hospital)
            # Salvar arquivo enviado
            filename = secure_filename(f"{usuario.id}_{int(datetime.utcnow().timestamp())}_{arquivo.filename}")
            caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            arquivo.save(caminho_arquivo)
            nome_arquivo_original = arquivo.filename
        else:
            # Usar imagem padrão de demonstração
            caminho_arquivo = os.path.join(basedir, 'Imagem', 'imagem.jfif')
            nome_arquivo_original = 'imagem_padrao.jpg'
        
        # Criar registro de exame
        novo_exame_db = Exame(
            usuario_id=usuario.id,
            nome_paciente=nome_paciente,
            cpf_paciente=cpf_paciente,
            data_nascimento=data_nascimento,
            sexo=sexo,
            hospital=hospital,
            sintomas=sintomas,
            observacoes=observacoes,
            caminho_imagem=caminho_arquivo,
            nome_arquivo_original=nome_arquivo_original,
            status='PENDENTE'
        )
        
        db.session.add(novo_exame_db)
        db.session.commit()
        
        # Analisar imagem com IA
        print(f"\n🔍 Iniciando análise de IA para exame #{novo_exame_db.id}...")
        
        resultado_ia = analisar_imagem(caminho_arquivo)
        
        if resultado_ia['sucesso']:
            # Atualizar exame com resultados
            novo_exame_db.doenca_identificada = resultado_ia.get('doenca_principal')
            novo_exame_db.probabilidade = resultado_ia.get('probabilidade')
            novo_exame_db.gravidade = resultado_ia.get('gravidade')
            novo_exame_db.confianca = resultado_ia.get('confianca')
            novo_exame_db.recomendacao = resultado_ia.get('recomendacao')
            novo_exame_db.prioridade = resultado_ia.get('prioridade')
            novo_exame_db.status = 'ANALISADO'
            novo_exame_db.resultado_json = resultado_ia
            
            db.session.commit()
            
            # Salvar análise
            analise = Analise(
                exame_id=novo_exame_db.id,
                usuario_id=usuario.id,
                resultado_completo=resultado_ia,
                tempo_processamento=resultado_ia.get('tempo_processamento')
            )
            
            db.session.add(analise)
            db.session.commit()
            
            print(f"✓ Análise concluída: {resultado_ia.get('doenca_principal')} ({resultado_ia.get('probabilidade')}%)")
            
            # Retornar página com resultados reais
            contexto = {
                'resultado_analise': resultado_ia,
                'dados_paciente': {
                    'id': novo_exame_db.id,
                    'nome_paciente': novo_exame_db.nome_paciente,
                    'cpf': novo_exame_db.cpf_paciente,
                    'data_nascimento': novo_exame_db.data_nascimento,
                    'sexo': novo_exame_db.sexo,
                    'hospital': novo_exame_db.hospital,
                    'sintomas': novo_exame_db.sintomas,
                    'observacoes': novo_exame_db.observacoes,
                    'data_registro': novo_exame_db.data_registro.strftime('%d/%m/%Y %H:%M'),
                },
                'usuario': usuario.nome,
                'sucesso': True
            }
            
            return render_template('novo_exame.html', **contexto)
        else:
            print(f"✗ Erro na análise: {resultado_ia.get('erro')}")
            novo_exame_db.status = 'ERRO'
            db.session.commit()
            
            return render_template('novo_exame.html',
                                 erro=f"Erro na análise: {resultado_ia.get('erro')}",
                                 usuario=usuario.nome,
                                 hospital=usuario.hospital)
    
    contexto = {
        'usuario': usuario.nome,
        'hospital': usuario.hospital,
    }
    
    return render_template('novo_exame.html', **contexto)


@app.route('/exames')
@login_requerido
def lista_exames():
    """Lista de todos os exames do usuário"""
    usuario = obter_usuario_atual()
    
    # Buscar exames ordenados por data (mais recentes primeiro)
    exames = Exame.query.filter_by(usuario_id=usuario.id).order_by(Exame.data_registro.desc()).all()
    
    contexto = {
        'usuario': usuario.nome,
        'hospital': usuario.hospital,
        'exames': exames,
        'total_exames': len(exames),
    }
    
    return render_template('exames.html', **contexto)


@app.route('/exames/<int:id_exame>')
@login_requerido
def detalhes_exame(id_exame):
    """Página de detalhes de um exame específico"""
    usuario = obter_usuario_atual()
    
    exame = Exame.query.get_or_404(id_exame)
    
    # Verificar permissão
    if exame.usuario_id != usuario.id:
        return redirect(url_for('lista_exames'))
    
    # Buscar análise associada
    analise = Analise.query.filter_by(exame_id=id_exame).first()
    
    contexto = {
        'usuario': usuario.nome,
        'hospital': usuario.hospital,
        'exame': exame,
        'analise': analise,
        'is_demo': False,
    }
    
    return render_template('detalhes_exame.html', **contexto)


@app.route('/exames/demo')
@login_requerido
def detalhes_exame_demo():
    """Página de detalhes de exame de demonstração (dados fictícios via query string)"""
    import types
    usuario = obter_usuario_atual()

    id_ex      = request.args.get('id', 'EXM-DEMO')
    paciente   = request.args.get('paciente', 'Paciente Demo')
    doenca     = request.args.get('doenca', 'Pneumonia')
    prioridade = request.args.get('prioridade', 'ALTA')
    prob_str   = request.args.get('prob', '78')
    data       = request.args.get('data', '—')
    sexo_val   = request.args.get('sexo', '—')

    prob_float = float(prob_str) if prob_str.replace('.', '').isdigit() else 78.0

    # SimpleNamespace evita o problema de escopo de classes internas
    exame = types.SimpleNamespace(
        id                  = id_ex,
        nome_paciente       = paciente,
        sexo                = sexo_val,
        cpf_paciente        = '***.***.***-**',
        data_nascimento     = '—',
        hospital            = usuario.hospital,
        sintomas            = None,
        observacoes         = None,
        data_registro       = data,
        caminho_imagem      = None,
        nome_arquivo_original = '—',
        status              = 'ANALISADO',
        doenca_identificada = doenca,
        probabilidade       = prob_float,
        gravidade           = 'Moderada',
        prioridade          = prioridade,
        recomendacao        = 'Correlacionar com apresentação clínica do paciente.',
        resultado_json      = {
            'sucesso': True,
            'doenca_principal': doenca,
            'probabilidade': prob_float,
            'gravidade': 'Moderada',
            'prioridade': prioridade,
            'recomendacao': 'Correlacionar com apresentação clínica do paciente.',
            'resultados_completos': [],
            'tempo_processamento': 0,
        },
    )

    contexto = {
        'usuario': usuario.nome,
        'hospital': usuario.hospital,
        'exame': exame,
        'analise': None,
        'is_demo': True,
    }

    return render_template('detalhes_exame.html', **contexto)


@app.route('/fila-prioridade')
@login_requerido
def fila_prioridade():
    """Página da fila de prioridade"""
    usuario = obter_usuario_atual()
    
    # Buscar exames ordenados por prioridade
    prioridades = {'CRÍTICO': 0, 'URGENTE': 1, 'ATENÇÃO': 2, 'NORMAL': 3}
    exames = Exame.query.filter_by(usuario_id=usuario.id).all()
    exames_ordenados = sorted(
        exames,
        key=lambda x: (prioridades.get(x.prioridade, 4), x.data_registro.timestamp()),
        reverse=True
    )
    
    contexto = {
        'usuario': usuario.nome,
        'hospital': usuario.hospital,
        'exames_fila': exames_ordenados,
        'total_fila': len(exames_ordenados),
    }
    
    return render_template('fila_prioridade.html', **contexto)


@app.route('/relatorios')
@login_requerido
def pagina_relatorios():
    """Página de relatórios com dados reais"""
    usuario = obter_usuario_atual()
    
    exames = Exame.query.filter_by(usuario_id=usuario.id).all()
    
    # Calcular estatísticas
    total_exames = len(exames)
    total_pacientes = len(set(e.cpf_paciente for e in exames))
    casos_graves = sum(1 for e in exames if e.prioridade in ['CRÍTICO', 'URGENTE'])
    exames_analisados = sum(1 for e in exames if e.status == 'ANALISADO')
    
    # Calcular tempo médio de atendimento
    tempos = [a.tempo_processamento for a in Analise.query.filter_by(usuario_id=usuario.id).all() if a.tempo_processamento]
    tempo_medio = sum(tempos) / len(tempos) if tempos else 0
    
    # Taxa de eficiência (exames analisados com sucesso / total)
    eficiencia = (exames_analisados / total_exames * 100) if total_exames > 0 else 0
    
    contexto = {
        'usuario': usuario.nome,
        'hospital': usuario.hospital,
        'total_exames': total_exames,
        'total_pacientes': total_pacientes,
        'casos_graves': casos_graves,
        'exames_analisados': exames_analisados,
        'tempo_medio_atendimento': f"{tempo_medio:.1f}s",
        'eficiencia_ia': f"{eficiencia:.1f}%",
        'exames': exames[:10]  # Últimos 10 exames
    }
    
    return render_template('relatorios.html', **contexto)


@app.route('/configuracoes')
@login_requerido
def pagina_configuracoes():
    """Página de configurações"""
    usuario = obter_usuario_atual()
    
    contexto = {
        'usuario': usuario.nome,
        'hospital': usuario.hospital,
        'crm': usuario.crm,
        'email': usuario.email,
    }
    
    return render_template('configuracoes.html', **contexto)


@app.route('/perfil')
@login_requerido
def pagina_perfil():
    """Página de perfil do usuário"""
    usuario = obter_usuario_atual()
    
    exames_usuario = Exame.query.filter_by(usuario_id=usuario.id).all()
    
    contexto = {
        'usuario': usuario.nome,
        'hospital': usuario.hospital,
        'crm': usuario.crm,
        'email': usuario.email,
        'total_exames_realizados': len(exames_usuario),
        'data_membro': usuario.data_criacao.strftime('%d/%m/%Y'),
    }
    
    return render_template('perfil.html', **contexto)


# ==========================================
# ROTAS API (AJAX)
# ==========================================

@app.route('/api/analisar-exame', methods=['POST'])
def api_analisar_exame():
    """API para análise de exame com IA"""
    if 'usuario_id' not in session:
        return jsonify({'sucesso': False, 'erro': 'Não autenticado'}), 401
    
    dados = request.json
    usuario = obter_usuario_atual()
    
    id_exame = dados.get('id_exame')
    exame = Exame.query.get_or_404(id_exame)
    
    # Verificar permissão
    if exame.usuario_id != usuario.id:
        return jsonify({'sucesso': False, 'erro': 'Sem permissão'}), 403
    
    if exame.status != 'PENDENTE':
        return jsonify({'sucesso': False, 'erro': 'Exame já foi analisado'}), 400
    
    # Analisar imagem
    resultado = analisar_imagem(exame.caminho_imagem)
    
    if resultado['sucesso']:
        exame.doenca_identificada = resultado.get('doenca_principal')
        exame.probabilidade = resultado.get('probabilidade')
        exame.gravidade = resultado.get('gravidade')
        exame.confianca = resultado.get('confianca')
        exame.recomendacao = resultado.get('recomendacao')
        exame.prioridade = resultado.get('prioridade')
        exame.status = 'ANALISADO'
        exame.resultado_json = resultado
        
        db.session.commit()
        
        # Salvar análise
        analise = Analise(
            exame_id=exame.id,
            usuario_id=usuario.id,
            resultado_completo=resultado,
            tempo_processamento=resultado.get('tempo_processamento')
        )
        db.session.add(analise)
        db.session.commit()
        
        return jsonify(resultado)
    else:
        return jsonify({'sucesso': False, 'erro': resultado.get('erro')}), 500


@app.route('/api/dados-dashboard')
def api_dados_dashboard():
    """API para dados do dashboard em tempo real"""
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    
    usuario = obter_usuario_atual()
    exames = Exame.query.filter_by(usuario_id=usuario.id).all()
    
    dados = {
        'total_exames': len(exames),
        'urgentes': sum(1 for e in exames if e.prioridade == 'URGENTE'),
        'criticos': sum(1 for e in exames if e.prioridade == 'CRÍTICO'),
        'atenção': sum(1 for e in exames if e.prioridade == 'ATENÇÃO'),
        'normais': sum(1 for e in exames if e.prioridade == 'NORMAL'),
    }
    
    return jsonify(dados)


# ==========================================
# ROTA PARA SERVIR UPLOADS
# ==========================================

@app.route('/uploads/<filename>')
def servir_upload(filename):
    """Serve arquivos da pasta de uploads ou imagens padrão"""
    try:
        secure_name = secure_filename(filename)
        
        # Se for imagem_padrao.jpg, servir sem autenticação
        if secure_name == 'imagem_padrao.jpg':
            caminho_padrao = os.path.join(basedir, 'Imagem', 'imagem.jfif')
            if os.path.exists(caminho_padrao):
                return send_file(caminho_padrao, mimetype='image/jpeg')
            return '', 404
        
        # Para outros arquivos, exigir autenticação
        if 'usuario_id' not in session:
            return '', 401
        
        # Validar se o arquivo do upload existe
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], secure_name)
        if os.path.exists(caminho_arquivo):
            return send_file(caminho_arquivo, as_attachment=False)
        
        # Arquivo não encontrado
        return '', 404
    except Exception as e:
        print(f"Erro ao servir arquivo: {e}")
        return '', 404


@app.route('/imagem-padrao')
def imagem_padrao():
    """Serve a imagem padrão sem autenticação"""
    try:
        caminho = os.path.join(basedir, 'Imagem', 'imagem.jfif')
        if os.path.exists(caminho):
            return send_file(caminho, mimetype='image/jpeg')
        return '', 404
    except Exception as e:
        print(f"Erro ao servir imagem padrão: {e}")
        return '', 404



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
    with app.app_context():
        init_db(app)
        
        # Criar usuários de demonstração (remover em produção)
        if Usuario.query.first() is None:
            print("\n📝 Criando usuário de demonstração...")
            usuario_demo = Usuario(
                email='demo@lifeai.com',
                nome='Dr. João Silva',
                cpf='123.456.789-10',
                crm='123456/SP',
                hospital='Hospital Clínico Central',
                senha=generate_password_hash('demo123')
            )
            db.session.add(usuario_demo)
            db.session.commit()
            print("✓ Usuário demo criado: demo@lifeai.com / senha: demo123\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
