from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View, DetailView
from .models import *
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def main(request):
    user = request.user
    par = {
        'header': 'Main page',
        'user': user

    }
    return render(request, 'MainPage.html', context=par)


class TeamForm(forms.ModelForm):
    class Meta(object):
        model = Team
        fields = ['team_name', 'rating', 'sport', 'number_of_players', 'picture', 'TeamId']

    def save(self):
        team = Team()
        team.team_name = self.cleaned_data.get('name')
        team.rating = self.cleaned_data.get('price')
        team.sport = self.cleaned_data.get('type')
        team.number_of_players = self.cleaned_data.get('quantity')
        picture = self.cleaned_data.get('picture')
        team.picture = picture
        team.save()


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=5, label='Логин')
    password = forms.CharField(min_length=6, widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(min_length=6, widget=forms.PasswordInput, label='Повторите ввод')
    last_name = forms.CharField(label='Фамилия')
    first_name = forms.CharField(label='Имя')
    email = forms.EmailField(label='Email')


def registration_1(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        is_val = form.is_valid()
        data = form.cleaned_data
        if data['password'] != data['password2']:
            is_val = False
            form.add_error('password2', ['Пароли должны совпадать'])
        if User.objects.filter(username=data['username']).exists():
            form.add_error('username', ['Такой логин уже занят'])
            is_val = False
        if is_val:
            new_user = User.objects.create_user(data['username'], data['email'], data['password'])
            print(new_user)
            user1 = User1()
            user1.user1 = new_user
            user1.email = data['email']
            user1.last_name = data['last_name']
            user1.first_name = data['first_name']
            user1.save()
            return HttpResponseRedirect('/login1')
        else:
            form = RegistrationForm()
    return render(request, 'registration_1.html', {'form': form})


def registration_form(request):
    errors = {}
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        if not last_name:
            errors['last_name'] = 'Введите Фамилию'

        first_name = request.POST.get('first_name')
        if not first_name:
            errors['first_name'] = 'Введите имя'

        email = request.POST.get('Email')
        if not email:
            errors['Email'] = 'Введите Email'

        username = request.POST.get('username')
        if not username:
            errors['username'] = 'Введите логин'
        elif len(username) < 8:
            errors['username'] = 'Логин должен превышать 5 символов'
        if User.objects.filter(username=username).exists():
            errors['username'] = 'Данный логин занят'

        password = request.POST.get('password')
        if not password:
            errors['password'] = 'Введите пароль'
        elif len(password) < 8:
            errors['password'] = 'Длина пароля должна превышать 6 символов'
        password_repeat = request.POST.get('password2')
        if password != password_repeat:
            errors['password_repeat'] = 'Пароли должны совпадать'
        print(username, password, "1")

        if not errors:
            new_user = User.objects.create_user(username, email, password)
            print(new_user)
            user1 = User1()
            user1.user1 = new_user
            user1.email = email
            user1.last_name = last_name
            user1.first_name = first_name
            user1.save()
            return HttpResponseRedirect('/login2')
        else:
            context = {'errors': errors, 'username': username, 'email': email, 'last_name': last_name,
                       'first_name': first_name, 'password': password, 'password_repeat': password_repeat}
            return render(request, 'registration.html', context)
    return render(request, 'registration.html', {'errors': errors})


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


def log_in(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            errors['username'] = 'Введите логин'
        elif len(username) < 5:
            errors['username'] = 'Слишком короткий логин. Минимальная длина-5 знаков'

        password = request.POST.get('password')
        if not password:
            errors['password'] = 'Введите пароль'
        elif len(password) < 8:
            errors['password'] = 'Слишком короткий пароль. Минимальная длина-8 знаков'

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is None and 'username' not in errors.keys() and 'password' not in errors.keys():
            errors['login'] = 'Логин или пароль введены неверно'

        if not errors:
            login(request, user)
            return HttpResponseRedirect('/items')
        else:
            context = {'errors': errors}
            return render(request, 'UserLogin.html', context)
    return render(request, 'UserLogin.html', {'errors':errors})


def log_in1(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        data = form.cleaned_data

        if form.is_valid():
            user = authenticate(request, username=data['username'], password=data['password'])
            print(len(data['username']), len(data['password']))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/items')
            else:
                form.add_error('username', ['Неверный логин или пароль'])
    else:
        form = LoginForm()
    return render(request, 'UserLogin_1.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'MainPage.html')


@login_required(login_url='/login2')
def logged_in(request):
    return render(request, 'items.html')


def logged_in_view(request):
    if request.user.is_authenticated:
        return render(request, 'items.html')
    else:
        return HttpResponseRedirect('/login1')


def new_item(request):
    errors = {}
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        if not team_name:
            errors['team_name'] = 'Введите Название команды'
        if Team.objects.filter(team_name=team_name).exists():
            errors['team_name'] = 'Данная команда уже существует'

        rating = request.POST.get('rating')
        if not rating:
            errors['rating'] = 'Введите рейтинг'
        if Team.objects.filter(rating=rating).exists():
            errors['rating'] = 'Команда с таким значением рейтинга уже существует'

        sport = request.POST.get('sport')
        if not sport:
            errors['sport'] = 'Введите вид спорта'

        number_of_players = request.POST.get('number_of_players')
        if not number_of_players:
            errors['number_of_players'] = 'Введите кол-во участников команды'

        picture = request.FILES.get('picture')
        if not picture:
            errors['picture'] = 'Загрузите фото'
        if not errors:
            team = Team(team_name=team_name, rating=rating, sport=sport, number_of_players=number_of_players,
                        picture=picture)
            team.save()
            TeamId = team.TeamId
            return HttpResponseRedirect('/item/' + str(TeamId))
        else:
            context = {'errors': errors, 'team_name': team_name, 'rating': rating, 'sport': sport,
                       'number_of_players': number_of_players, 'picture': picture}

    return render(request, 'new_item.html', locals())


class ItemsView(View):
    def get(self, request):
        dict_users = {}
        teams = Team.objects.all()
        teams1 = Team.objects.all()
        form = TeamForm()
        paginator = Paginator(teams, 5)
        page = request.GET.get('page')
        try:
            teams = paginator.page(page)
        except PageNotAnInteger:
            teams = paginator.page(1)
        except EmptyPage:
            teams = paginator.page(paginator.num_pages)
        return render(request, 'items.html', context={'teams': teams, 'users': dict_users, 'form': form,
                                                      'teams1': teams1})


class TeamObject(DetailView):
    model = Team
    context_object_name = 'TeamObject'
    template_name = 'obj.html'


def new_bet(request, team):
    errors = {}
    if request.method == 'POST':
        bet = Bet()
        uid = request.user.id
        user = User1.objects.get(id=uid)
        bet.user = user
        bet_id = bet.id
        team1 = Team.objects.get(TeamId=int(team))
        amount = request.POST.get('amount')
        date = datetime.today()
        bet.date = date
        bet.amount = amount
        if not errors:
            bet.save()
            bet2 = BetTeam()
            bet2.team_id = team1.TeamId
            bet2.id = bet_id
            bet2.bet_id = bet.id
            bet2.user_id = uid
            bet2.save()
            return HttpResponseRedirect('/item/'+str(team1.TeamId)+'/')
        else:
            context = {'errors': errors, 'amount': amount}

    return render(request, 'new_bet.html', locals())


def bets_users(request, team):
    bets = []
    team1 = Team.objects.get(TeamId=int(team))
    users = User1.objects.all()
    bet3 = []
    bet = BetTeam.objects.filter(team_id=team1.TeamId).all()
    for b in bet:
        bet1 = Bet.objects.filter(id=b.bet_id).all()
        if len(bet1) != 0:
            bet3.append(b.id)
    for i in bet3:
        bets.append(Bet.objects.get(id=i))
    return render(request, 'bets.html', context={"bets": bets, "users": users, 'team': team})
