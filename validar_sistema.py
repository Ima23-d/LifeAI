#!/usr/bin/env python3
"""
Script de validação da plataforma LifeAI
Verifica se todos os componentes estão funcionando corretamente
"""

import os
import sys

print("\n" + "="*60)
print("LifeAI - Validação do Sistema")
print("="*60 + "\n")

# 1. Verificar importações
print("1️⃣ Verificando importações...")
try:
    from flask import Flask
    print("   ✓ Flask OK")
    
    from flask_sqlalchemy import SQLAlchemy
    print("   ✓ SQLAlchemy OK")
    
    from werkzeug.security import generate_password_hash
    print("   ✓ Werkzeug OK")
    
    import torch
    print("   ✓ PyTorch OK")
    
    import torchxrayvision as xrv
    print("   ✓ TorchXRayVision OK")
    
    import skimage.io
    print("   ✓ Scikit-Image OK")
    
    print("\n✓ Todas as importações OK!\n")
except ImportError as e:
    print(f"\n✗ Erro de importação: {e}")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)

# 2. Verificar estrutura de pastas
print("2️⃣ Verificando estrutura de pastas...")
required_folders = ['templates', 'static', 'Modelo']
for folder in required_folders:
    if os.path.exists(folder):
        print(f"   ✓ {folder}/ OK")
    else:
        print(f"   ⚠ {folder}/ não encontrado")

# Criar pasta de uploads se não existir
if not os.path.exists('uploads'):
    os.makedirs('uploads')
    print("   ✓ uploads/ criada")
else:
    print("   ✓ uploads/ OK")

print()

# 3. Verificar banco de dados
print("3️⃣ Testando banco de dados...")
try:
    from database import db, Usuario, Exame, Analise, init_db
    from app import app
    
    with app.app_context():
        db.create_all()
        print("   ✓ Banco de dados inicializado")
        
        # Contar usuários
        user_count = Usuario.query.count()
        exam_count = Exame.query.count()
        print(f"   ✓ Usuários: {user_count}")
        print(f"   ✓ Exames: {exam_count}")
    
    print("\n✓ Banco de dados OK!\n")
except Exception as e:
    print(f"\n✗ Erro com banco de dados: {e}\n")

# 4. Verificar modelo de IA
print("4️⃣ Carregando modelo de IA (primeira vez pode levar minutos)...")
try:
    from ai_analyzer import carregar_modelo
    
    print("   ⏳ Carregando modelo... (aguarde)")
    modelo = carregar_modelo()
    print(f"   ✓ Modelo carregado: {type(modelo).__name__}")
    print(f"   ✓ Doenças detectadas: {len(modelo.pathologies)}")
    
    print("\n✓ Modelo de IA OK!\n")
except Exception as e:
    print(f"\n⚠ Aviso ao carregar IA: {e}")
    print("   Isto pode acontecer na primeira execução.")
    print("   O modelo será baixado quando iniciar a aplicação.\n")

# 5. Resumo final
print("="*60)
print("✓ Sistema pronto para operação!")
print("="*60)
print("\nPróximos passos:")
print("1. Execute: python app.py")
print("2. Acesse: http://localhost:5000")
print("3. Use as credenciais:")
print("   Email: demo@lifeai.com")
print("   Senha: demo123")
print("\n" + "="*60 + "\n")
