import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Criar instância do SQLAlchemy
db = SQLAlchemy()

class Usuario(db.Model):
    """Modelo de usuário"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    crm = db.Column(db.String(20), nullable=False)
    hospital = db.Column(db.String(120), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento
    exames = db.relationship('Exame', backref='usuario', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Usuario {self.email}>'


class Exame(db.Model):
    """Modelo de exame"""
    __tablename__ = 'exames'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Informações do paciente
    nome_paciente = db.Column(db.String(120), nullable=False)
    cpf_paciente = db.Column(db.String(14), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    
    # Informações do exame
    hospital = db.Column(db.String(120), nullable=False)
    sintomas = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    
    # Arquivo de imagem
    caminho_imagem = db.Column(db.String(255), nullable=False)
    nome_arquivo_original = db.Column(db.String(120), nullable=False)
    
    # Resultados da IA
    doenca_identificada = db.Column(db.String(120), nullable=True)
    probabilidade = db.Column(db.Float, nullable=True)
    gravidade = db.Column(db.String(20), nullable=True)
    confianca = db.Column(db.Float, nullable=True)
    recomendacao = db.Column(db.Text, nullable=True)
    resultado_json = db.Column(db.JSON, nullable=True)  # Armazena todos os resultados
    
    # Metadados
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    prioridade = db.Column(db.String(20), default='NORMAL')
    status = db.Column(db.String(20), default='PENDENTE')  # PENDENTE, ANALISADO, CONCLUÍDO
    
    def __repr__(self):
        return f'<Exame {self.id} - {self.nome_paciente}>'


class Analise(db.Model):
    """Modelo para armazenar histórico de análises"""
    __tablename__ = 'analises'
    
    id = db.Column(db.Integer, primary_key=True)
    exame_id = db.Column(db.Integer, db.ForeignKey('exames.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Detalhes da análise
    resultado_completo = db.Column(db.JSON, nullable=False)
    tempo_processamento = db.Column(db.Float, nullable=True)
    modelo_versao = db.Column(db.String(50), nullable=True)
    
    data_analise = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Analise {self.id}>'


def init_db(app):
    """Inicializa o banco de dados"""
    with app.app_context():
        db.create_all()
        print("✓ Banco de dados inicializado com sucesso!")
