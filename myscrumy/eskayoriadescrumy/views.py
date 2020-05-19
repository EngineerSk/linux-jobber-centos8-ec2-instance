from django.http import HttpResponse
from django.shortcuts import render
from .models import ScrumyGoals

# Create your views here.
def index(request):
    goal = ScrumyGoals.objects.filter(goal_name__contains='Lear')
    return HttpResponse(goal)

def move_goal(request, goal_id):
    myId = goal_id
    goal =  ScrumyGoals.objects.get(goal_id=myId)
    return HttpResponse(goal)


def add_goal(request):
    myGoalId=randInt(1000, 9999)
    while(ScrumyGoals.objects.get(goal_id=myGoalId) is not None):
        myGoalId=randInt(1000, 9999)

    goal = ScrumyGoals.objects.create(goal_id=myGoalId, 
    goal_name='Keep Learning Django', created_by='Louis', moved_by='Louis',
    owner='Louis', goal_status=GoalStatus.objects.get(status_name='Weekly Goal'), 
    user=User.objects.create(username='Louis Oma'))


def home(request):
    goals = ScrumyGoals.objects.all(goal_name='Keep Learning Django')
    return HttpResponse(', '.join[each_goal.goal_name for goals])
