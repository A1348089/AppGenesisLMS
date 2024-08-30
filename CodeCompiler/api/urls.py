from django.urls import path
from CodeCompiler.views import * 

urlpatterns = [
    path('code/', CodeExecutionView.as_view(), name="code-compiler"),
]
