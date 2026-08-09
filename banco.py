# ==================================================
# 🔹 banco.py — SEM CORES
# ==================================================

import json
import os

ARQUIVO_USUARIOS = "backlogday_usuarios.json"
ARQUIVO_DADOS = "backlogday_ordens.json"
PASTA_ANEXOS = "anexos_ordens"
PASTA_RELATORIOS = "relatorios_pdf"

def criar_pastas():
    if not os.path.exists(PASTA_ANEXOS):
        os.makedirs(PASTA_ANEXOS)
        print(f"  Pasta '{PASTA_ANEXOS}' criada!")
    if not os.path.exists(PASTA_RELATORIOS):
        os.makedirs(PASTA_RELATORIOS)
        print(f"  Pasta '{PASTA_RELATORIOS}' criada!")
    return True

def carregar_arquivo(caminho_arquivo, valor_padrao=None):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  Arquivo '{caminho_arquivo}' nao encontrado. Criando...")
        return valor_padrao if valor_padrao is not None else []
    except Exception as e:
        print(f"  Erro ao ler: {e}")
        return valor_padrao if valor_padrao is not None else []

def salvar_arquivo(caminho_arquivo, dados):
    try:
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4, default=str)
        return True
    except Exception as e:
        print(f"  Erro ao salvar: {e}")
        return False

def carregar_usuarios():
    usuarios = carregar_arquivo(ARQUIVO_USUARIOS, [])
    if not usuarios:
        print("  Criando conta ADMINISTRADOR padrao...")
        usuarios = [{"id": 1, "nome": "adm", "senha": "adm123", "nivel": 9}]
        salvar_arquivo(ARQUIVO_USUARIOS, usuarios)
        print("  Usuario: adm  |  Senha: adm123")
    return usuarios

def salvar_usuarios(usuarios):
    return salvar_arquivo(ARQUIVO_USUARIOS, usuarios)

def carregar_ordens():
    return carregar_arquivo(ARQUIVO_DADOS, [])

def salvar_ordens(ordens):
    return salvar_arquivo(ARQUIVO_DADOS, ordens)
