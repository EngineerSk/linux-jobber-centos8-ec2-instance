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
