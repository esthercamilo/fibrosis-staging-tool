import os
import sys
import django
from django.forms import model_to_dict
import json
sys.path.append('.')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from api.models import Skill, Student, StudentQuestion


#sk3 = Skill.objects.get(id=3)

#dependentes = sk3.dependent_skills.all()

#1. listar os estudantes

def listar_estudantes():
    lista= Student.objects.values()
    for student in lista:
        print(student)

#listar_estudantes()

#2. listar quais foram as questões resolvidas por um estudante

def listar_questao():
    estudante= Student.objects.get(id=1)
    questoes = StudentQuestion.objects.filter(student_id=estudante)

    print(f'Questões resolvidas por {estudante.fullname}:')
    for registro in questoes:
        print(f'-{registro.question.html}')

listar_questao()

#3. listar quais as habilidades necessárias para resolver uma das questões já resolvidas pelo estudante

