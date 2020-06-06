from django.forms import ModelForm
from .models import ScrumyGoals, User

class SignupForm(ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'username', 'password']


class CreateGoalForm(ModelForm):
	class Meta:
		model = ScrumyGoals
		fields = ['goal_name', 'user']


class MoveGoalForm(ModelForm):
	class Meta:
		model = ScrumyGoals
		fields = ['goal_status']