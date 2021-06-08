from django.db.models.fields import CharField
from django.contrib.auth.models import User
from django.db.models.expressions import Value, OuterRef, Exists
from django.db.models import Q

from .models import UserFollows, Review, Ticket


def get_users_viewable_posts(user):
    users_followed_id = UserFollows.objects.filter(user=user.id).values_list('followed_user_id', flat=True)
    users = User.objects.filter(Q(id__in=users_followed_id) | Q(id=user.id))
    tickets = Ticket.objects.filter(user__in=users)
    reviews = Review.objects.filter(Q(ticket__in=tickets) | Q(user=user))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    
    user_review = Review.objects.filter(user=user, ticket=OuterRef('pk'))
    tickets = tickets.annotate(user_has_review=Exists(user_review))
    return tickets, reviews

def get_users_posts(user):
    tickets = Ticket.objects.filter(user=user)
    reviews = Review.objects.filter(user=user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    return tickets, reviews