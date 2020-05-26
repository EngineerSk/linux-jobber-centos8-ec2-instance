from django.urls import path, include
from . import views

app_name = 'eskayoriadescrumy'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('movegoal/<int:goal_id>', views.move_goal),
    path('addgoal', views.add_goal),
    path('home', views.home)
]
