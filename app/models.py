from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class User1(models.Model):
    user1 = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    phone = models.PositiveIntegerField(unique=True, null=True)
    email = models.EmailField(max_length=50, unique=True)
    birthday = models.DateField(blank=True, null=True)
    passport = models.PositiveIntegerField(unique=True, null=True)

    def __str__(self):
        return str(self.last_name)


class Team(models.Model):
    TeamId = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=30, unique=True, null=True)
    rating = models.PositiveSmallIntegerField(null=True, unique=True)
    sport = models.CharField(max_length=30, null=True)
    number_of_players = models.PositiveSmallIntegerField(null=True)
    picture = models.ImageField(upload_to='pics/', null=True, blank=True)

    def __str__(self):
        return str(self.team_name)


class Bet(models.Model):
    user = models.ForeignKey(User1, on_delete=models.CASCADE)
    team = models.ManyToManyField(Team, through="BetTeam")
    date = models.DateField()
    amount = models.FloatField(null=True)

    def __str__(self):
        return str(self.id)


class BetTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
    id = models.AutoField( primary_key=True)

    def __str__(self):
        return str(self.id)