from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, Http404
from .models import Post, Category, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import PostForm, CategoryForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CommentForm
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext


def handler404(request, exception):
    return render(request, 'blog_app/404.html')


class HomeView(ListView):                   # view to use
    model = Post                            # model to use
    template_name = 'blog_app/home.html'    # temp to use
    ordering = ['-date']
    paginate_by = 5

    # code to pass categories as context to the home view so they appear in nav bar
    # for class based views we need to define context this way
    def get_context_data(self, *args, **kwargs):
        menu_items = Category.objects.all().values
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["menu"] = menu_items

        # print(context)
        return context

# detailed view of individual posts
# this view will automatically get the post with the pk that was passed with the url pattern


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/detail.html'

    def get_context_data(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        context = super(PostDetailView, self).get_context_data(
            *args, **kwargs)

        liked = False

        user_liked = post.likes.filter(id=self.request.user.id)

        if user_liked:
            liked = True

        context["liked"] = liked
        return context


class AddPostView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm       # use our form
    template_name = 'blog_app/add_post.html'
    success_message = "Post added successfully!"
    # put all fields from model on the page
    # fields = '__all__'


class EditPostView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog_app/update_post.html'
    success_message = "Post updated!"


class DeletePostView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog_app/delete_post.html'
    success_message = "Post deleted!"

    # redirect after a post is deleted
    def get_success_url(self):
        return reverse('home')

    # for success message in delete view we do this -->
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeletePostView, self).delete(request, *args, **kwargs)


class AddCategoryView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'blog_app/add_category.html'
    form_class = CategoryForm
    success_message = "Category added!"
    # put all fields from model on the page
    # fields = '__all__'

    # pass categories to view

    def get_context_data(self, *args, **kwargs):
        menu_items = Category.objects.all().values
        context = super(AddCategoryView, self).get_context_data(
            *args, **kwargs)
        context["menu"] = menu_items

        # print(context)
        return context


def FilterView(request, cat):
    filtered_posts = Post.objects.filter(category=cat).all().order_by('-date')
    total = len(filtered_posts.values_list())

    page = request.GET.get('page', 1)

    paginator = Paginator(filtered_posts, 5)

    try:
        filtered_posts = paginator.page(page)
    except PageNotAnInteger:
        filtered_posts = paginator.page(1)
    except EmptyPage:
        filtered_posts = paginator.page(paginator.num_pages)

    context = {
        'category': cat,
        'posts': filtered_posts,
        'total': total
    }

    return render(request, 'blog_app/filtered.html', context)


def FilterAuthorView(request, id):
    filtered_posts = Post.objects.filter(author_id=id).all().order_by('-date')
    total = len(filtered_posts.values_list())

    print(total)
    if total == 0:
        raise Http404("error")

    else:

        page = request.GET.get('page', 1)

        paginator = Paginator(filtered_posts, 5)

        try:
            filtered_posts = paginator.page(page)
        except PageNotAnInteger:
            filtered_posts = paginator.page(1)
        except EmptyPage:
            filtered_posts = paginator.page(paginator.num_pages)

        context = {
            'author': User.objects.get(id=id),
            'posts': filtered_posts,
            'total': total
        }

        return render(request, 'blog_app/filtered_author.html', context)


@login_required
def LikeView(request, pk):
    # get the post to like
    post = get_object_or_404(Post, id=pk)

    # check if logged in user has liked post
    user_liked = post.likes.filter(id=request.user.id)

    if user_liked:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    # return HttpResponseRedirect(reverse('detail', args=[str(pk)]))

    return redirect('detail', post.pk)


@login_required
def CommentView(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        print(request.POST)

        c = Comment.objects.create(post_id=pk, name=get_current_user(
        ), body=request.POST.get('body'))

        post.comments.add(c)

        return redirect('detail', post.pk)

    context = {
        "form": CommentForm,
        "post": post
    }

    return render(request, 'blog_app/comment.html', context)


class DeleteCommentView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog_app/delete_comment.html'
    success_message = "Comment deleted!"

    # redirect after a post is deleted
    def get_success_url(self):
        return reverse('home')

    # for success message in delete view we do this -->
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteCommentView, self).delete(request, *args, **kwargs)


def aboutView(request):
    return render(request, 'blog_app/about.html')
