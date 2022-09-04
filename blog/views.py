from datetime import date
from webbrowser import get
from django.shortcuts import HttpResponse, render, get_object_or_404
from .models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse
from  django.views.generic import ListView, DetailView

from  django.views import View
from .forms import CommentForm

# Create your views here.




# def home(request):
#     posts = Post.objects.all().order_by('-date')[:3] #first 3 elements [-3:] last 3 posts
#     return render(request, 'blog/index.html',{'posts':posts})


class Home(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

# def posts(request):
#     all_posts = Post.objects.all()
#     return render(request, 'blog/all-posts.html', {'posts':all_posts})

class All_Posts(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    ordering = ['-date']
    context_object_name= 'posts'

# def unique_posts(request, slug):
#     post = get_object_or_404(Post,  slug=slug)
#     return render(request, 'blog/post-detail.html', {
#         'post':post,
#         'post_tags':post.tag.all()
#     })



# class Unique_Post(DetailView):
#     template_name = 'blog/post-detail.html'
#     model = Post

#     def get_context_data(self, **kwargs):

#        context =  super().get_context_data(**kwargs)
#        context['post_tags'] = self.object.tag.all()
#        context['comment_form'] = CommentForm()
#        return context


class Unique_Post(View):
    def is_saved_post(self,request, post_id):
        stored_posts = request.session.get('stored_posts')
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        # stored_posts = request.session.get('stored__posts')
        # if stored_posts is not None:
        #     is_saved_for_later = post.id in stored_posts
        # else:
        #     is_saved_for_later = False
        context = {
            'post':post,
            'is_saved_later':self.is_saved_post(request, post.id),
            'post_tags':post.tag.all(),
            'comment_form' : CommentForm(),
            'comments': post.comments.all().order_by('-id')
        }
        return render(request, 'blog/post-detail.html', context)


    def post(self, request, slug):
        comment_post = CommentForm( request.POST)
        post = Post.objects.get(slug=slug)
        if comment_post.is_valid():
            comment = comment_post.save(commit=False) #post is being excluded so modelform so commit to false be4 saving to database
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('uniquepost', args=[slug]))

        context = {
            'post':post,
            'post_tags':post.tag.all(),
            'is_saved_later':self.is_saved_post(request, post.id),
            'comment_form' : comment_post,'comments': post.comments.all().order_by('-id')
        }
        return render(request, 'blog/post-detail.html', context)



class Read_later(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
          posts = Post.objects.filter(id__in=stored_posts)
          context["posts"] = posts
          context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)


    def post(self, request):
        stored_posts = request.session.get('stored_posts')

        if stored_posts is None:
            stored_posts = []

        post_id = request.POST['post_id']

        if post_id not in stored_posts:
            stored_posts.append(post_id)

        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect('/')

