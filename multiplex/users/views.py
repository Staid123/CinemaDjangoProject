from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib import auth, messages
from carts.models import ProductCart, TicketCart
from orders.models import Order, OrderTicketItem, OrderProductItem
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm



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
                    TicketCart.objects.filter(session_key=session_key).update(user=user)

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
                TicketCart.objects.filter(session_key=session_key).update(user=user)
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
    
    orders = Order.objects.filter(user=request.user).prefetch_related(
                Prefetch(
                    "orderproductitem_set",
                    queryset=OrderProductItem.objects.select_related("product"),
                ),
                Prefetch(
                    "orderticketitem_set",
                    queryset=OrderTicketItem.objects.select_related("ticket"),
                )
            ).order_by("-id")
        

    context = {
        'title': 'Home - Кабинет',
        'form': form,
        'orders': orders,
    }
    return render(request, 'users/profile.html', context)



class UserPasswordChange(PasswordChangeView, LoginRequiredMixin):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
