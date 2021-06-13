from django.http.response import Http404
from django.shortcuts import render, redirect
from friendslist.models import Friend, Category, Memo
from friendslist.forms import FriendForm, UserCreationForm, CategoryForm, MemoForm
from django.contrib.auth.views import LoginView
from django.contrib import messages

def index(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    first_category = categories.first()
    friends = Friend.objects.filter(user=user)
    context = {
        'friends': friends,
        'categories': categories,
        'first_category': first_category,
    }
    return render(request, 'friendslist/index.html', context)

def create(request):
    if request.method == 'POST':
        form = FriendForm(request.POST)
        if form.is_valid():
            friend = form.save(commit=False)
            friend.user = request.user
            friend.save()
            return redirect('/')

    user = request.user
    categories = Category.objects.filter(user=user)
    first_category = categories.first()
    context = {
        'categories': categories,
        'first_category': first_category,
    }
    return render(request, 'friendslist/create.html', context)

def friend(request, pk):
    if request.method == 'POST':
        friend = Friend.objects.get(pk=pk)
        form = FriendForm(request.POST, instance=friend)
        if form.is_valid():
            friend.save()

    user = request.user
    categories = Category.objects.filter(user=user)            
    friend = Friend.objects.get(pk=pk)
    if friend.birthday is not None:
        friend_birthday = "{0:%Y-%m-%d}".format(friend.birthday)
    else:
        friend_birthday = friend.birthday
    memos = Memo.objects.filter(friend=friend)
    context = {
        'categories': categories,
        'friend': friend,
        'friend_birthday': friend_birthday,
        'memos': memos,
    }
    return render(request, 'friendslist/friend.html', context)

def delete(request, pk):
    try:
        friend = Friend.objects.get(pk=pk)
    except Friend.DoesNotExist:
        raise Http404
    friend.delete()
    return redirect('/')

def category_index(request, pk):
    user = request.user
    categories = Category.objects.filter(user=user)
    current_category = Category.objects.get(pk=pk)
    first_category = categories.first()
    friends = Friend.objects.filter(category=current_category)
    context = {
        'friends': friends,
        'categories': categories,
        'current_category': current_category,
        'first_category': first_category,
    }
    return render(request, 'friendslist/category/index.html', context)

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            user = request.user
            categories = Category.objects.filter(user=user)
            first_category = categories.first()
            return redirect('/category/{}'.format(first_category.id))

    user = request.user
    categories = Category.objects.filter(user=user)
    first_category = categories.first()
    context = {
        'first_category': first_category,
    }
    return render(request, 'friendslist/category/create.html', context)

def category_delete(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise Http404
    category.delete()

    user = request.user
    categories = Category.objects.filter(user=user)
    first_category = categories.first()
    return redirect('/category/{}'.format(first_category.id))

def memo_create(request, pk):
    if request.method == 'POST':
        form = MemoForm(request.POST)
        friend = Friend.objects.get(pk=pk)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.friend = friend
            memo.save()
            return redirect('/{}/'.format(pk))

    context = {}
    return render(request, 'friendslist/memo/create.html', context)

def memo_delete(request, pk, memo_pk):
    try:
        memo = Memo.objects.get(pk=memo_pk)
    except Memo.DoesNotExist:
        raise Http404
    memo.delete()

    return redirect('/{}/'.format(pk))



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
      return redirect('/login/')

  return render(request, 'friendslist/auth.html', context)