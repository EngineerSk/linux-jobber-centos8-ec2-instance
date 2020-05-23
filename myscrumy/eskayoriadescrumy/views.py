from django.http import HttpResponse
from django.shortcuts import render
from random import randint
from .models import GoalStatus, ScrumyGoals, User

# Create your views here.
def index(request):
    goal = ScrumyGoals.objects.filter(goal_name__contains='Lear')
    return HttpResponse(goal)


def move_goal(request, goal_id):
    myId = goal_id
    try:
       obj =  ScrumyGoals.objects.get(goal_id=myId)
    except ScrumyGoals.DoesNotExist:
       return render(request, 'eskayoriadescrumy/exception.html', 
                     {'error':'A record with that goal id does not exist'})
    return HttpResponse(obj.goal_name)


def add_goal(request):
    myGoalId = randint(1000, 9999)

    try:
       while ScrumyGoals.objects.get(goal_id = myGoalId) is not None:
          myGoalId = randint(1000, 9999)  
    except ScrumyGoals.DoesNotExist:
       goal = ScrumyGoals.objects.create(goal_id = myGoalId, 
       goal_name = 'Keep Learning Django', created_by = 'Louis', 
       moved_by = 'Louis', owner = 'Louis', 
       goal_status = GoalStatus.objects.get(status_name = 'Weekly Goal'), 
       user = User.objects.get(username = 'Louis Oma'))
       goal.save()
     
    return HttpResponse()    
    

def home(request):
    goal = None

    try:
       goal = ScrumyGoals.objects.get(goal_name = "Learn Django")

    except ScrumyGoals.DoesNotExist:
       return HttpResponse()

    context = {
      'goal_name':goal.goal_name,
      'goal_id':goal.goal_id,
      'user':goal.user,
      'goal_status':goal.goal_status
    }

    return render(request, 'eskayoriadescrumy/home.html', context)
