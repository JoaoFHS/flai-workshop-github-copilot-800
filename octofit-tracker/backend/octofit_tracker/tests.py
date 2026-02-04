from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.name, "Test User")
        self.assertEqual(self.user.email, "test@example.com")
    
    def test_user_str(self):
        self.assertEqual(str(self.user), "Test User")


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            name="Test Team",
            description="A test team"
        )
    
    def test_team_creation(self):
        self.assertEqual(self.team.name, "Test Team")
        self.assertEqual(self.team.description, "A test team")
    
    def test_team_str(self):
        self.assertEqual(str(self.team), "Test Team")


class ActivityModelTest(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(
            user_id="123456789012345678901234",
            activity_type="Running",
            duration=30,
            calories=300,
            distance=5.0,
            date="2024-01-01T10:00:00Z"
        )
    
    def test_activity_creation(self):
        self.assertEqual(self.activity.activity_type, "Running")
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories, 300)


class LeaderboardModelTest(TestCase):
    def setUp(self):
        self.entry = Leaderboard.objects.create(
            user_id="123456789012345678901234",
            user_name="Test User",
            team_id="123456789012345678901234",
            team_name="Test Team",
            total_activities=10,
            total_calories=3000,
            total_duration=300,
            rank=1
        )
    
    def test_leaderboard_creation(self):
        self.assertEqual(self.entry.user_name, "Test User")
        self.assertEqual(self.entry.rank, 1)


class WorkoutModelTest(TestCase):
    def setUp(self):
        self.workout = Workout.objects.create(
            title="Morning Run",
            description="A quick morning run",
            category="Cardio",
            difficulty="Medium",
            duration=30,
            calories_estimate=300,
            exercises=["Warm-up", "Running", "Cool-down"]
        )
    
    def test_workout_creation(self):
        self.assertEqual(self.workout.title, "Morning Run")
        self.assertEqual(self.workout.category, "Cardio")


class APIRootTest(APITestCase):
    def test_api_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)


class UserAPITest(APITestCase):
    def test_create_user(self):
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TeamAPITest(APITestCase):
    def test_create_team(self):
        data = {
            'name': 'New Team',
            'description': 'A new team for testing'
        }
        response = self.client.post('/api/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ActivityAPITest(APITestCase):
    def test_create_activity(self):
        data = {
            'user_id': '123456789012345678901234',
            'activity_type': 'Cycling',
            'duration': 45,
            'calories': 450,
            'distance': 15.0,
            'date': '2024-01-01T10:00:00Z'
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LeaderboardAPITest(APITestCase):
    def test_get_leaderboard(self):
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    def test_get_workouts(self):
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
