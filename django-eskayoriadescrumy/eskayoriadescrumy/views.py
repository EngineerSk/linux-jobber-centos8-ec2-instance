from django.http import HttpResponse
from django.shortcuts import render
from random import randint
from .models import GoalStatus, ScrumyGoals, User
from .forms import SignupForm, CreateGoalForm
from django.contrib.auth.models import Group

# Create your views here.
def index(request):
    form = SignupForm()
    if request.method == 'POST':
      form = SignupForm(request.POST)
      my_group = Group.objects.get(name = 'Developer')
      
      if form.is_valid:
        my_group.user_set.add(form.save())
        return HttpResponse('Your account has been created successfully')
    else:
      form = SignupForm()

    return render(request, 'eskayoriadescrumy/index.html', {'form':form})


def move_goal(request, goal_id):
    myId = goal_id
    try:
       obj =  ScrumyGoals.objects.get(goal_id=myId)
    except ScrumyGoals.DoesNotExist:
       return render(request, 'eskayoriadescrumy/exception.html', 
                     {'error':'A record with that goal id does not exist'})
    return HttpResponse(obj.goal_name)


def add_goal(request):
    scrumy_goal_form = CreateGoalForm()
    if request.method == 'POST':
      scrumy_goal_form = CreateGoalForm(request.POST)
      scrumy_goal_form.save()
    else:
      scrumy_goal_form = CreateGoalForm()
    return render(request, 'eskayoriadescrumy/addgoal.html', {'form':scrumy_goal_form})
    

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
