from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from django.http import HttpResponseRedirect
from .forms import PostForm, EditPostForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth import REDIRECT_FIELD_NAME, login, authenticate, logout

from django.contrib import messages
# Create your views here.

def BaseView(request):
    return render(request, 'activities/index.html',{})

def LikeView(request, pk):
    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

class UserRegistrationView(generic.CreateView):
    form_class=UserCreationForm
    template_name = 'activities/register.html'
    success_url = reverse_lazy('share-thoughts')

class PostView(ListView):
    model = Post
    template_name = "activities/share_thoughts.html"
    ordering = ['-post_date']
    cats = Category.objects.all()

    def get_context_data(self,*args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostView,self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class PostDetail(DetailView):
    model = Post
    template_name = "activities/detailed.html"

    def get_context_data(self,*args, **kwargs):
        cat_menu = Category.objects.all()
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context = super(PostDetail,self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        context['total_likes'] = total_likes
        context['liked'] = liked
        return context

class CreatePost(CreateView):
    model = Post
    form_class = PostForm
    template_name = "activities/add_post.html"

    def get_context_data(self,*args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(CreatePost,self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

class AddCategoryView(CreateView):
    model = Category
    fields ='__all__'
    template_name = "activities/add_category.html"

    def get_context_data(self,*args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(AddCategoryView,self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

class AddCommentView(CreateView):
    model = Comment
    fields = '__all__'
    template_name = "activities/add_comment.html"
    

def CategoryView(request, cats):
    cats_list = Post.objects.filter(category=cats)
    return render(request, 'activities/categories.html', context={"cats":cats, "category_post":cats_list})

class UpdatePostView(UpdateView):
    model =Post
    fields =  ['title','category','body']
    template_name="activities/update_post.html"

class DeletePostView(DeleteView):
    model= Post
    template_name = "activities/delete_post.html"
    success_url = reverse_lazy('share-thoughts')


def login_Request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password =password)
            if user is not None:
                login(request, user)
                print("I am in the login request")
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('home')
            else:
                messages.error(request,"Invalid Username or password")
        else:
            messages.error(request,"Invalid Username or password")
    form = AuthenticationForm()
    return render(request,"activities/login.html",{"form":form})
    

def logout_request(request):
    logout(request)
    messages.info(request, f"Logged out successfully!")
    return redirect('home')
    