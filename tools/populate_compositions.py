import os
import csv
import re
from datetime import *

import django
from django.db import IntegrityError
from django.db.models import Q

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'makemake.settings'
django.setup()

from makemake.compositions.models import Composition, CompositionHasComponents
from makemake.units.models import Unit

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

print("Reading .txt file - materials nao desonerado")
items = ler_csv_tab('extras/sinapi_materials_ndeso.txt')

print("Inserting materials at composition table")
for item in items:
        if len(item) < 5:
            continue
        CODE = item[0].replace("'",'')
        TEXT = clean_text(item[1])
        UNIT = item[2].strip()
        value = processar_string(item[2])
        try:
            instance_unit = Unit.objects.get(symbol__iexact=value.lower())
            instance = Composition(code=CODE, dbtype=2, description=TEXT, type=1, unit=instance_unit)
            instance.save()
        except IntegrityError:
            pass

print("Reading .txt file - materials")
items = ler_csv_tab('extras/sinapi_materials_deso.txt')

print("Inserting materials at composition table")
for item in items:
        if len(item) < 5:
            continue
        CODE = item[0].replace("'",'')
        TEXT = clean_text(item[1])
        UNIT = item[2].strip()
        value = processar_string(item[2])
        try:
            instance_unit = Unit.objects.get(symbol__iexact=value.lower())
            instance = Composition(code=CODE, dbtype=2, description=TEXT, type=1, unit=instance_unit)
            instance.save()
        except IntegrityError:
            pass

print("Reading .txt file -  compositions")
items = ler_csv_tab('extras/sinapi_compositions.txt')

print("Inserting compoments at composition table")
for item in items:

    #try:

        if len(item) < 5:
            continue
        code_composition = processar_string(item[6])
        desccomposition = item[7]
        unit = processar_string(item[8]).lower()
        tipo = processar_string(item[11])
        code_component= processar_string(item[12])
        desccomponent = item[13]
        origin = item[15]
        price = origin_func(origin)
        qty = item[16].replace(',','.')

        if code_composition != '' and code_component == '':
            try:
                instance_unit = Unit.objects.get(Q(symbol__iexact=unit) | Q(symbol_alternative1__iexact=unit) | Q(symbol_alternative2__iexact=unit))
            except:
                u1 = Unit(name=unit, symbol=unit, symbol_alternative1=unit, symbol_alternative2=unit,)
                u1.save()
                instance_unit = Unit.objects.get(Q(symbol__iexact=unit) | Q(symbol_alternative1__iexact=unit) | Q(symbol_alternative2__iexact=unit))
            
            is_instance_exist = Composition.objects.filter(Q(code=code_composition) & Q(dbtype=2)).exists()
            if is_instance_exist:
                instance1 = Composition.objects.filter(Q(code=code_composition) & Q(dbtype=2)).update(code=code_composition, description=desccomposition, dbtype=2,  type=1, unit=instance_unit, iscomposition=True,)
            else:
                instance1 = Composition.objects.create(code=code_composition, description=desccomposition, dbtype=2, type=1, unit=instance_unit, iscomposition=True)

        elif code_composition != '' and not (code_component == ''):
            if tipo == 'insumo':
                b1 = Composition.objects.get(code=code_composition)
                b2 = Composition.objects.get(code=code_component)
                exist = CompositionHasComponents.objects.filter(Q(composition_master=b1) & Q(composition_slave=b2)).exists()
                if not exist:
                    b3 = CompositionHasComponents.objects.create(composition_master=b1, composition_slave=b2, quantity=qty, origin=price)
            if tipo == 'composicao':
                b1 = Composition.objects.get(Q(code=code_composition) & Q(dbtype=2))
                exist = Composition.objects.filter(Q(code=code_component) & Q(dbtype=2)).exists()

                if not exist:
                    instance1 = Composition.objects.create(code=code_component, description=desccomponent, dbtype=2, type=1, unit=instance_unit, iscomposition=True)
                    b3 = CompositionHasComponents.objects.create(composition_master=b1, composition_slave=instance1, quantity=qty, origin=price)
                else:
                    b2 = Composition.objects.get(Q(code=code_component) & Q(dbtype=2))
                    b3 = CompositionHasComponents.objects.create(composition_master=b1, composition_slave=b2, quantity=qty, origin=price)
