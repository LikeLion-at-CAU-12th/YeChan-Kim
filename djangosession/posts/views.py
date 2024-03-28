from django.shortcuts import render
from django.http import JsonResponse # �߰� 
from django.shortcuts import get_object_or_404 # �߰�

# Create your views here.

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello lielion-12th!"
        })
    
def index(request):
    return render(request, 'index.html')

def info(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '메시지 전달 성공',
            'data' : [
                {
                    "name" : "김예찬",
                    "age" : 25,
                    "major" : "Computer Science & Engineering"
                },
                {
                    "name" : "박연우",
                    "age" : 22,
                    "major" : "Computer Science & Engineering"
                }
            ]
        },
        json_dumps_params={'ensure_ascii': False})