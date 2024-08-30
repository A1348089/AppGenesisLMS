from django.db import connection # for SQL
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import subprocess
import sys

####################################### Code Compiler View Start ####################################
class CodeExecutionView(APIView):
    def get(self, request, *args, **kwargs):

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
                        "code": code,
                        "output": output,
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
                "code": code,
                "output": result.stdout.strip(),
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
        
####################################### Code Compiler View End ####################################