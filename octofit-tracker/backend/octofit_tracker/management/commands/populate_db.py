from django.core.management.base import BaseCommand
from django.utils import timezone
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        
        # Delete all existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared'))
        
        # Create teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Assemble the strongest heroes from the Marvel Universe',
            created_at=timezone.now()
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Unite the legendary heroes from DC Comics',
            created_at=timezone.now()
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created teams: {team_marvel.name}, {team_dc.name}'))
        
        # Create users (superheroes)
        self.stdout.write('Creating superhero users...')
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com', 'password': 'iamironman'},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com', 'password': 'avenger1'},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com', 'password': 'asgardian'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com', 'password': 'redledger'},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com', 'password': 'smash123'},
            {'name': 'Spider-Man', 'email': 'peter.parker@marvel.com', 'password': 'webslinger'},
        ]
        
        dc_heroes = [
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com', 'password': 'darknight'},
            {'name': 'Superman', 'email': 'clark.kent@dc.com', 'password': 'krypton'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com', 'password': 'amazonian'},
            {'name': 'The Flash', 'email': 'barry.allen@dc.com', 'password': 'speedforce'},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com', 'password': 'atlantis'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@dc.com', 'password': 'willpower'},
        ]
        
        marvel_users = []
        for hero in marvel_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                password=hero['password'],
                team_id=str(team_marvel._id),
                created_at=timezone.now()
            )
            marvel_users.append(user)
        
        dc_users = []
        for hero in dc_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                password=hero['password'],
                team_id=str(team_dc._id),
                created_at=timezone.now()
            )
            dc_users.append(user)
        
        all_users = marvel_users + dc_users
        self.stdout.write(self.style.SUCCESS(f'Created {len(all_users)} superhero users'))
        
        # Create activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'Combat Training']
        activities_count = 0
        
        for user in all_users:
            # Create 5-10 activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                calories = duration * random.randint(5, 15)
                distance = round(random.uniform(1, 20), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                date = timezone.now() - timedelta(days=random.randint(0, 30))
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    calories=calories,
                    distance=distance,
                    date=date,
                    notes=f'{activity_type} session by {user.name}'
                )
                activities_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {activities_count} activities'))
        
        # Create leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        leaderboard_entries = []
        
        for user in all_users:
            user_activities = Activity.objects.filter(user_id=str(user._id))
            total_activities = user_activities.count()
            total_calories = sum(activity.calories for activity in user_activities)
            total_duration = sum(activity.duration for activity in user_activities)
            
            team = team_marvel if user.team_id == str(team_marvel._id) else team_dc
            
            leaderboard_entry = Leaderboard.objects.create(
                user_id=str(user._id),
                user_name=user.name,
                team_id=user.team_id,
                team_name=team.name,
                total_activities=total_activities,
                total_calories=total_calories,
                total_duration=total_duration,
                rank=0
            )
            leaderboard_entries.append((leaderboard_entry, total_calories))
        
        # Assign ranks based on total calories
        leaderboard_entries.sort(key=lambda x: x[1], reverse=True)
        for rank, (entry, _) in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard_entries)} leaderboard entries'))
        
        # Create workouts
        self.stdout.write('Creating workout suggestions...')
        workouts = [
            {
                'title': 'Superhero Strength Training',
                'description': 'Build superhuman strength with this intense workout',
                'category': 'Strength',
                'difficulty': 'Advanced',
                'duration': 60,
                'calories_estimate': 450,
                'exercises': [
                    {'name': 'Bench Press', 'sets': 4, 'reps': 10},
                    {'name': 'Deadlifts', 'sets': 4, 'reps': 8},
                    {'name': 'Squats', 'sets': 4, 'reps': 12},
                    {'name': 'Pull-ups', 'sets': 3, 'reps': 15}
                ]
            },
            {
                'title': 'Speed Force Cardio',
                'description': 'Boost your speed and endurance like The Flash',
                'category': 'Cardio',
                'difficulty': 'Intermediate',
                'duration': 45,
                'calories_estimate': 500,
                'exercises': [
                    {'name': 'Sprint Intervals', 'duration': 15, 'intensity': 'high'},
                    {'name': 'High Knees', 'duration': 10, 'intensity': 'medium'},
                    {'name': 'Burpees', 'sets': 3, 'reps': 15},
                    {'name': 'Jump Rope', 'duration': 10, 'intensity': 'high'}
                ]
            },
            {
                'title': 'Warrior Flexibility',
                'description': 'Improve flexibility and balance like an Amazonian warrior',
                'category': 'Flexibility',
                'difficulty': 'Beginner',
                'duration': 30,
                'calories_estimate': 150,
                'exercises': [
                    {'name': 'Yoga Flow', 'duration': 10},
                    {'name': 'Warrior Poses', 'duration': 10},
                    {'name': 'Stretching', 'duration': 10}
                ]
            },
            {
                'title': 'Combat Ready Training',
                'description': 'Master combat skills with this mixed martial arts workout',
                'category': 'Mixed',
                'difficulty': 'Advanced',
                'duration': 75,
                'calories_estimate': 600,
                'exercises': [
                    {'name': 'Shadow Boxing', 'duration': 15},
                    {'name': 'Kickboxing Drills', 'duration': 20},
                    {'name': 'Core Exercises', 'sets': 3, 'reps': 20},
                    {'name': 'Agility Drills', 'duration': 20}
                ]
            },
            {
                'title': 'Asgardian Hammer Workout',
                'description': 'Build god-like power with this hammer-inspired routine',
                'category': 'Strength',
                'difficulty': 'Advanced',
                'duration': 50,
                'calories_estimate': 400,
                'exercises': [
                    {'name': 'Sledgehammer Slams', 'sets': 4, 'reps': 15},
                    {'name': 'Farmers Walk', 'duration': 10},
                    {'name': 'Battle Ropes', 'sets': 4, 'duration': 30},
                    {'name': 'Medicine Ball Throws', 'sets': 3, 'reps': 12}
                ]
            },
            {
                'title': 'Web-Slinger Agility',
                'description': 'Develop Spider-Man level agility and reflexes',
                'category': 'Agility',
                'difficulty': 'Intermediate',
                'duration': 40,
                'calories_estimate': 350,
                'exercises': [
                    {'name': 'Plyometric Jumps', 'sets': 3, 'reps': 15},
                    {'name': 'Ladder Drills', 'duration': 10},
                    {'name': 'Box Jumps', 'sets': 3, 'reps': 12},
                    {'name': 'Obstacle Course', 'duration': 15}
                ]
            }
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts)} workout suggestions'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Teams: {Team.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {Activity.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard Entries: {Leaderboard.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {Workout.objects.count()}'))
