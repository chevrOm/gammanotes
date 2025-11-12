import tkinter as tk
from tkinter import ttk, messagebox
import csv

# Nome do arquivo CSV
arquivo_csv = 'gammanotes.csv'

# Função para carregar dados do CSV
def carregar_dados():
    try:
        with open(arquivo_csv, 'r', newline='', encoding='utf-8') as f:
            reader = list(csv.reader(f))
            cabecalho = reader[0]
            linhas = reader[1:]
        return cabecalho, linhas
    except FileNotFoundError:
        return [], []

# Função para salvar dados no CSV
def salvar_dados():
    with open(arquivo_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(cabecalho)
        writer.writerows(linhas)
    messagebox.showinfo("Salvo", "Arquivo salvo com sucesso!")

# Atualiza a tabela com os dados
def atualizar_tabela():
    for item in tree.get_children():
        tree.delete(item)
    for idx, linha in enumerate(linhas):
        tree.insert('', 'end', iid=idx, values=linha)

# Preenche os campos de entrada com os dados do registro selecionado
def preencher_campos(event):
    selecionado = tree.selection()
    if selecionado:
        idx = int(selecionado[0])
        registro = linhas[idx]
        for i, col in enumerate(cabecalho):
            entry_widgets[col].delete(0, tk.END)
            entry_widgets[col].insert(0, registro[i].replace('.CME@RITHMIC', '').replace('#', ''))

# Adiciona um novo registro baseado no primeiro registro como padrão
def adicionar_registro():
    if linhas:
        padrao = linhas[0][:]
        novo_registro = padrao[:]
        for i, col in enumerate(cabecalho):
            valor = entry_widgets[col].get()
            if col.lower() == 'symbol':
                if not valor.endswith('.CME@RITHMIC'):
                    valor += '.CME@RITHMIC'
            elif 'color' in col.lower():
                valor = '#' + valor if not valor.startswith('#') else valor
            novo_registro[i] = valor or padrao[i]
        linhas.append(novo_registro)
        atualizar_tabela()
    else:
        messagebox.showwarning("Aviso", "Não há registros existentes para usar como padrão.")

# Apaga o registro selecionado
def apagar_registro():
    selecionado = tree.selection()
    if selecionado:
        idx = int(selecionado[0])
        linhas.pop(idx)
        atualizar_tabela()
        limpar_campos()
    else:
        messagebox.showwarning("Aviso", "Selecione um registro para apagar.")

# Edita o registro selecionado
def editar_registro():
    selecionado = tree.selection()
    if selecionado:
        idx = int(selecionado[0])
        registro_padrao = linhas[0][:]
        for i, col in enumerate(cabecalho):
            valor = entry_widgets[col].get()
            if col.lower() == 'symbol':
                if not valor.endswith('.CME@RITHMIC'):
                    valor += '.CME@RITHMIC'
            elif 'color' in col.lower():
                valor = '#' + valor if not valor.startswith('#') else valor
            registro_padrao[i] = valor or registro_padrao[i]
        linhas[idx] = registro_padrao
        atualizar_tabela()
    else:
        messagebox.showwarning("Aviso", "Selecione um registro para editar.")

# Limpa os campos de entrada
def limpar_campos():
    for col in cabecalho:
        entry_widgets[col].delete(0, tk.END)

# Carrega os dados iniciais
cabecalho, linhas = carregar_dados()

# Cria a janela principal
root = tk.Tk()

# expande janela auto ----------------------------------
root.geometry("1000x600")  # define tamanho inicial da janela
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
# expande janela auto ----------------------------------

root.title("Editor de gammanotes.csv")

# Tabela de registros
tree = ttk.Treeview(root, columns=cabecalho, show='headings')

for col in cabecalho:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(padx=10, pady=10, fill='x')
tree.bind('<<TreeviewSelect>>', preencher_campos)
atualizar_tabela()

# Frame dos campos de entrada
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

entry_widgets = {}
for i, col in enumerate(cabecalho):
    tk.Label(frame_inputs, text=f"{col}:").grid(row=i, column=0)
    entry = tk.Entry(frame_inputs)
    entry.grid(row=i, column=1)
    entry_widgets[col] = entry

# Frame dos botões
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Adicionar", command=adicionar_registro).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Editar", command=editar_registro).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Apagar", command=apagar_registro).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Salvar", command=salvar_dados).grid(row=0, column=3, padx=5)

root.mainloop()
