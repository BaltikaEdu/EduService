from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from Examinatus.forms import RegisterUserForm, LoginUserForm
from Examinatus.models import Test, Question


# Create your views here.
class RegisterUser(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy('profile/')
    template_name = 'register.html'
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context


class LoginUser(SuccessMessageMixin, LoginView):

    form_class = LoginUserForm
    template_name = 'login.html'
    next_page = '/profile/'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context


def main(request):
    return HttpResponse('Главная страница')


@login_required(login_url='/login/')
def profile(request):
    return HttpResponse(request.user.username)


def logout_user(request):
    logout(request)
    return redirect('/login/')


def create_test(request):
    if request.method == "GET":
        return render(request, 'create_test.html')
    if request.method == 'POST':
        test = Test(
            name=request.POST.get('name'),
            creator=User.objects.get(username=request.user.username)
        )
        test.save()
        return HttpResponse('Тест создан')


def test(request, id=0):
    if id == 0 or not Test.objects.filter(id=id).exists():
        return HttpResponseRedirect('/')
    test = Test.objects.get(id=id)
    questions = Question.objects.filter(test=test)
    return render(request, 'test.html', context={'test': test, 'questions': questions})


def add_question(request, id=0):
    if id == 0 or not Test.objects.filter(id=id).exists():
        return HttpResponseRedirect('/')
    test = Test.objects.get(id=id)
    if test.creator.id != request.user.id:
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        return render(request, 'add_question.html')
    if request.method == 'POST':
        question = Question(
            text=request.POST.get('text'),
            answer=request.POST.get('answer'),
            test=test
        )
        question.save()
        return HttpResponseRedirect(f'/test/{id}')
