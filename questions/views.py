from django.shortcuts import render

import subprocess
import sys
from django.db import connection # for SQL

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from questions.api.serializers import QuestionSerializer
from questions.models import Questions
# Create your views here.

class QuestionsCreateView(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()

class QuestionsListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()

class QuestionsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()

class QuestionCodeCompiler(generics.RetrieveAPIView):

    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()

    def get(self, request, *args, **kwargs):
        # Retrieve the Question object
        question = self.get_object()
        serializer = self.get_serializer(question)
        question = serializer.data.get('question')
        answer = serializer.data.get('answer')

        code = request.data.get("code")
        language = request.data.get("language")

        if not code or not language:
            return Response({"error": "Code and language are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Determine the command to run based on the programming language
        if language == "python":
            cmd = [sys.executable, "-c", code]
        elif language == "javascript":
            cmd = ["node", "-e", code]
        elif language == "bash":
            cmd = ["bash", "-c", code]
        elif language == "SQLite3":
            try:
                with connection.cursor() as cursor:
                    cursor.executescript(code)
                    if "select" in code.strip().lower():
                        rows = cursor.fetchall()
                        columns = [col[0] for col in cursor.description] if cursor.description else []
                        output = [dict(zip(columns, row)) for row in rows] if rows else "Query executed successfully"
                    else:
                        output = "SQL executed successfully"
                    return Response({
                        "question":question,
                        "code": code,
                        "output": output,
                        "answer": str(answer),
                        "error": ""
                        })
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": f"Unsupported language: {language}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Execute the command with a timeout
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            
            return Response({
                "question":question,
                "code": code,
                "output": result.stdout.strip(),
                "answer": str(answer),
                "error": result.stderr.strip()
            })
        except subprocess.TimeoutExpired:
            return Response({"error": "Code execution timed out."}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except subprocess.CalledProcessError as e:
            return Response({"error": f"Command failed with return code {e.returncode}."}, status=status.HTTP_400_BAD_REQUEST)
        except FileNotFoundError:
            return Response({"error": "Command not found. Ensure the appropriate interpreter is installed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)