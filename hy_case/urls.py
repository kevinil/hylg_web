from django.urls import path
from django.views.generic import  RedirectView

from . import views

urlpatterns = [
    # ex: /
    #path('', views.redirect_view, name='redirect'),
    path('', RedirectView.as_view(url='index/')),

    path('index/', views.index, name='index'),

    path('login/', views.login, name='login'),

    path('logout/', views.logout, name='logout'),

    path('case/', views.case, name='case'),

    path('data/', views.data, name='data'),

    path('report/', views.report, name='report'),

    path('clue/', views.clue, name='clue'),

    path('user/', views.user, name='user'),

    # request

    path('reportRequest/', views.reportRequest, name='reportRequest'),

]


