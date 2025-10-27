import csv

arquivo = 'gammanotes.csv'  # Nome do arquivo original
#arquivo_saida = 'gammanotes_atualizado.csv'  # Nome do arquivo de saída

# Carrega o conteúdo do arquivo original
with open(arquivo, 'r', newline='', encoding='utf-8') as f:
    reader = list(csv.reader(f))
    cabecalho = reader[0]
    linhas = reader[1:]

# Guarda o padrão do primeiro registro
padrao = linhas[0][:]  # copia todos os campos do primeiro registro

# Identifica o índice do campo Note
try:
    idx_note = cabecalho.index("Note")
except ValueError:
    idx_note = 2  # fallback para terceira coluna se não encontrar

# Loop interativo para adicionar ou apagar registros
while True:
    print("\nEscolha uma opção:")
    print("1 - Adicionar novo registro")
    print("2 - Apagar registro existente (escolhendo da lista)")
    print("Enter - Finalizar edição")
    opcao = input("Opção: ")

    if opcao == '':
        break
    elif opcao == '1':
        simbolo = input('Digite o símbolo: ')
        valor = input('Digite o preço: ')
        nota = input('Digite a nota: ')
        cor = input('Cor da nota: #')
        novo_registro = padrao[:]  # copia o padrão
        novo_registro[0] = simbolo + '.CME@RITHMIC'  # acrescenta o sufixo
        novo_registro[1] = valor
        novo_registro[2] = nota
        novo_registro[3] = '#ffffff'    # cor da letra
        novo_registro[4] = '#' + cor
        linhas.append(novo_registro)
        print(f"Linha adicionada: {novo_registro}")
    elif opcao == '2':
        print("\nRegistros disponíveis para apagar:")
        for idx, linha in enumerate(linhas):
            simbolo = linha[0]
            valor = linha[1]
            nota = linha[2]
            print(f"{idx}: símbolo = {simbolo}, valor = {valor}, nota = {nota}")
        indice_apagar = input("\nDigite o número do registro que deseja apagar: ")
        try:
            indice_apagar = int(indice_apagar)
            if 0 <= indice_apagar < len(linhas):
                registro_removido = linhas.pop(indice_apagar)
                print(f"Registro removido: símbolo = {registro_removido[0]}, valor = {registro_removido[1]}")
            else:
                print("Índice inválido. Nenhum registro foi removido.")
        except ValueError:
            print("Entrada inválida. Nenhum registro foi removido.")
    else:
        print("Opção inválida. Tente novamente.")

# Pergunta se deseja salvar o arquivo
salvar = input(f'\nDeseja salvar o arquivo como "{arquivo}"? (s/n): ')
if salvar.lower() == 's':
    with open(arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(cabecalho)
        writer.writerows(linhas)
    print('Arquivo atualizado com sucesso!')
else:
    print('Arquivo não foi salvo.')