from django.urls import path
from questions.views import (QuestionsCreateView, QuestionsListView, QuestionsView, QuestionCodeCompiler)

urlpatterns = [
    path('', QuestionsListView.as_view(), name='question-list'),
    path('create/', QuestionsCreateView.as_view(), name='question-create'),
    path('<int:pk>/', QuestionsView.as_view(), name='question-details'),
    path('<int:pk>/code/', QuestionCodeCompiler.as_view(), name='question-code'),
]
