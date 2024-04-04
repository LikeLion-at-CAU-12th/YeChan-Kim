from django.shortcuts import render
from django.http import JsonResponse 
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from posts.models import * 

# Create your views here.

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello likelion-12th!"
        })
    
def index(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def get_post_detail(request, id):
    post = get_object_or_404(Post, pk = id)
    post_detail_json = {
        "id" : post.id,
        "title" : post.title,
        "content" : post.content,
        "writer" : post.writer,
        "category" : post.category,
    }

    return JsonResponse({
        'status' : 200,
        'message' : '게시글 조회 성공',
        'data' : post_detail_json
    })

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