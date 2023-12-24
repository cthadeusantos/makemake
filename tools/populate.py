import django
import os

 # Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'makemake.settings'
django.setup()

from django.contrib.auth.models import User
users = [  ("user1", "user1"),
            ("user2", "user2"),
            ("user3", "user3")]
for user in users:
    instance = User(username=user[0], password=user[1])
    instance.save()


from makemake.categories.models import Category
categories = [  ("ELE", "ELÉTRICA", "ELÉTRICA"),
                ("ARQ", "ARQUITETURA","ARQUITETURA"),
                ("TEL", "TELECOMUNICAÇÕES","TELECOMUNICAÇÕES"),
                ("AUT", "AUTOMAÇÃO","AUTOMAÇÃO"),
                ("HVA", "HVAC","HVAC")]
for category in categories:
    instance = Category(code=category[0], name=category[1], description=category[2])
    instance.save()


from makemake.sites.models import Site
sites = [   ("Campus Manguinhos", 19),
            ("Campus Hélio Fraga",19),
            ("FIOCRUZ Amazônia", 4)]
for site in sites: 
    instance = Site(name=site[0], place=site[1])
    instance.save()


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

# from makemake.projects.models import Project

#     projects = [(code='0022024' name="Projecto Teste", description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent at faucibus magna. Donec aliquam auctor nisi ac fermentum. Etiam convallis metus ac odio ullamcorper tempor. Aenean efficitur, augue a ornare.'),
#                 (code='0022024', name="Projecto Cabify", description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet lorem at nunc tincidunt ornare ac vel diam. Aliquam sit amet lacus justo. Quisque.')]
                
#     description = models.TextField(default='', blank=True)
#     created_at = models.DateField(default=date.today, editable=True)
#     updated_at = models.DateField(default=date.today, editable=True)
#     buildings = models.ManyToManyField(Building, related_name='buildings', blank=True)
#     project_manager = models.ForeignKey(User, related_name='manager', on_delete=models.PROTECT, blank=True, null=True,)
#     project_management_support = models.ForeignKey(User, related_name='support', on_delete=models.PROTECT, blank=True, null=True,)
#     members = models.ManyToManyField(User, related_name='members', blank=True)
#     project_stakeholders = models.ManyToManyField(User, related_name='stakeholders', blank=True)
#     interlocutor = models.TextField(default='', blank=True)
#     objects = models.Manager()  # The default manager
