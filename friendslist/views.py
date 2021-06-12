from django.http.response import Http404
from django.shortcuts import render, redirect
from friendslist.models import Friend, Category
from friendslist.forms import FriendForm, UserCreationForm, CategoryForm
from django.contrib.auth.views import LoginView
from django.contrib import messages

def index(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    friends = Friend.objects.all()
    context = {
        'friends': friends,
        'categories': categories,
    }
    return render(request, 'friendslist/index.html', context)

def create(request):
    if request.method == 'POST':
        form = FriendForm(request.POST)
        if form.is_valid():
            friend = form.save(commit=False)
            friend.save()
            return redirect('/')
    return render(request, 'friendslist/create.html')

def friend(request, pk):
    if request.method == 'POST':
        friend = Friend.objects.get(pk=pk)
        form = FriendForm(request.POST, instance=friend)
        if form.is_valid():
            friend.save()
            
    friend = Friend.objects.get(pk=pk)
    context = {
        'friend': friend
    }
    return render(request, 'friendslist/friend.html', context)

def delete(request, pk):
    try:
        friend = Friend.objects.get(pk=pk)
    except Friend.DoesNotExist:
        raise Http404
    friend.delete()
    return redirect('/')

def category_index(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    context = {
        'categories': categories,
    }
    return render(request, 'friendslist/category/index.html', context)

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('/category/')
    return render(request, 'friendslist/category/create.html')

def category_delete(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise Http404
    category.delete()
    return redirect('/category/')

class Login(LoginView):
    template_name = 'friendslist/auth.html'

    def form_valid(self, form):
        messages.success(self.request, 'ログイン完了！！！')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'エラーあり')
        return super().form_invalid(form)

def signup(request):
  context = {}
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      # user.is_active = False
      user.save()
      messages.success(request, '登録完了！！！')
      return redirect('/')
  return render(request, 'friendslist/auth.html', context)