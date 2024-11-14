from django.db import models
from django.contrib.auth.models import User


class Institution(models.Model):
    """
    Instituição que organizou a questão, por exemplo: USP, UNESP.
    """
    DoesNotExist = None
    id = models.AutoField(primary_key=True)
    sigla = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=200, null=True)


class Goal(models.Model):
    """
    É um cadastro de objetivos.
    O objetivo é um estudante simulado que teve desempenho almejado para determinado exame.
    Pode ser ainda a média de um conjunto de estudantes que ficará previamente cadastrado
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)  # ENEM
    score_by_skill = models.JSONField(null=True)
    description = models.TextField(null=True, blank=True)


class KnowledgeObject(models.Model):
    """Exemplo: Energia cinética"""

    """Habilidades descritas na Base Curricular Nacional"""
    SUPER_CHOICES = [
        (1, 'Linguagens'),
        (2, 'Matemática'),
        (3, 'Ciências da Natureza'),
        (4, 'Ciências Humanas')
    ]

    TEMATIC_UNIT_CHOICES = [

        (1, 'Leitura e escuta'),
        (2, 'Escrita'),
        (3, 'Análise linguística / Semiótica'),
        (4, 'Oralidade'),

        (10, 'Números'),
        (11, 'Álgebra'),
        (12, 'Geometria'),
        (13, 'Grandezas e medidas'),
        (14, 'Probabilidade e estatística'),

        (20, 'Matéria e energia'),
        (21, 'Vida, Terra e Cosmos'),

        (30, 'Geografia: o sujeito e seu lugar no mundo'),
        (31, 'História'),
        # Finalizar o cadastro
    ]

    GRADE_CHOICES = [
        (1, '1ºAno EF'),
        (2, '2ºAno EF'),
        (3, '3ºAno EF'),
        (4, '4ºAno EF'),
        (5, '5ºAno EF'),
        (6, '6ºAno EF'),
        (7, '7ºAno EF'),
        (8, '8ºAno EF'),
        (9, '9ºAno EF'),
        (10, '1ºAno EM'),
        (11, '2ºAno EM'),
        (12, '3ºAno EM')
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    description = models.TextField(default="", null=True, blank=True)
    superfield = models.IntegerField(choices=SUPER_CHOICES, null=True, verbose_name="Área")
    tematic_unit = models.IntegerField(choices=TEMATIC_UNIT_CHOICES, null=True, verbose_name="Unidade temática")


class Competence(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20)
    description = models.TextField()


class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(default="", null=True, blank=True)
    # Exemplo: EF04MA20 é o código usado pela Base Nacional Comum Curricular
    code = models.CharField(max_length=20)
    competence = models.ForeignKey(Competence, on_delete=models.SET_NULL, null=True)
    # Pode depender de muitas habilidades para se concretizar
    dependent_skills = models.ManyToManyField('self', symmetrical=False, related_name='dependencies')


class SkillConsolidation(models.Model):
    """Tempo praticando uma habilidade"""
    id = models.AutoField(primary_key=True)
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True)
    time = models.FloatField(null=True)


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=500)
    cpf = models.CharField(max_length=500, null=True)
    objective = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True)
    date_objective_definition = models.DateTimeField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='student_user')
    skillconsolidationset = models.ManyToManyField(SkillConsolidation, related_name='student_skillconsolidation')


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    statement = models.TextField(null=True)
    image = models.FilePathField(null=True)
    html = models.TextField(null=False)
    answer_option = models.CharField(max_length=10, null=False)  # a, b, c ou i, ii, iii, etc.
    answer_description = models.TextField(default="", null=False, blank=True)
    kos = models.ManyToManyField(KnowledgeObject, related_name='question_ko')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=False)
    year = models.IntegerField(null=False)
    skill = models.ManyToManyField(Skill, related_name='question_skill', null=True)


class Background(models.Model):
    """Material necessário para o desenvolvimento de KOS e Skills"""
    id = models.AutoField(primary_key=True)
    ko = models.ForeignKey(KnowledgeObject, on_delete=models.CASCADE, null=True)
    html = models.TextField(null=True)  # usar safe no template
    video = models.FilePathField(null=True)


class StudentQuestion(models.Model):
    """Questões respondidas"""
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # Performance indicators
    date_solved = models.DateTimeField(null=True)
    time_resolution = models.FloatField(null=True)  # Seconds
    attempt_number = models.IntegerField(default=0)
    finalscore = models.FloatField(null=True)
    associated_goal = models.ManyToManyField(Goal, related_name="studentquestion_goal", null=True)
