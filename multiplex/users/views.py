from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib import auth, messages
from carts.models import ProductCart
from multiplex import settings
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from django.contrib.auth.views import PasswordChangeView


def login(request):
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, 'Вы вошли в аккаунт')

                if session_key:
                    ProductCart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('users:logout'):
                    return redirect(request.POST.get('next'))
                return redirect('cinema:home')
    else:
        form = LoginUserForm()

    return render(request, 'users/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = RegisterUserForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            if session_key:
                ProductCart.objects.filter(session_key=session_key).update(user=user)
            return redirect('cinema:home')
    else:
        form = RegisterUserForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUserForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileUserForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})



class UserPasswordChange(PasswordChangeView, LoginRequiredMixin):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"