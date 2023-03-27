from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

def home(request):
	context={
	    'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
			return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
			return False


	

def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})


@login_required
def favorite_add(request,id):
	post = get_object_or_404(Post, id=id)
	if post.favorite.filter(id=request.user.id).exists():
		post.favorite.remove(request.user)
		def get_absolute_url(self):
			return reverse('post-detail', kwargs={'pk': self.pk})
	else:
		post.favorite.add(request.user)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def favorite_list(request):
	new = Post.objects.filter(favorite=request.user)
	return render(request, 'blog/favorites.html', {'new': new})