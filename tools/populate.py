import django
import os
import sys

import time
import sys

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