from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from djongo import models

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'
        db_table = 'users'

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        app_label = 'octofit_tracker'
        db_table = 'teams'

class Activity(models.Model):
    user = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=50)
    duration = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'
        db_table = 'activities'

class Leaderboard(models.Model):
    user = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'
        db_table = 'leaderboard'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'
        db_table = 'workouts'

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear collections
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Users
        users = [
            User(email='ironman@marvel.com', name='Iron Man', team='Marvel'),
            User(email='captain@marvel.com', name='Captain America', team='Marvel'),
            User(email='spiderman@marvel.com', name='Spider-Man', team='Marvel'),
            User(email='batman@dc.com', name='Batman', team='DC'),
            User(email='superman@dc.com', name='Superman', team='DC'),
            User(email='wonderwoman@dc.com', name='Wonder Woman', team='DC'),
        ]
        User.objects.bulk_create(users)

        # Activities
        Activity.objects.bulk_create([
            Activity(user='Iron Man', activity_type='run', duration=30),
            Activity(user='Captain America', activity_type='cycle', duration=45),
            Activity(user='Spider-Man', activity_type='swim', duration=25),
            Activity(user='Batman', activity_type='run', duration=40),
            Activity(user='Superman', activity_type='fly', duration=60),
            Activity(user='Wonder Woman', activity_type='row', duration=35),
        ])

        # Leaderboard
        Leaderboard.objects.bulk_create([
            Leaderboard(user='Iron Man', points=100),
            Leaderboard(user='Captain America', points=90),
            Leaderboard(user='Spider-Man', points=80),
            Leaderboard(user='Batman', points=110),
            Leaderboard(user='Superman', points=120),
            Leaderboard(user='Wonder Woman', points=95),
        ])

        # Workouts
        Workout.objects.bulk_create([
            Workout(name='Morning Cardio', difficulty='Easy'),
            Workout(name='Strength Training', difficulty='Medium'),
            Workout(name='HIIT', difficulty='Hard'),
        ])

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
