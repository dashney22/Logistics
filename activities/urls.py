from django.urls import path
from django.views.generic.dates import DateDetailView
from .views import BaseView, PostView, PostDetail, CreatePost, UpdatePostView, DeletePostView,UserRegistrationView,LikeView ,login_Request,AddCategoryView, CategoryView, AddCommentView

urlpatterns = [
    path('',BaseView, name="home"),
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', login_Request, name="login"),
    path('posts/',PostView.as_view(), name="share-thoughts"),
    path('post/<int:pk>/' ,PostDetail.as_view(), name="post-detail"),
    path('add_post/',CreatePost.as_view(), name="add-post"),
    path('add_category/',AddCategoryView.as_view(), name="add-category"),
    path('post/<int:pk>/edit', UpdatePostView.as_view(),name='update-post'),
    path('post/delete/<int:pk>', DateDetailView.as_view(), name="delete-post"),
    path('category/<str:cats>/', CategoryView, name="category"),
    path("like/<int:pk>", LikeView, name="like-post"),
    path("comment/", AddCommentView.as_view(), name="add-comment"),
]