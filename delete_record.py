#!/usr/bin/env python
"""Script para deletar registros do banco de dados"""

from database import db, Usuario, Exame, init_db
from app import app

def deletar_usuario_por_nome(nome):
    """Deleta usuário por nome"""
    with app.app_context():
        usuario = Usuario.query.filter_by(nome=nome).first()
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            print(f"✓ Usuário '{nome}' deletado com sucesso!")
        else:
            print(f"✗ Usuário '{nome}' não encontrado!")

def deletar_paciente_por_nome(nome):
    """Deleta paciente (exame) por nome do paciente"""
    with app.app_context():
        exames = Exame.query.filter_by(nome_paciente=nome).all()
        if exames:
            for exame in exames:
                print(f"Deletando exame #{exame.id} do paciente {nome}...")
                db.session.delete(exame)
            db.session.commit()
            print(f"✓ {len(exames)} exame(s) de '{nome}' deletado(s) com sucesso!")
        else:
            print(f"✗ Nenhum exame encontrado para o paciente '{nome}'!")

def deletar_exame_por_id(exame_id):
    """Deleta exame por ID"""
    with app.app_context():
        exame = Exame.query.get(exame_id)
        if exame:
            print(f"Deletando exame #{exame_id} ({exame.nome_paciente})...")
            db.session.delete(exame)
            db.session.commit()
            print(f"✓ Exame #{exame_id} deletado com sucesso!")
        else:
            print(f"✗ Exame #{exame_id} não encontrado!")

def listar_todos_exames():
    """Lista todos os exames"""
    with app.app_context():
        exames = Exame.query.all()
        if exames:
            print("\n📋 EXAMES NO BANCO DE DADOS:")
            print("-" * 80)
            for exame in exames:
                print(f"ID: {exame.id} | Paciente: {exame.nome_paciente} | Status: {exame.status}")
            print("-" * 80)
        else:
            print("✗ Nenhum exame encontrado!")

if __name__ == '__main__':
    import sys
    
    print("\n🗑️  DELETAR REGISTROS DO BANCO DE DADOS\n")
    
    # Opções
    if len(sys.argv) > 1:
        opcao = sys.argv[1]
        
        if opcao == 'listar':
            listar_todos_exames()
        elif opcao == 'deletar-paciente' and len(sys.argv) > 2:
            nome = sys.argv[2]
            deletar_paciente_por_nome(nome)
        elif opcao == 'deletar-id' and len(sys.argv) > 2:
            exame_id = int(sys.argv[2])
            deletar_exame_por_id(exame_id)
        else:
            print("Uso:")
            print("  python delete_record.py listar                    - Listar todos exames")
            print("  python delete_record.py deletar-paciente <nome>   - Deletar exame por nome")
            print("  python delete_record.py deletar-id <id>           - Deletar exame por ID")
    else:
        print("Uso:")
        print("  python delete_record.py listar                    - Listar todos exames")
        print("  python delete_record.py deletar-paciente <nome>   - Deletar exame por nome")
        print("  python delete_record.py deletar-id <id>           - Deletar exame por ID")
        print("\nExemplo:")
        print("  python delete_record.py deletar-paciente aaaa")
        print("  python delete_record.py deletar-id 1\n")
