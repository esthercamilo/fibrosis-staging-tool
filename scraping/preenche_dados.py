import os
import sys
import django
import json

from django.utils.termcolors import background

sys.path.append('.')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from api.models import Goal, Skill, Competence, KnowledgeObject, Background, StudentQuestion, Student

#competence = Competence(code='exemplo1' , description='sjjsgusdjf')
#competence.save()

student = Student(fullname= 'Leticia Camilo', objective_id= 1, date_objective_definition='2024-11-05 00:00:00.000 -0300', cpf=23572354)
student.save()

print()