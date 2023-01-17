from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView,DetailView,FormView
from django.views.generic.edit import DeleteView,UpdateView,CreateView
from .models import Article
from django.urls import reverse_lazy, reverse 
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from .forms import CommentForm
from django.views.generic.detail import SingleObjectMixin
from django.views import View

class ArticleListView( LoginRequiredMixin,ListView):
    model = Article
    template_name = "article_list.html"
    
class ArticleDeleteView( LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url= reverse_lazy("article_list")
    template_name= "article_delete.html"
    
    def test_func(self):
        return self.get_object().author == self.request.user
    
class ArticleUpdateView( LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields=(
        "title",
        "body",
    )
    template_name= "article_edit.html"
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
class CommentGet(DetailView):
    model = Article
    template_name= "article_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
    
class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        return super().post(request,*args,**kwargs)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk":article.pk})


class ArticleDetailView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        view = CommentGet.as_view()
        return view(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        view = CommentPost.as_view()
        return view(request,*args,**kwargs)
    
class ArticleCreateView(LoginRequiredMixin,CreateView):
    model = Article
    fields = (
        "title",
        "body",
        #"author",
    )
    template_name = "article_create.html"
    
    # What this does is to remove the author field from the article and set it automatically...
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    