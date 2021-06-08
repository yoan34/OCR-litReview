from django.contrib import admin
from .models import Ticket, Review, UserFollows


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'image', 'time_created']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'rating', 'user', 'headline', 'time_created']

@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ['user', 'followed_user']