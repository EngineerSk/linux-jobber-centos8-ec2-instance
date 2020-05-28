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
    weekly_goals = None
    daily_goals = None
    verify_goals = None
    done_goals = None
    scrumy_goals = None

    try:
       status = GoalStatus.objects.get(status_name = "Weekly Goal")
       weekly_goals = status.scrumygoals_set.all()
       status = GoalStatus.objects.get(status_name = "Daily Goal")
       daily_goals = status.scrumygoals_set.all()
       status = GoalStatus.objects.get(status_name = "Verify Goal")
       verify_goals = status.scrumygoals_set.all()
       status = GoalStatus.objects.get(status_name = "Done Goal")
       done_goals = status.scrumygoals_set.all()
       scrumy_goals = ScrumyGoals.objects.all()

    except ScrumyGoals.DoesNotExist:
       return HttpResponse()

    context = {
      'users' : User.objects.all(),
      'weekly_goals' : weekly_goals,
      'daily_goals' : daily_goals,
      'verify_goals' : verify_goals,
      'done_goals' : done_goals,
      'scrumy_goals' : scrumy_goals
    }

    return render(request, 'eskayoriadescrumy/home.html', context)
