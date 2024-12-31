import re
import csv
import chardet
from django.db import IntegrityError
from django.shortcuts import render
from makemake.imports.forms import *


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

def import_sinapi_file():
    pass

# Import compositions .csv files
# input : A .csv file
# output : ?? To define 
def icompositions(request):
    if request.method == 'POST':
        form = ImportPricesForm(request.POST, request.FILES)
        if form.is_valid():
            # O arquivo enviado está em request.FILES['file']
            uploaded_file = request.FILES['upload_url']
            
            # Certifique-se de que o arquivo é de texto
            if uploaded_file.content_type == 'text/plain':
                # Lendo o conteúdo do arquivo
                raw_data = uploaded_file.read()
                # Detectando a codificação do arquivo
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                
                # Rewind do arquivo para reler corretamente com a codificação correta
                uploaded_file.seek(0)

                # Lendo o arquivo CSV com a codificação detectada
                decoded_file = raw_data.decode(encoding)

                # Usando csv.reader para processar o arquivo CSV
                items = csv.reader(decoded_file.splitlines())

                # Aqui você pode processar o conteúdo como desejar
                # Exemplo: quebrar em linhas
                #lines = content.splitlines()
                print("Inserting materials at composition table")
                for item in items:
                        delimiter = '\t'
                        # Remove a nova linha e divide por tabulação
                        line = item[0].strip().split(delimiter)
                        if len(line) < 5:
                            continue
                        CODE = line[0].replace("'",'')
                        TEXT = clean_text(line[1])
                        UNIT = line[2].strip()
                        value = processar_string(line[2])
                        try:
                            # instance_unit = Unit.objects.get(symbol__iexact=value.lower())
                            # instance = Composition(code=CODE, dbtype=2, description=TEXT, type=1, unit=instance_unit)
                            # instance.save()
                            print(CODE, TEXT, UNIT, value)
                        except IntegrityError:
                            pass
                
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