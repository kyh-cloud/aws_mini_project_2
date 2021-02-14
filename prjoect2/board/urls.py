from django.conf.urls import url, include
from django.urls import path

from board import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('loginProcess/', views.loginProcess, name='loginProcess'),
    path('', views.login, name="login"),
    path('home', views.home, name="home"),
    path('board_write', views.board_write, name="board_write"),
    path('board_insert', views.board_insert, name="board_insert"),
    path('board_view', views.board_view, name="board_view"),
    path('board_edit', views.board_edit, name="board_edit"),
    path('board_update', views.board_update, name="board_update"),
    path('board_delete', views.board_delete, name="board_delete"),
    path('comment_insert', views.comment_insert, name="comment_insert"),


    path('ds_querytolist', views.ds_querytolist, name="ds_querytolist"),
    path('ds_orm', views.ds_orm, name="ds_orm"),

    path('markdown2', views.markdown2, name="markdown2"),
]
