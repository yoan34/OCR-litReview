from django.urls import path
from . import views


app_name = 'ticket'

urlpatterns = [
    path('flux/', views.flux, name='flux'),
    path('posts/', views.posts, name='posts'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('create_ticket_review/', views.create_ticket_review, name='create_ticket_review'),
    path('create_review/<int:id>/', views.create_review, name='create_review'),
    path('edit_ticket/<int:id>/', views.edit_ticket, name='edit_ticket'),
    path('edit_review/<int:id>/', views.edit_review, name='edit_review'),
]
