from rest_framework import serializers

from api.models import Question, Student


class GenericSerializer(serializers.Serializer):
    class Meta:
        model = Question
        fields = ['id', 'html', 'answer_option', 'answer_description', 'year', 'institution_id']

    def create(self, validated_data):
        return Question.objects.create(**validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'html', 'answer_option', 'answer_description', 'year', 'institution_id']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Student
        fields= ['id', 'fullname', 'objective_id', 'date_objective_definition', 'cpf', 'user_id']