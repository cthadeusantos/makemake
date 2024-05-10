import django
import os

 # Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'makemake.settings'
django.setup()

print("Populating USERS")
from django.contrib.auth.models import User
users = [  ("user1", "user1"),
            ("user2", "user2"),
            ("user3", "user3")]
for user in users:
    instance = User(username=user[0], password=user[1])
    instance.save()

print("Populating CATEGORIES")
from makemake.categories.models import Category
categories = [  ("ELE", "ELÉTRICA", "ELÉTRICA"),
                ("ARQ", "ARQUITETURA","ARQUITETURA"),
                ("TEL", "TELECOMUNICAÇÕES","TELECOMUNICAÇÕES"),
                ("AUT", "AUTOMAÇÃO","AUTOMAÇÃO"),
                ("HVA", "HVAC","HVAC")]
for category in categories:
    instance = Category(code=category[0], name=category[1], description=category[2])
    instance.save()


print("Populating SITES")
from makemake.sites.models import Site
sites = [   ("Campus Manguinhos", 19),
            ("Campus Hélio Fraga",19),
            ("FIOCRUZ Amazônia", 4)]
for site in sites: 
    instance = Site(name=site[0], place=site[1])
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

print("Populating PROJECTS")
from makemake.projects.models import Project
projects = [(1, 2023,"Projecto Teste 2023", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent at faucibus magna. Donec aliquam auctor nisi ac fermentum. Etiam convallis metus ac odio ullamcorper tempor. Aenean efficitur, augue a ornare.", 2, 1, 2, 'Interlocutor 0001'),
            (2, 2024,"Projecto Teste 2024", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent at faucibus magna. Donec aliquam auctor nisi ac fermentum. Etiam convallis metus ac odio ullamcorper tempor. Aenean efficitur, augue a ornare.", 3, 3, 1, 'Interlocutor 0002')]
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
                       interlocutor=project[6]
                       )
    instance.save()
    b2 = Project.objects.get(code=project[0], year=project[1])
    b2.buildings.add(building_instance)