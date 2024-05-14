import django
import os
import sys

import time

import csv
import re
from datetime import *

from django.db import IntegrityError
from django.db.models import Q

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

def progresso2(iterable, prefix='', size=60, out=sys.stdout):
    """
    Exibe uma barra de progresso para um iterável de tamanho desconhecido.

    Args:
    iterable (iterable): Qualquer iterável que você deseja processar.
    prefix (str): Uma string opcional para ser exibida antes da barra de progresso.
    size (int): O comprimento da barra de progresso.
    out (file object): O fluxo de saída onde a barra de progresso será escrita (padrão: sys.stdout).
    """
    def show(j, total):
        x = int(size * j / total) if total else 0
        out.write(f"{prefix}[{'#' * x}{'.' * (size - x)}] {j}/{total or '?'}\r")
        out.flush()

    count = 0
    total = None

    try:
        total = len(iterable)
    except TypeError:
        pass

    show(count, total)
    for item in iterable:
        count += 1
        yield item
        show(count, total)

    out.write('\n')
    out.flush()

# # Exemplo de uso com um gerador de tamanho desconhecido
# def gerador():
#     for i in range(100):
#         time.sleep(0.1)  # Simula uma tarefa que demora um pouco
#         yield i

# for item in progresso(gerador(), prefix='Progresso:', size=50):
#     pass  # Processa cada item do gerador


def progresso(iterable, prefix='', size=60, out=sys.stdout):
    """
    Exibe uma barra de progresso.

    Args:
    iterable (iterable): Qualquer iterável que você deseja processar.
    prefix (str): Uma string opcional para ser exibida antes da barra de progresso.
    size (int): O comprimento da barra de progresso.
    out (file object): O fluxo de saída onde a barra de progresso será escrita (padrão: sys.stdout).
    """
    count = len(iterable)

    def show(j):
        x = int(size * j / count)
        out.write(f"{prefix}[{'#' * x}{'.' * (size - x)}] {j}/{count}\r")
        out.flush()

    show(0)
    for i, item in enumerate(iterable, 1):
        yield item
        show(i)
    out.write('\n')
    out.flush()

 # Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'makemake.settings'
django.setup()

print("Populating USERS")
from django.contrib.auth.models import User
#for index in range(100):
for index in progresso(range(100), prefix='Progress:', size=50):
    name = "user"
    name = name + str(index+1)
    instance = User(username=name)
    instance.set_password(name) # Criptography password
    instance.save()

print("Populating CATEGORIES")
from makemake.categories.models import Category
categories = [  ("ELE", "ELÉTRICA", "ELÉTRICA", ('doc', '',), ''),
                ("ARQ", "ARQUITETURA","ARQUITETURA", ('doc','',), ''),
                ("TEL", "TELECOMUNICAÇÕES","TELECOMUNICAÇÕES",('doc','',), ''),
                ("AUT", "AUTOMAÇÃO","AUTOMAÇÃO",('doc','',), ''),
                ("CIV", "CIVIL","CIVIL", ('doc','',), ''),
                ("EST", "ESTRUTURAS","ESTRUTURAS", ('doc','budget',), ''),
                ("DRE", "DRENAGEM","DRENAGEM", ('doc','',), ''),
                ("HVA", "HVAC","HVAC", ('doc','',), ''),
                ("Z00", "Serviços de Escritório, Laboratório e Campo","Serviços de Escritório, Laboratório e Campo", ('', 'budget',), ''),
                ("Z01", "Canteiro de Obra", "Canteiro de Obra", ('', 'budget',), ''),
                ("Z02", "Movimento de Terra", "Movimento de Terra", ('', 'budget',), ''),
                ("Z03", "Transportes", "Transportes", ('', 'budget',), ''),
                ("Z04", "Serviços Complementares", "Serviços Complementares", ('', 'budget',), ''),
                ("Z05", "Galeria, Drenos e Conexos", "Galeria, Drenos e Conexos", ('', 'budget',), ''),
                ("Z06", "Argamassa, Injeções e Consolidações", "Argamassa, Injeções e Consolidações", ('', 'budget',), ''),
                ("Z07", "Bases e Pavimentos", "Bases e Pavimentos", ('', 'budget',), ''),
                ("Z08", "Serviços de Parques e Jardins", "Serviços de Parques e Jardins", ('', 'budget',), ''),
                ("Z09", "Fundações", "Fundações", ('', 'budget',), ''),
                ("Z10", "Alvenaria e Divisórias", "Alvenaria e Divisórias", ('', 'budget',), ''),
                ("Z11", "Revestimento de Paredes, Tetos e Pisos", "Revestimento de Paredes, Tetos e Pisos", ('', 'budget',), ''),
                ("Z12", "Esquadrias de PVC, Ferro, Alumínio ou Madeira, Vidraças e Ferragens","Esquadrias de PVC, Ferro, Alumínio ou Madeira, Vidraças e Ferragens", ('', 'budget',), ''),
                ("Z13", "Instalações Elétricas, Hidráulicas, Sanitárias e Mecânicas", "Instalações Elétricas, Hidráulicas, Sanitárias e Mecânicas", ('', 'budget',), ''),
                ("Z14", "Coberturas, Isolamentos e Impermeabilizações","Coberturas, Isolamentos e Impermeabilizações", ('', 'budget',), ''),
                ("Z15", "Pinturas","Pinturas", ('', 'budget',), ''), 
                ("Z16", "Aparelhos Hidráulicos, Sanitários Elétricos, Mecânicos e Esportivos", "Aparelhos Hidráulicos, Sanitários Elétricos, Mecânicos e Esportivos", ('', 'budget',), ''),
                ("Z17", "Aluguel de Equipamentos", "Aluguel de Equipamentos", ('', 'budget',), ''),
                ("Z18", "Custos Rodoviários", "Custos Rodoviários", ('', 'budget',), ''), 
                ("ILU", "Iluminação", "Iluminação", ('doc', 'budget',), 'ELE'),
                ("ILP", "Iluminação Pública", "Iluminação Pública", ('doc', 'budget',), 'ILU'),
                ("ILE", "Iluminação Externa", "Iluminação Externa", ('doc', 'budget',), 'ILU'),
                ("ILC", "Iluminação Cênica", "Iluminação Cênica", ('doc', 'budget',), 'ILU'),
                ("Z19", "Reflorestamento e Exploração Florestal", "Reflorestamento e Exploração Florestal", ('', 'budget',), ''),
                ]
for category in categories:
    a = category[3][0] != ''
    b = category[3][1] != ''
    try:
        instance = Category.objects.get(code=category[4].upper())
    except:
        instance = None
    instance = Category(code=category[0].upper(), name=category[1], description=category[2], fordocs=a, forbudgets=b,)
    instance.save()


print("Populating SITES")
from makemake.sites.models import Site
sites = [   ("Campus Manguinhos", 19),
            ("Campus Hélio Fraga",19),
            ("Campus Mata Atlântica",19),
            ("Farmanguinhos",19),
            ("IBEX",19),
            ("Instituto Fernandes Figueira",19),
            ("FIOCRUZ Amazônia", 4)]
for site in sites: 
    instance = Site(name=site[0], place=site[1])
    instance.save()

print("Populating COMPANIES")
from makemake.companies.models import Company
items = [   ("Mercado Livre", '12345678901234'),
            ("Magazine Luiza", '02345678901234'),
            ("Amazon", '22345678901234'),
            ("Vendinha do bairro", '32345678901234'),
            ("Concessionária de energia", '42345678901234'),]
for item in items: 
    instance = Company(name=item[0], number=item[1])
    instance.save()

print("Populating BUILDINGS")
from makemake.buildings.models import Building
buildings = [   ("Castelo FIOCRUZ", 1, 0, "Campus Manguinhos"),
                ("COGIC", 5, 0, "Campus Manguinhos"),
                ("Arthur Neiva", 4, 0, "Campus Manguinhos"),
                ("Farmácia Helio Fraga", 2, 0, "Campus Hélio Fraga"),
                ("Diretoria HF", 6, 0, "Campus Hélio Fraga"),
                ("Predio NB3", 7, 0, "Campus Hélio Fraga"),
                ("Maria Deane", 3, 0, "FIOCRUZ Amazônia"),
                ("Anexo", 8, 0, "FIOCRUZ Amazônia")]
for building in buildings:
    site_instance = Site.objects.get(name=building[3])
    instance = Building(name=building[0], number=building[1], status=building[2], site=site_instance)
    instance.save()

print("Populating UNITS")
from makemake.units.models import Unit
items = [   
    ("Conjunto", 1000, "CJ"),
    ("Metro", 2, "m"),
    ("Metro quadrado", 3, "m2"),
    ("Metro cúbico", 4, "m3"),
    ("Quilograma", 5, "kg"),
    ("Litro", 4, "l"),
    ("Quilowatt-hora", 8, "kWh"),
    ("Quilowatt", 6, "kW"),
    ("100m", 0, "100m"),
    ("310ml", 0, "310ml"),
    ("Cento", 0, "cento"),
    ("Hora", 0, "h"),
    ("JG", 0, "JG"),
    ("m/mes", 0, "m/mes"),
    ("m2/mes", 0, "m2/mes"),
    ("m2xmes", 0, "m2xmes"),
    ("Mes", 0, "mes"),
    ("Mil", 0, "mil"),
    ("mxmes", 0, "mxmes"),
    ("Par", 0, "par"),
    ("Saco 25kg", 0, "sc25kg"),
    ("T", 0, "T"),
    ("Unidade", 0, "UN"),
    ("Unidade x mês", 0, "unxmes"),
    ]
for item in items:
    instance = Unit(name=item[0], type=item[1], symbol=item[2], symbol_alternative1=item[2], symbol_alternative2=item[2])
    instance.save()

print("Populating PROJECTS")
from makemake.projects.models import Project
projects = [(1, 2023,"Projecto Teste 2023", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent at faucibus magna. Donec aliquam auctor nisi ac fermentum. Etiam convallis metus ac odio ullamcorper tempor. Aenean efficitur, augue a ornare.", 2, 1, 2, 'Interlocutor 0001', 5, 'remarks'),
            (2, 2024,"Projecto Teste 2024", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent at faucibus magna. Donec aliquam auctor nisi ac fermentum. Etiam convallis metus ac odio ullamcorper tempor. Aenean efficitur, augue a ornare.", 3, 3, 1, 'Interlocutor 0002', 5, 'remarks')]
for project in projects:
    building_instance = Building.objects.get(pk=project[4])
    manager_instance = User.objects.get(pk=project[5])
    manager_support_instance = User.objects.get(pk=project[6])
    instance = Project(code=project[0],
                       year=project[1],
                       name=project[2],
                       description=project[3],
                       project_manager=manager_instance,
                       project_manager_support=manager_support_instance,
                       interlocutor=project[7],
                       project_status=project[8],
                       remarks=project[9],
                       )
    instance.save()
    b2 = Project.objects.get(code=project[0], year=project[1])
    b2.buildings.add(building_instance)

answer = input("Deseja popular as composições? S/N?").upper()
if answer == "S":
    from makemake.compositions.models import Composition, CompositionHasComponents
    from makemake.units.models import Unit
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
