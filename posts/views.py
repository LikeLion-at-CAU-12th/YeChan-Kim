from django.shortcuts import render
from django.http import JsonResponse 
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from posts.models import * 
from datetime import date, timedelta
import json

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

@require_http_methods(["POST", "GET"])
def post_list(request):

    if request.method == "POST" :
        body = json.loads(request.body.decode("utf=8"))

        new_post = Post.objects.create(
            writer = body['writer'],
            title = body['title'],
            content = body['content'],
            category = body['category']
        )    

        new_post_json = {
            "id": new_post.id,
            "writer": new_post.writer,
            "title" : new_post.title,
            "content": new_post.content,
            "category": new_post.category
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 생성 성공',
            'data': new_post_json
        })
    
    if request.method == "GET" :
        post_all = Post.objects.all()

        post_json_all = []

        for post in post_all:
            post_json = {
                "id": post.id,
                "title" : post.title,
                "writer": post.writer,
                "content" : post.content,
                "category": post.category
            }

            post_json_all.append(post_json)

        return JsonResponse({
            "status" : 200,
            "message" : "게시글 목록 조회 성공",
            "data" : post_json_all
        })
    
@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, id) :

    if request.method == "GET" :
        post = get_object_or_404(Post, pk = id)

        post_json = {
                "id": post.id,
                "title" : post.title,
                "writer": post.writer,
                "content" : post.content,
                "category": post.category
        }

        return JsonResponse({
            "status" : 200,
            "message" : "메시지 조회 성공",
            "data" : post_json
        })
    
    if request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))

        update_post = get_object_or_404(Post, pk = id) #primary key.

        update_post.title = body["title"]
        update_post.content = body["content"]
        update_post.category = body["category"]

        update_post.save()

        update_post_json = {
            "id" : update_post.id,
            "writer" : update_post.writer,
            "title" : update_post.title,
            "content" : update_post.content,
            "category" : update_post.category
        }

        return JsonResponse({
            "status" : 200,
            "message" : "게시글 수정 성공",
            "data" : update_post_json
        })
    
    if request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk = id)
        delete_post.delete()

        return JsonResponse({
                'status': 200,
                'message': '게시글 삭제 성공',
                'data': None
        })
    

#특정 게시글에 포함된 모든 comment 읽어오는 API 만들기 (특정 게시글이므로 id 필요함.)
@require_http_methods(["GET"])
def comment_detail(request, id) :

    if request.method == "GET":
        post = get_object_or_404(Post, pk=id)

        comment_all = Comment.objects.filter(post_id=post)

        comment_all_json = []

        for comment in comment_all:
            comment_json = {
                "id" : comment.id,
                "post_id" : comment.post_id.id,
                "user_id" : comment.user_id,
                "content" : comment.content
            }
            comment_all_json.append(comment_json)
        
        return JsonResponse({
            "status" : 200,
            "message" : "게시글 댓글 목록 조회 성공",
            "data" : comment_all_json
        })
    
#최근 일주일 동안 작성된 게시글 목록을 볼 수 있는 기능 제작
@require_http_methods(["GET"])
def view_recent_week(request):
    
    if request.method == "GET":

        #updated_at__range = [시작 시간, 끝 시간]
        recent_all = Post.objects.filter(updated_at__range = [date.today() - timedelta(days=6), date.today()]).order_by('created_at').reverse()

        recent_json_all = []


        for recent in recent_all:
            recent_json = {
                    "id": recent.id,
                    "title" : recent.title,
                    "writer": recent.writer,
                    "content" : recent.content,
                    "category": recent.category
            }
            recent_json_all.append(recent_json)

        return JsonResponse({
            "status" : 200,
            "message" : "일주일간 포스트 조회 성공",
            "data" : recent_json_all
        })