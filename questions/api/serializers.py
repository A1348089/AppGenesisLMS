from rest_framework import serializers

from questions.models import Questions

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'