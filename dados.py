# ==================================================
# 🔹 dados.py — SEM CORES · CORRIGIDO
# ==================================================

# 🏭 MÁQUINAS CADASTRADAS
MAQUINAS = [
    "HV-10105", "HV-10110", "HV-10111", "HV-10114", "HV-10116",
    "HV-10117", "HV-10119", "HV-10120", "HV-10121", "HV-10122",
    "HV-10123", "HV-10080", "HV-10089", "HV-19029", "HV-10164",
    "HV-10134"
]

# 🏷️ CABEÇOTES CADASTRADOS
CABECOTES = [
    "CB-12153", "CB-12158", "CB-10159", "CB-12163", "CB-12165",
    "CB-12166", "CB-12168", "CB-12169", "CB-12170", "CB-12171",
    "CB-12172", "CB-12144", "CB-12149", "CB-12214", "CB-12106",
    "CB-12173"
]

# 🔧 ITENS DE INSPEÇÃO — MÁQUINA BASE
SISTEMAS_MAQUINA_BASE = {
    "MÁQUINA BASE": [
        "MOTOR", "RADIADOR DE ÁGUA", "RADIADOR DE ÓLEO", "CONDENSADOR",
        "PROTEÇÃO ANTICHAMAS MANG DIESEL", "BATERIAS", "MANGUEIRAS TANQUE DIESEL",
        "MANGUEIRAS LINHA SUCÇÃO AR", "ABRAÇADEIRA MANG FIL AR", "PROTEÇÃO MANG SUCÇÃO AR",
        "MANTA DO SILENCIOSO", "PROTEÇÃO DA TURBINA", "TURBINA", "VAZAMENTO MOTOR",
        "VAZAMENTO BOMBA DE ÁGUA", "BICO INJETOR", "CHICOTE ELÉTRICO", "ALTERNADOR",
        "MOTOR DE PARTIDA", "COXINS E PARAFUSOS", "TAMPA DO TANQUE"
    ],
    "GIRO": ["VAZAMENTO REDUTOR", "MANGUEIRAS", "SWIVEL"],
    "COMANDO HIDRÁULICO": [
        "PROTEÇÃO DO BRAÇO", "VAZAMENTO", "MANGUEIRAS",
        "CHICOTE ELÉTRICO", "CONECTORES", "VÁLVULAS/SOLENÓIDES"
    ],
    "SISTEMA DE LUBRIFICAÇÃO": ["CONEXÕES E MANGUEIRAS", "SISTEMA LINCOLN"],
    "TRANSMISSÃO": [
        "BOMBA HIDRÁULICA", "MANGUEIRAS", "MOTOR DE TRAÇÃO",
        "MANGUEIRAS MOTOR DE TRAÇÃO"
    ],
    "MATERIAL RODANTE": [
        "ROLETES SUP", "ROLETES INF", "PROTEÇÃO DOS ROLETES", "LINK/ SAPATA"
    ],
    "PROTEÇÕES": [
        "GRADES DA MÁQUINA", "FARÓIS", "ESCADA", "CABINE", "MOTOR",
        "CORRIMÃO", "GRUA", "EXTINTOR", "TAMPÃO INFERIOR DO H"
    ],
    "GRUA/BRAÇO/LANÇA": [
        "CILINDRO", "FOLGAS", "MANGUEIRAS", "TUBULAÇÃO",
        "DISTRIBUIÇÃO DE GRAXA", "PONTEIRA"
    ],
    "CABINE": [
        "CHAVE GERAL", "CHAVE DE PARTIDA", "FARÓIS DA CABINE",
        "LIMPADOR DO LEXAN", "CABOS/CONECTORES"
    ]
}

# 🔧 ITENS DE INSPEÇÃO — CABEÇOTE
SISTEMAS_CABECOTE = {
    "CABEÇOTE": ["ROTATOR", "MOTOR DO ROTATOR", "BIELA", "MANGUEIRAS"],
    "UNIDADE DE CORTE": [
        "SENSORES", "PROTEÇÃO DO SENSOR", "PLACA DO SABRE", "CILINDRO DO SABRE",
        "MOTOR DE SERRA", "TUBOS", "MANGUEIRAS", "CAIXA DE SERRA"
    ],
    "CHASSIS": [
        "CHASSIS", "CILINDRO DO TILT", "BATENTE DO TILT", "LINK",
        "MANGUEIRA LANÇA LINK", "SWIVEL MANG LANÇA LINK", "SUPORTE DO LINK", "CAPÔ"
    ],
    "ROLOS": [
        "MOTORES", "SUPORTE DO ROLO", "TAMPA PROTEÇÃO DO MOTOR", "MANGUEIRAS DO ROLO",
        "BRAÇADEIRA MANG ROLO", "SWIVEL MANG DO ROLO", "CAPA DOS ROLOS", "CAMES",
        "ROLAMENTO", "ARTICULADORES", "CILINDRO", "ROLO DO DORSO"
    ],
    "FACAS": [
        "CILINDROS", "FACA SUP ESQ", "FACA SUP DIR", "FACA INF ESQ",
        "FACA INF DIR", "FACA FIXAS", "MANGUEIRAS"
    ],
    "COMANDO": [
        "SUPORTE", "CHICOTE", "CONECTORES", "VÁLVULAS/SOLENÓIDES",
        "VAZAMENTO", "MANG LINK AO COMANDO", "MÓDULO ELETRÔNICO (MHC)"
    ]
}

# 🔐 NÍVEIS DE ACESSO
NIVEIS = {
    1: "Operador",
    2: "Mecânico",
    3: "Almoxarifado",
    4: "Inspetor",
    5: "Supervisor de Manutenção",
    6: "Supervisor de Operação",
    7: "Coordenador",
    8: "Gerente",
    9: "ADMINISTRADOR"
}

# 📊 STATUS DAS ORDENS
STATUS = {
    1: "AGUARDANDO SERVIÇO",
    2: "EM MANUTENÇÃO",
    3: "AGUARDANDO PEÇA",
    4: "PEÇA PARA RETIRADA",
    5: "AGUARDANDO FINALIZAÇÃO",
    6: "ORDEM CONCLUÍDA",
    7: "MÁQUINA PARADA",
    8: "MÁQUINA LIBERADA"
}

# 🖼️ CABEÇALHO
def exibir_cabecalho_sistema():
    print("\n" + "="*60)
    print("   BACKLOGDAY — SISTEMA DE GESTÃO DE MANUTENÇÃO")
    print("   Máquinas Florestais · Cabeçotes · Unidades de Corte")
    print("="*60)

# 📋 FUNÇÕES AUXILIARES
def escolher_maquina():
    print("\n  MAQUINAS CADASTRADAS:")
    for i, maq in enumerate(MAQUINAS, 1):
        print(f"   {i:2d} → {maq}")
    print("-"*35)
    while True:
        try:
            op = int(input("  Escolha o NUMERO da maquina: "))
            if 1 <= op <= len(MAQUINAS):
                return MAQUINAS[op - 1]
            print(f"  Digite entre 1 e {len(MAQUINAS)}!")
        except ValueError:
            print("  Apenas numeros!")

def escolher_cabecote():
    print("\n  CABECOTES CADASTRADOS:")
    print("    0 → Nenhum (Maquina Base)")
    for i, cab in enumerate(CABECOTES, 1):
        print(f"   {i:2d} → {cab}")
    print("-"*35)
    while True:
        try:
            op = int(input("  Escolha o NUMERO do cabecote: "))
            if op == 0:
                return "Nenhum"
            if 1 <= op <= len(CABECOTES):
                return CABECOTES[op - 1]
            print(f"  Digite entre 0 e {len(CABECOTES)}!")
        except ValueError:
            print("  Apenas numeros!")

def escolher_sistema_e_item(tem_cabecote):
    sistemas = SISTEMAS_CABECOTE if tem_cabecote else SISTEMAS_MAQUINA_BASE
    titulo = "  SISTEMAS DO CABECOTE" if tem_cabecote else "  SISTEMAS DA MAQUINA BASE"
    lista = list(sistemas.keys())
    print(f"\n{titulo}:")
    for i, s in enumerate(lista, 1):
        print(f"   {i:2d} → {s}")
    print("-"*35)
    while True:
        try:
            op_s = int(input("  Escolha o NUMERO do SISTEMA: "))
            if 1 <= op_s <= len(lista):
                sistema = lista[op_s - 1]
                break
            print(f"  Digite entre 1 e {len(lista)}!")
        except ValueError:
            print("  Apenas numeros!")
    itens = sistemas[sistema]
    print(f"\n  ITENS — {sistema}:")
    for i, item in enumerate(itens, 1):
        print(f"   {i:2d} → {item}")
    print("-"*35)
    while True:
        try:
            op_i = int(input("  Escolha o NUMERO do ITEM: "))
            if 1 <= op_i <= len(itens):
                return sistema, itens[op_i - 1]
            print(f"  Digite entre 1 e {len(itens)}!")
        except ValueError:
            print("  Apenas numeros!")
