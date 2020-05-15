from django.db import models

# Create your models here.

class GoalStatus(models.Model):
	status_name=models.CharField(max_length=30)

	def __str__(self):
		return status_name


class ScrumyGoal(models.Model):
	goal_id = models.IntegerField(default=0)
	goal_name = models.CharField(max_length=30)
	created_by = models.CharField(max_length=30)
	moved_by = models.CharField(max_length=30)
	owner = models.CharField(max_length=30)
	goal_status = models.ForeignKey(GoalStatus, on_delete=models.PROTECT)
	user = models.ForeignKey(User, related_name="rname", on_delete=models.PROTECT)
	
	def __str__(self):
		return goal_name

class ScrumyHistory(models.Model):
	moved_by = models.CharField(max_length=30)
	created_by = models.CharField(max_length=30)
	moved_from = models.CharField(max_length=30)
	moved_to = models.CharField(max_length=30)
	time_of_action = models.DateTimeField(auto_now=False, auto_now_add=False)
	goal=models.ForeignKey(ScrumyGoal, on_delete=models.PROTECT)

	def __str__(self):
		return created_by
