import re
import csv
import chardet
from django.shortcuts import render
from makemake.imports.forms import *

# Read .csv file
def ler_csv_tab_delimitado(caminho_arquivo):
    """
    Lê um arquivo .csv separado por tabulação e retorna o conteúdo como uma lista de dicionários.
    
    Parâmetros:
    caminho_arquivo (str): O caminho para o arquivo .csv.

    Retorna:
    List[Dict[str, str]]: Uma lista de dicionários, onde cada dicionário representa uma linha do arquivo.
    """
    with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
        leitor = csv.DictReader(csvfile, delimiter='\t')
        dados = [linha for linha in leitor]
    return dados

def ler_csv_tab(file_path, delimiter='\t'):
    """
    Lê um arquivo CSV separado por tabulação e retorna uma tabela (lista de listas).

    Args:
    file_path (str): O caminho do arquivo CSV a ser lido.

    Returns:
    list: Uma lista de listas onde cada sublista representa uma linha do arquivo.
    """
    tabela = []

    # Avoid character u'\ufeff' , use encoding='utf-8-sig' not encoding='utf-8'
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            for line in file:
                # Remove a nova linha e divide por tabulação
                linha = line.strip().split(delimiter)
                #linha = line.strip().split('|')
                tabela.append(linha)
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='utf-16') as file:
            for line in file:
                # Remove a nova linha e divide por tabulação
                linha = line.strip().split(delimiter)
                #linha = line.strip().split('|')
                tabela.append(linha)
    
    return tabela

def processar_string(texto):
    """
    Remove todos os espaços de uma string e converte todas as letras maiúsculas em minúsculas.

    Args:
    texto (str): A string a ser processada.

    Returns:
    str: A string processada sem espaços e com letras minúsculas.
    """
    # Remove todos os espaços da string
    texto_sem_espacos = texto.replace(" ", "")
    # Converte todas as letras maiúsculas em minúsculas
    texto_processado = texto_sem_espacos.lower()
    
    return texto_processado

def clean_text(text):
  """
  Remove caracteres especiais no início e fim do texto.

  Args:
    text: Texto a ser limpo.

  Returns:
    Texto limpo com caracteres especiais removidos.
  """
  pattern = r"^[\'\"\s]+|[\'\"\s]+$"  # Padrão regex para caracteres especiais
  return re.sub(pattern, "", text)

def origin_func(item):
    item = item.strip().upper()
    if item == 'COEFICIENTE DE REPRESENTATIVIDADE':
        return 1
    elif item == 'COLETADO':
        return 2
    else:
        return 0

# Create your views here.
def icompositions(request):
    if request.method == 'POST':
        form = ImportPricesForm(request.POST, request.FILES)
        if form.is_valid():
            # O arquivo enviado está em request.FILES['file']
            uploaded_file = request.FILES['upload_url']
            
            # Certifique-se de que o arquivo é de texto
            if uploaded_file.content_type == 'text/plain':
                # Lendo o conteúdo do arquivo
                #content = uploaded_file.read().decode('utf-8')  # Decodifique o conteúdo para string
                # Detectando a codificação do arquivo
                raw_data = uploaded_file.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                
                # Rewind do arquivo para reler corretamente com a codificação correta
                uploaded_file.seek(0)

                # Lendo o arquivo CSV com a codificação detectada
                decoded_file = raw_data.decode(encoding)

                # Aqui você pode processar o conteúdo como desejar
                # Exemplo: quebrar em linhas
                lines = content.splitlines()
                
                # Retornar as linhas para o template, por exemplo
                return render(request, 'file_processed.html', {'lines': lines})
            else:
                return render(request, 'imports/icompositions.html', {'form': form, 'error': 'Por favor, envie um arquivo de texto.'})
    else:
        form = ImportPricesForm()

    return render(request, 'imports/icompositions.html', {'form': form})

def ImportPrices(request):
    if request.method == 'POST':    # Newly filled form
        pass
    else:
        form = ImportPricesForm()
    context = {'form': form}
    return render(request, 'prices/imports.html', context)