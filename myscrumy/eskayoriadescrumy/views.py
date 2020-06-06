from django.http import HttpResponse
from django.shortcuts import render
from random import randint
from .models import GoalStatus, ScrumyGoals, User
from .forms import SignupForm, CreateGoalForm, MoveGoalForm
from django.contrib.auth.models import Group

# Create your views here.
def index(request):
    current_user = request.user
    group = getGroup(current_user)
    users_in_developer = Group.objects.get(name='Developer').user_set.all()
    users_in_quality_assurance = Group.objects.get(name='Quality Assurance').user_set.all()
    users_in_admin = Group.objects.get(name='Admin').user_set.all()
    users_in_owner = Group.objects.get(name='Owner').user_set.all()

    form = SignupForm()
    if request.method == 'POST':
      form = SignupForm(request.POST)
      my_group = Group.objects.get(name = 'Developer')
      
      if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        my_group.user_set.add(user)
        return HttpResponse('Your account has been created successfully')

    else:
      form = SignupForm()

    return render(request, 'eskayoriadescrumy/index.html', {'current_user':request.user, 'group':group, 'form':form})


def move_goal(request, goal_id):
    myId = goal_id
    current_user = request.user
    group = getGroup(current_user)
    users_in_developer = Group.objects.get(name='Developer').user_set.all()
    users_in_quality_assurance = Group.objects.get(name='Quality Assurance').user_set.all()
    users_in_admin = Group.objects.get(name='Admin').user_set.all()
    users_in_owner = Group.objects.get(name='Owner').user_set.all()
    
    try:
      goal = ScrumyGoals.objects.get(goal_id=myId)
      move_goal_form = MoveGoalForm()

      done_goal = GoalStatus.objects.get(status_name__contains='Done')
      verify_goal = GoalStatus.objects.get(status_name__contains='Verify')
      weekly_goal = GoalStatus.objects.get(status_name__contains='Weekly')

      if request.method == 'POST':
        move_goal_form = MoveGoalForm(request.POST)

        if move_goal_form.is_valid():
          current_user = request.user
          print(current_user)
          if move_goal_form.cleaned_data["goal_status"] is not None:
            if current_user in users_in_developer and goal.user == current_user:
              if move_goal_form.cleaned_data["goal_status"] != done_goal:
                goal.goal_status = move_goal_form.cleaned_data["goal_status"]
                goal.save()
                
            elif current_user in users_in_quality_assurance:
              if goal.user == current_user:
                if move_goal_form.cleaned_data["goal_status"] != weekly_goal:
                  goal.goal_status = move_goal_form.cleaned_data["goal_status"]
                  goal.save()

              elif goal.user in users_in_quality_assurance is None: 
                if goal.goal_status == verify_goal:
                  if move_goal_form.cleaned_data["goal_status"] is done_goal:
                    goal.goal_status = move_goal_form.cleaned_data.get["goal_status"]
                    goal.save()

            elif current_user in users_in_admin:
              goal.goal_status = move_goal_form.cleaned_data["goal_status"]
              goal.save()

            elif current_user in users_in_owner:
              if goal.user == current_user:
                goal.goal_status = move_goal_form.cleaned_data["goal_status"]
                goal.save()

          else:
            return HttpResponse("{current_user.username} cannot move {goal.goal.name} to {goal.goal_status}" )

      else:
        move_goal_form = MoveGoalForm()

    except ScrumyGoals.DoesNotExist:
       return render(request, 'eskayoriadescrumy/exception.html', 
                     {'error':'A record with that goal id does not exist'})
    return render(request, 'eskayoriadescrumy/movegoal.html', {'current_user':request.user, 'group':group, 'form':move_goal_form})


def add_goal(request):
    current_user = request.user
    group = getGroup(current_user)
    scrumy_goal_form = CreateGoalForm()

    if request.method == 'POST':
      scrumy_goal_form = CreateGoalForm(request.POST)
      if scrumy_goal_form.is_valid():
        users_in_developer = Group.objects.get(name='Developer').user_set.all()
        users_in_quality_assurance = Group.objects.get(name='Quality Assurance').user_set.all()
        users_in_admin = Group.objects.get(name='Admin').user_set.all()
        users_in_owner = Group.objects.get(name='Owner').user_set.all()
        weekly_goal = GoalStatus.objects.get(status_name__contains='Weekly')

        if scrumy_goal_form.cleaned_data.get('goal_name') is not None:
          if current_user in users_in_developer or current_user in users_in_quality_assurance or current_user in users_in_owner:
            myId = randint(1000, 9999)
            try:
              while ScrumyGoals.objects.get(goal_id = myId) is not None:
                myId = randint(1000, 9999)
            except ScrumyGoals.DoesNotExist:
              goal = scrumy_goal_form.save(commit=False)
              goal.goal_name = scrumy_goal_form.cleaned_data["goal_name"]
              goal.goal_status = weekly_goal
              goal.user = current_user
              goal.goal_id = myId
              goal.save()
              
          else:
            scrumy_goal_form = CreateGoalForm()
    else:
      scrumy_goal_form = CreateGoalForm()
    return render(request, 'eskayoriadescrumy/addgoal.html', {'current_user':request.user, 'group':group, 'form':scrumy_goal_form})
    

def home(request):
    weekly_goals = None
    daily_goals = None
    verify_goals = None
    done_goals = None
    scrumy_goals = None
    group = getGroup(request.user)

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
      'current_user' : request.user,
      'group' : group,
      'users' : User.objects.all(),
      'weekly_goals' : weekly_goals,
      'daily_goals' : daily_goals,
      'verify_goals' : verify_goals,
      'done_goals' : done_goals,
      'scrumy_goals' : scrumy_goals
    }

    return render(request, 'eskayoriadescrumy/home.html', context)

def getGroup(current_user):
    users_in_developer = Group.objects.get(name='Developer').user_set.all()
    users_in_quality_assurance = Group.objects.get(name='Quality Assurance').user_set.all()
    users_in_admin = Group.objects.get(name='Admin').user_set.all()
    users_in_owner = Group.objects.get(name='Owner').user_set.all()
    group = None

    if current_user in users_in_developer:
      group = 'Developer'
    elif current_user in users_in_quality_assurance:
      group = 'Quality Assurance'
    elif current_user in users_in_admin:
      group = 'Admin'
    else:
      group = 'Owner'

    return group
