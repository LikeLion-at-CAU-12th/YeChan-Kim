from django.urls import path
from posts.views import *

urlpatterns = [
    #path('', post_list, name="post_list"),
    #path('<int:id>', post_detail, name = "post_detail"),
    #path('<int:id>/comment', comment_detail, name = "comment_detail"),
    #path('recent', view_recent_week, name = "recent_week"),
    path('', PostList.as_view()),
    path('<int:id>/', PostDetail.as_view()),
    path('<int:id>/comment', CommentList.as_view()),
]