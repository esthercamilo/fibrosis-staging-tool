import json
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from django.forms.models import model_to_dict
from rest_framework.schemas.coreapi import field_to_schema
from rest_framework.response import Response
from api.models import Question, Institution, Student
from api.serializers import GenericSerializer, QuestionSerializer, StudentSerializer
from django.core.exceptions import ObjectDoesNotExist




class QuestionView(viewsets.ViewSet):

    @swagger_auto_schema(operation_id="Atualiza questão", tags=['Questões'], request_body=GenericSerializer)
    def put(self, request, question_id,  *kwargs):
        """
         atualiza antiga
        """
        try:
            question=Question.objects.get(id=question_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": 'Esse id não existe ou não é válido'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        field_to_update = []

        if 'institution' in data:
            try:
                institution = Institution.objects.get(id=data['institution'])
                question.institution = institution
            except ObjectDoesNotExist:
                return JsonResponse({"error": 'Institution com esse ID não existe'}, status=status.HTTP_400_BAD_REQUEST)


        for field, value in data.items():
            if hasattr(question, field) and field != 'institution':
                setattr(question, field, value)
                field_to_update.append(field)

        question.save()
        return JsonResponse({"response": f"dados recebidos com sucesso"}, status=status.HTTP_200_OK)



    @swagger_auto_schema(operation_id="Cria questão", tags=['Questões'], request_body=QuestionSerializer)
    def post(self, request, *kwargs):

        """
         Cria questão
        """
        institution_sigla = request.data.get('institution').strip()
        try:
            institution = Institution.objects.get(sigla__iexact=institution_sigla)
        except Institution.DoesNotExist:
            return JsonResponse({"error": "Instituição não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        novo_dict = request.data.copy()
        novo_dict.pop('institution')
        novo_dict['institution'] = institution


        question = Question(**novo_dict)
        question.save()

        return JsonResponse({"response": "Dados recebidos com sucesso"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_id="Obtém questão", tags=['Questões'])
    def get(self, request, question_id, *kwargs):
        """
        Obtém questão
        """
        try:
            question = model_to_dict(Question.objects.get(id=question_id))
            return JsonResponse({"response": question}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return JsonResponse({"error": 'Esse id não existe ou não é válido'}, status=status.HTTP_400_BAD_REQUEST)



    @swagger_auto_schema(operation_id="Exclui", tags=['Questões'])
    def delete(self, request, question_id, *kwargs):
        """
        Deletar questão
        """
        try:
            question = Question.objects.get(id=question_id)
            question.delete()
            return JsonResponse({"response": f"id excluido"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return JsonResponse({"error": 'Esse id não existe ou não é válido'}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(operation_id="Mostra as questões", tags=['Questões'])
    def show_all(self, request, *kwargs):

        """
         Mostra todas as questões cadastradas
        """

        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class StudentView(viewsets.ViewSet):
    @swagger_auto_schema(operation_id="Obtém dados dos estudantes", tags=['Estudantes'])
    def get(self, request, student_id):
        try:
            estudante=Student.objects.get(id=student_id)
            estudante_dict=model_to_dict(estudante)
            return JsonResponse(estudante_dict)
        except Exception as e:
            return JsonResponse({'error':str(e)})


    @swagger_auto_schema(operation_id="Exclui um estudante", tags=['Estudantes'])
    def delete(self, request, student_id):
        try:
            estudante=Student.objects.get(id=student_id)
            estudante.delete()
            return JsonResponse({"response": f"id excluido"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return JsonResponse({'error':'Esse id não existe ou não é válido'})

    @swagger_auto_schema(operation_id="Atualiza dados do estudante", tags=['Estudantes'], request_body=StudentSerializer)
    def put(self, request, student_id):
        try:
            estudante=Student.objects.get(id=student_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": 'Esse id não existe ou não é válido'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = StudentSerializer(estudante, data=request.data,
                                       partial=True)  # 'partial=True' permite atualizar campos específicos
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"response": "dados recebidos com sucesso"}, status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_id="Cadastra um novo estudante", tags=['Estudantes'], request_body=StudentSerializer)
    def post(self, request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"response": "Estudante criado com sucesso"}, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(operation_id="Filtra dados dos estudantes", tags=['Estudantes'])
    def filter(self, request):
        objective_id = request.GET.get('objective_id')

        estudantes = Student.objects.all()

        if objective_id is not None:
            estudantes = estudantes.filter(objective_id=objective_id)

        serializer = StudentSerializer(estudantes, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)