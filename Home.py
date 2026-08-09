import streamlit as st
import json
import os
from datetime import datetime
from banco import carregar_usuarios, salvar_usuarios, carregar_ordens, salvar_ordens
from dados import MAQUINAS, CABECOTES, SISTEMAS_MAQUINA_BASE, SISTEMAS_CABECOTE, NIVEIS, STATUS

st.set_page_config(page_title="BACKLOGDAY - Gestão de Manutenção", layout="wide")

# ==================================================
# 📂 ARQUIVO LOCAL PARA ORDENS OFFLINE (FILA)
# ==================================================
ARQUIVO_FILA_OFFLINE = "fila_offline.json"

def carregar_fila_offline():
    """Carrega ordens que ficaram pendentes sem internet"""
    if os.path.exists(ARQUIVO_FILA_OFFLINE):
        with open(ARQUIVO_FILA_OFFLINE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_fila_offline(fila):
    """Salva ordem na fila local"""
    with open(ARQUIVO_FILA_OFFLINE, "w", encoding="utf-8") as f:
        json.dump(fila, f, ensure_ascii=False, indent=2)

def verificar_conexao():
    """Simula verificação de conexão (no Streamlit Cloud = sempre online)"""
    # Em ambiente online = True; offline = False
    try:
        import urllib.request
        urllib.request.urlopen("https://streamlit.io", timeout=2)
        return True
    except:
        return False

def sincronizar_fila_se_online():
    """Sincroniza automaticamente ordens da fila quando volta internet"""
    if not verificar_conexao():
        return 0, False  # Sem internet → não sincroniza

    fila = carregar_fila_offline()
    if not fila:
        return 0, True  # Nada para sincronizar

    ordens = carregar_ordens()
    sincronizadas = 0

    for ordem_off in fila:
        novo_id = max([x["id"] for x in ordens], default=0) + 1
        ordem_off["id"] = novo_id
        ordem_off["sincronizada_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        ordens.append(ordem_off)
        sincronizadas += 1

    if sincronizadas > 0:
        salvar_ordens(ordens)
        salvar_fila_offline([])  # Limpa fila após sincronizar
        st.toast(f"✅ SINCRONIZADAS {sincronizadas} ORDENS!", icon="🌐")

    return sincronizadas, True

# ==================================================
# 🔄 INICIALIZAR SESSÃO
# ==================================================
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "pagina" not in st.session_state:
    st.session_state.pagina = "login"
if "tela_selecionada" not in st.session_state:
    st.session_state.tela_selecionada = "listar"
if "ultima_sincronia" not in st.session_state:
    st.session_state.ultima_sincronia = None

# Carregar dados
usuarios = carregar_usuarios()
ordens = carregar_ordens()

# 🔄 TENTAR SINCRONIZAR AO ABRIR O SISTEMA
qtd_sinc, online = sincronizar_fila_se_online()
fila_pendente = len(carregar_fila_offline())

# ==================================================
# 🔐 TELA DE LOGIN
# ==================================================
if st.session_state.pagina == "login":
    st.title("🔐 BACKLOGDAY — Sistema de Gestão de Manutenção")
    st.subheader("Máquinas Florestais · Cabeçotes · Unidades de Corte")

    # Status de conexão
    if online:
        st.success("🌐 Sistema ONLINE — sincronização ativa")
    else:
        st.warning("📡 Sistema OFFLINE — ordens serão sincronizadas quando conectar")
        if fila_pendente > 0:
            st.info(f"⏳ {fila_pendente} ordem(ns) aguardando sincronização")

    st.divider()

    nome = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Entrar", type="primary"):
            for u in usuarios:
                if u["nome"] == nome and u["senha"] == senha:
                    st.session_state.usuario = u
                    st.session_state.pagina = "principal"
                    st.session_state.tela_selecionada = "listar"
                    st.success(f"Bem-vindo, {u['nome']}! Perfil: {NIVEIS[u['nivel']]}")
                    st.rerun()
                    break
            else:
                st.error("Usuário ou senha inválidos!")

    st.divider()

# ==================================================
# 🧭 PAINEL PRINCIPAL
# ==================================================
elif st.session_state.pagina == "principal" and st.session_state.usuario:
    u = st.session_state.usuario

    # Cabeçalho com status de sincronização
    col_titulo, col_status = st.columns([3, 1])
    with col_titulo:
        st.title(f"🚜 BACKLOGDAY — Olá, {u['nome']} ({NIVEIS[u['nivel']]})")
    with col_status:
        if online:
            st.success("🌐 CONECTADO")
            if qtd_sinc > 0:
                st.info(f"✅ {qtd_sinc} sincronizada(s)")
        else:
            st.warning("📡 SEM CONEXÃO")
            if fila_pendente > 0:
                st.info(f"⏳ {fila_pendente} na fila")

    st.divider()

    # ==================================================
    # 📋 MENU DE ÍCONES
    # ==================================================
    st.subheader("📋 MENU PRINCIPAL")
    st.divider()

    botoes_menu = [
        ("📋", "Listar Ordens", "listar"),
        ("➕", "Abrir Ordem", "abrir"),
        ("🔧", "Assumir Ordem", "assumir"),
        ("📦", "Solicitar Peças", "pecas"),
        ("✅", "Finalizar Ordem", "finalizar"),
        ("⚙️", "Cadastrar Usuário", "cadastrar"),
        ("📊", "Relatórios", "relatorios"),
    ]
    if u["nivel"] == 9:
        botoes_menu.insert(6, ("🗑️", "Excluir Ordem", "excluir"))
    botoes_menu.append(("🚪", "Sair", "sair"))

    cols = st.columns(3)
    for idx, (icone, label, tag) in enumerate(botoes_menu):
        with cols[idx % 3]:
            eh_ativo = st.session_state.tela_selecionada == tag
            tipo_botao = "primary" if eh_ativo else "secondary"
            if st.button(f"{icone}  {label}", type=tipo_botao, use_container_width=True):
                st.session_state.tela_selecionada = tag
                st.rerun()

    st.divider()

    tela = st.session_state.tela_selecionada

    # 🚪 Sair
    if tela == "sair":
        st.session_state.usuario = None
        st.session_state.pagina = "login"
        st.session_state.tela_selecionada = "listar"
        st.rerun()

    # ==================================================
    # 📋 LISTAR ORDENS
    # ==================================================
    elif tela == "listar":
        st.subheader("📋 Lista de Ordens de Manutenção")

        fila = carregar_fila_offline()
        if fila:
            st.warning(f"⏳ {len(fila)} ORDEM(NS) AGUARDANDO CONEXÃO — será(ão) sincronizada(s) automaticamente")
            for fo in fila:
                st.markdown(f"""
                ⏳ **Ordem temporária — {fo.get('categoria', '')}**
                - Equipamento: {fo.get('equipamento', '')}
                - Sistema/Item: {fo.get('sistema', '')} / {fo.get('item', '')}
                - Solicitante: {fo.get('solicitante_nome', '')} | 📅 {fo.get('data_abertura', '')}
                - **Status: AGUARDANDO CONEXÃO**
                """)
                st.divider()

        if not ordens and not fila:
            st.info("Nenhuma ordem cadastrada.")
        else:
            for o in ordens:
                categoria = o.get("categoria", "Não informada")
                st.markdown(f"""
                **Ordem #{o['id']} — {STATUS[o['status']]}**
                - 🏷️ Categoria: **{categoria}**
                - 📌 Equipamento: {o['equipamento']}
                - 🔧 Sistema/Item: {o.get('sistema', '---')} / {o.get('item', '---')}
                - 👤 Solicitante: {o['solicitante_nome']} | 📅 Abertura: {o['data_abertura']}
                """)
                st.divider()

    # ==================================================
    # ➕ ABRIR ORDEM — COM MODO OFFLINE
    # ==================================================
    elif tela == "abrir":
        if u["nivel"] not in [1, 2, 4, 5, 7, 8, 9]:
            st.error("Sem permissão para abrir ordens!")
        else:
            st.subheader("➕ Abrir Nova Ordem")

            if not online:
                st.warning("📡 MODO OFFLINE — Ordem será salva localmente e sincronizada automaticamente quando conectar à internet")

            st.divider()

            categoria = st.radio("**Selecione a Categoria:**", ["MÁQUINA", "CABEÇOTE"], horizontal=True)
            titulo = st.text_input("Título / Assunto")
            descricao = st.text_area("Descrição do Problema")

            equipamento = None
            sistema = None
            item = None
            st.divider()

            if categoria == "MÁQUINA":
                equipamento = st.selectbox("Selecione a Máquina", MAQUINAS)
                st.divider()
                sistemas_maq = list(SISTEMAS_MAQUINA_BASE.keys())
                sistema = st.selectbox("Sistema da Máquina", sistemas_maq)
                itens_maq = SISTEMAS_MAQUINA_BASE[sistema]
                item = st.selectbox("Item / Componente", itens_maq)

            elif categoria == "CABEÇOTE":
                equipamento = st.selectbox("Selecione o Cabeçote", CABECOTES)
                st.divider()
                sistemas_cb = list(SISTEMAS_CABECOTE.keys())
                sistema = st.selectbox("Sistema do Cabeçote", sistemas_cb)
                itens_cb = SISTEMAS_CABECOTE[sistema]
                item = st.selectbox("Item / Componente", itens_cb)

            st.divider()

            if st.button("✅ Abrir Ordem", type="primary", use_container_width=True):
                dados_ordem = {
                    "categoria": categoria,
                    "titulo": titulo,
                    "descricao": descricao,
                    "equipamento": equipamento,
                    "sistema": sistema,
                    "item": item,
                    "status": 1,
                    "solicitante_id": u["id"],
                    "solicitante_nome": u["nome"],
                    "data_abertura": datetime.now().strftime("%d/%m/%Y %H:%M")
                }

                if online:
                    # ✅ ONLINE — salva direto
                    novo_id = max([x["id"] for x in ordens], default=0) + 1
                    dados_ordem["id"] = novo_id
                    ordens.append(dados_ordem)
                    salvar_ordens(ordens)
                    st.success(f"✅ Ordem #{novo_id} aberta com sucesso!")
                else:
                    # ⏳ OFFLINE — guarda na fila
                    fila = carregar_fila_offline()
                    dados_ordem["id_temporario"] = len(fila) + 1
                    fila.append(dados_ordem)
                    salvar_fila_offline(fila)
                    st.success(f"⏳ Ordem salva LOCALMENTE! Será sincronizada automaticamente quando conectar à internet.")

                st.info(f"Categoria: {categoria} | Equipamento: {equipamento}")
                st.rerun()

    # ==================================================
    # 🔧 ASSUMIR ORDEM
    # ==================================================
    elif tela == "assumir":
        if u["nivel"] != 2:
            st.error("Apenas Mecânicos podem assumir ordens!")
        elif not online:
            st.warning("📡 Sem conexão — não é possível atualizar ordens. Aguarde restabelecer a internet.")
        else:
            st.subheader("🔧 Assumir Ordem")
            ordens_abertas = [o for o in ordens if o["status"] == 1]
            if not ordens_abertas:
                st.info("Nenhuma ordem disponível.")
            else:
                opcoes = [f"#{o['id']} — {o.get('categoria','')} — {o['equipamento']}" for o in ordens_abertas]
                id_escolhida = st.selectbox("Escolha a Ordem", opcoes)
                id_num = int(id_escolhida.split("#")[1].split(" ")[0])
                if st.button("🔧 Assumir Ordem", type="primary"):
                    for o in ordens:
                        if o["id"] == id_num:
                            o["status"] = 2
                            o["responsavel_nome"] = u["nome"]
                            o["data_inicio"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                            salvar_ordens(ordens)
                            st.success(f"✅ Ordem #{id_num} assumida!")
                            st.rerun()

    # ==================================================
    # 📦 SOLICITAR PEÇAS
    # ==================================================
    elif tela == "pecas":
        if u["nivel"] != 2:
            st.error("Apenas Mecânicos podem solicitar peças!")
        elif not online:
            st.warning("📡 Sem conexão — não é possível atualizar ordens. Aguarde restabelecer a internet.")
        else:
            st.subheader("📦 Solicitar Peças")
            ordens_em_andamento = [o for o in ordens if o["status"] == 2 and o.get("responsavel_nome") == u["nome"]]
            if not ordens_em_andamento:
                st.info("Nenhuma ordem em manutenção.")
            else:
                opcoes = [f"#{o['id']} — {o.get('categoria','')} — {o['equipamento']}" for o in ordens_em_andamento]
                id_escolhida = st.selectbox("Escolha a Ordem", opcoes)
                id_num = int(id_escolhida.split("#")[1].split(" ")[0])
                pecas = st.text_area("Peças e Quantidades")
                if st.button("📦 Solicitar Peças", type="primary"):
                    for o in ordens:
                        if o["id"] == id_num:
                            o["solicitacao_pecas"] = pecas
                            o["status"] = 3
                            o["data_solicitacao_pecas"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                            salvar_ordens(ordens)
                            st.success(f"✅ Peças solicitadas na Ordem #{id_num}!")
                            st.rerun()

    # ==================================================
    # ✅ FINALIZAR ORDEM
    # ==================================================
    elif tela == "finalizar":
        if not online:
            st.warning("📡 Sem conexão — não é possível atualizar ordens. Aguarde restabelecer a internet.")
        else:
            st.subheader("✅ Finalizar Ordem")
            pode_todas = u["nivel"] in [8, 9]
            if pode_todas:
                ordens_finalizaveis = [o for o in ordens if o["status"] in [4, 5]]
            else:
                ordens_finalizaveis = [o for o in ordens if o["status"] == 5 and o.get("responsavel_nome") == u["nome"]]
            if not ordens_finalizaveis:
                st.info("Nenhuma ordem para finalizar.")
            else:
                opcoes = [f"#{o['id']} — {o.get('categoria','')} — {o['equipamento']}" for o in ordens_finalizaveis]
                id_escolhida = st.selectbox("Escolha a Ordem", opcoes)
                id_num = int(id_escolhida.split("#")[1].split(" ")[0])
                obs = st.text_area("Observações de Conclusão")
                if st.button("✅ Concluir Ordem", type="primary"):
                    for o in ordens:
                        if o["id"] == id_num:
                            o["status"] = 6
                            o["observacao_conclusao_supervisor"] = obs
                            o["data_conclusao_supervisor"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                            salvar_ordens(ordens)
                            st.success(f"✅ Ordem #{id_num} CONCLUÍDA!")
                            st.rerun()

    # ==================================================
    # 🗑️ EXCLUIR ORDEM
    # ==================================================
    elif tela == "excluir":
        if u["nivel"] != 9:
            st.error("❌ Apenas ADMINISTRADOR pode excluir ordens!")
        elif not online:
            st.warning("📡 Sem conexão — não é possível excluir ordens. Aguarde restabelecer a internet.")
        else:
            st.subheader("🗑️ Excluir Ordem — Rápido")
            st.warning("⚠️ ATENÇÃO: A ordem será APAGADA DEFINITIVAMENTE!")
            st.divider()

            if not ordens:
                st.info("Nenhuma ordem cadastrada.")
            else:
                st.subheader("Lista de Ordens — Clique para Apagar:")
                st.divider()

                for o in ordens:
                    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
                    with col1:
                        st.write(f"**#{o['id']}**")
                    with col2:
                        st.write(f"{o.get('categoria', '---')}")
                    with col3:
                        st.write(f"{o['equipamento']}")
                    with col4:
                        st.write(f"{STATUS[o['status']]}")
                    with col5:
                        if st.button(f"🗑️ Apagar", key=f"del_{o['id']}", type="secondary"):
                            st.session_state[f"confirmar_{o['id']}"] = True
                            st.rerun()

                    if st.session_state.get(f"confirmar_{o['id']}", False):
                        st.warning(f"⚠️ Confirmar exclusão da ORDEM #{o['id']}?")
                        col_sim, col_nao = st.columns(2)
                        with col_sim:
                            if st.button("✅ SIM, APAGAR!", type="primary", key=f"sim_{o['id']}"):
                                ordens[:] = [x for x in ordens if x["id"] != o["id"]]
                                salvar_ordens(ordens)
                                st.success(f"✅ ORDEM #{o['id']} APAGADA COM SUCESSO!")
                                st.session_state[f"confirmar_{o['id']}"] = False
                                st.rerun()
                        with col_nao:
                            if st.button("❌ NÃO, CANCELAR", key=f"nao_{o['id']}"):
                                st.session_state[f"confirmar_{o['id']}"] = False
                                st.rerun()
                    st.divider()

                st.subheader("🔢 Apagar por Número:")
                id_direto = st.number_input("Digite o NÚMERO da Ordem:", min_value=1, step=1)
                if st.button("🗑️ APAGAR AGORA!", type="primary"):
                    encontrou = False
                    for i, o in enumerate(ordens):
                        if o["id"] == id_direto:
                            ordens.pop(i)
                            salvar_ordens(ordens)
                            st.success(f"✅ ORDEM #{id_direto} APAGADA COM SUCESSO!")
                            encontrou = True
                            st.rerun()
                            break
                    if not encontrou:
                        st.error(f"❌ Ordem #{id_direto} NÃO ENCONTRADA!")

    # ==================================================
    # ⚙️ CADASTRAR USUÁRIO
    # ==================================================
    elif tela == "cadastrar":
        if u["nivel"] != 9:
            st.error("Apenas ADMINISTRADOR pode cadastrar usuários!")
        elif not online:
            st.warning("📡 Sem conexão — não é possível cadastrar usuários. Aguarde restabelecer a internet.")
        else:
            st.subheader("⚙️ Cadastrar Novo Usuário")
            nome_novo = st.text_input("Nome do Usuário")
            senha_nova = st.text_input("Senha", type="password")
            nivel_novo = st.selectbox("Nível de Acesso", list(NIVEIS.keys()), format_func=lambda x: f"{x} - {NIVEIS[x]}")
            if st.button("✅ Cadastrar", type="primary"):
                for x in usuarios:
                    if x["nome"] == nome_novo:
                        st.error("Usuário já existe!")
                        break
                else:
                    novo_id = max([x["id"] for x in usuarios], default=0) + 1
                    usuarios.append({"id": novo_id, "nome": nome_novo, "senha": senha_nova, "nivel": nivel_novo})
                    salvar_usuarios(usuarios)
                    st.success(f"✅ Usuário '{nome_novo}' cadastrado como {NIVEIS[nivel_novo]}!")
                    st.rerun()

    # ==================================================
    # 📊 RELATÓRIOS
    # ==================================================
    elif tela == "relatorios":
        st.subheader("📊 Relatório Geral")
        st.write(f"**Total de Ordens:** {len(ordens)}")

        fila = carregar_fila_offline()
        if fila:
            st.write(f"⏳ **Aguardando Conexão:** {len(fila)} ordem(ns)")

        st.divider()
        st.subheader("Por Categoria")
        qtd_maquina = sum(1 for o in ordens if o.get("categoria") == "MÁQUINA")
        qtd_cabecote = sum(1 for o in ordens if o.get("categoria") == "CABEÇOTE")
        st.write(f"🚜 **Máquina:** {qtd_maquina} ordens")
        st.write(f"✂️ **Cabeçote:** {qtd_cabecote} ordens")

        st.divider()
        st.subheader("Por Status")
        for s in STATUS:
            qtd = sum(1 for o in ordens if o["status"] == s)
            if qtd > 0:
                st.write(f"{STATUS[s]}: **{qtd}**")

else:
    st.session_state.pagina = "login"
    st.rerun()
