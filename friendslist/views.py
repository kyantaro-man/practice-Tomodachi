from django.http.response import Http404
from django.shortcuts import render, redirect
from friendslist.models import Friend
from friendslist.forms import FriendForm, UserCreationForm
from django.contrib.auth.views import LoginView

def index(request):
    friends = Friend.objects.all()
    context = {
        'friends': friends,
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

class Login(LoginView):
    template_name = 'friendslist/auth.html'

def signup(request):
  context = {}
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      # user.is_active = False
      user.save()
      return redirect('/')
  return render(request, 'friendslist/auth.html', context)