import flet as ft
import os
from pessoas import Pessoa
from manipulador import Manipulador

# Variáveis globais
arquivo_atual = None
usuarios = []
m = Manipulador()

def main(page: ft.Page):
    global nome_input, cpf_input, email_input, profissao_input, codigo_input, output_text, nome_arquivo_input
    
    # Título da página
    page.title = "Gerenciador de Usuários JSON"
    
    # Definir campo para o nome do arquivo JSON
    nome_arquivo_input = ft.TextField(label="Nome do Arquivo JSON", width=300)

    # Componentes da interface para dados do usuário
    nome_input = ft.TextField(label="Nome", width=300)
    cpf_input = ft.TextField(label="CPF", width=300)
    email_input = ft.TextField(label="E-mail", width=300)
    profissao_input = ft.TextField(label="Profissão", width=300)
    codigo_input = ft.TextField(label="Código do Usuário", width=300)
    output_text = ft.Text(value="", color=ft.colors.RED)
    
    # Botões
    abrir_arquivo_button = ft.ElevatedButton("Abrir Arquivo", on_click=abrir_arquivo)
    salvar_usuario_button = ft.ElevatedButton("Salvar Usuário", on_click=salvar_usuario)
    alterar_usuario_button = ft.ElevatedButton("Alterar Usuário", on_click=alterar_usuario)
    deletar_usuario_button = ft.ElevatedButton("Deletar Usuário", on_click=deletar_usuario)
    
    # Adicionar componentes à página
    page.add(
        ft.Column([
            ft.Text("Nome do Arquivo JSON"),
            nome_arquivo_input,  # Corrigido: Campo agora é definido corretamente
            abrir_arquivo_button,
            ft.Text("Dados do Usuário"),
            nome_input,
            cpf_input,
            email_input,
            profissao_input,
            codigo_input,
            salvar_usuario_button,
            alterar_usuario_button,
            deletar_usuario_button,
            output_text
        ])
    )
    
    page.update()

# Função de abrir arquivo
def abrir_arquivo(e):
    global arquivo_atual, usuarios
    arquivo_atual = nome_arquivo_input.value  # Armazena o nome do arquivo aberto
    try:
        usuarios = m.abrir_arquivo(arquivo_atual)
        output_text.value = f"Arquivo {arquivo_atual}.json aberto com sucesso.\n{usuarios}"
    except Exception as ex:
        output_text.value = f"Erro ao abrir o arquivo: {ex}"
    output_text.update()

# Função de salvar usuário
def salvar_usuario(e):
    global arquivo_atual, usuarios
    if arquivo_atual is None:
        output_text.value = "Nenhum arquivo aberto para salvar os dados."
        output_text.update()
        return

    # Verificar se todos os campos estão preenchidos
    if not (nome_input.value and cpf_input.value and email_input.value and profissao_input.value):
        output_text.value = "Preencha todos os campos antes de salvar."
        output_text.update()
        return

    try:
        # Criar um novo usuário e adicionar à lista
        novo_usuario = {
            'codigo': len(usuarios),
            'nome': nome_input.value,
            'cpf': cpf_input.value,
            'email': email_input.value,
            'profissao': profissao_input.value
        }
        usuarios.append(novo_usuario)
        resultado = m.salvar_dados(usuarios, arquivo_atual)  # Salvar os dados no JSON
        output_text.value = resultado
    except Exception as ex:
        output_text.value = f"Erro ao salvar o usuário: {ex}"

    output_text.update()

# Função de alterar usuário
def alterar_usuario(e):
    global arquivo_atual, usuarios
    if arquivo_atual is None:
        output_text.value = "Nenhum arquivo aberto para alterar os dados."
        output_text.update()
        return

    try:
        codigo = int(codigo_input.value)

        if codigo < 0 or codigo >= len(usuarios):
            output_text.value = "Código de usuário inválido."
            output_text.update()
            return

        usuario = usuarios[codigo]
        # Alterar os campos, se houver novo valor
        for campo in ['nome', 'cpf', 'email', 'profissao']:
            novo_valor = eval(f'{campo}_input').value
            if novo_valor:
                usuario[campo] = novo_valor

        resultado = m.salvar_dados(usuarios, arquivo_atual)  # Salvar alterações no JSON
        output_text.value = f"Usuário alterado com sucesso.\n{resultado}"
    except Exception as ex:
        output_text.value = f"Erro ao alterar usuário: {ex}"

    output_text.update()

# Função de deletar usuário
def deletar_usuario(e):
    global arquivo_atual, usuarios
    if arquivo_atual is None:
        output_text.value = "Nenhum arquivo aberto para deletar o usuário."
        output_text.update()
        return

    try:
        codigo = int(codigo_input.value)

        if codigo < 0 or codigo >= len(usuarios):
            output_text.value = "Código de usuário inválido."
            output_text.update()
            return

        del usuarios[codigo]  # Deletar o usuário da lista
        resultado = m.salvar_dados(usuarios, arquivo_atual)  # Salvar alterações no JSON
        output_text.value = f"Usuário deletado com sucesso.\n{resultado}"
    except Exception as ex:
        output_text.value = f"Erro ao deletar usuário: {ex}"

    output_text.update()

# Iniciar a aplicação Flet
ft.app(target=main)