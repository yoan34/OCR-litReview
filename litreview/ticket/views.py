import itertools
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User

from .forms import ReviewForm, TicketForm, UserFollowsForm
from .models import Review, UserFollows, Ticket

from .tools import get_users_viewable_posts, get_users_posts


@login_required
def posts(request):
    tickets, reviews = get_users_posts(request.user)
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        if content_type == 'ticket':
            Ticket.objects.get(id=request.POST.get('id')).delete()
        else:
            Review.objects.get(id=request.POST.get('id')).delete()

    posts = sorted(itertools.chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
    return render(request, 'ticket/flux.html', {'section': 'posts',
                                                'posts': posts})


@login_required
def subscriptions(request):
    name = None
    users = User.objects.all().exclude(id=request.user.id)
    users_followed_id = UserFollows.objects.filter(user=request.user.id).values_list('followed_user_id', flat=True)
    followers_id = UserFollows.objects.filter(followed_user=request.user.id).values_list('user_id', flat=True)

    users_followed = User.objects.filter(id__in=users_followed_id)
    followers = User.objects.filter(id__in=followers_id)

    if request.method == 'POST':
        if len(request.POST) == 3:
            # desabonnement
            search_form = UserFollowsForm()
            followed_user = User.objects.filter(username=request.POST.get('username'))
            followed_user_id = followed_user.values_list("id", flat=True)[0]
            relation = UserFollows.objects.filter(user=request.user.id, followed_user=followed_user_id)
            relation.delete()
        else:
            # recherche utilisateur
            search_form = UserFollowsForm(request.POST)
            if search_form.is_valid():
                name = search_form.cleaned_data['username']
                user = users.filter(username=name)
                if user.exists():
                    relation = UserFollows.objects.filter(user=request.user, followed_user=user[0])
                    if relation.exists():
                        messages.error(request, f"{user.values_list('username', flat=True)[0]} est \
                            déjà dans votre liste d'amis.")
                    else:
                        relation = UserFollows(user=request.user, followed_user=user[0])
                        relation.save()
                        messages.success(request, f"{user.values_list('username', flat=True)[0]} à \
                            été ajouté avec succès.")
                else:
                    messages.error(request, "Ce nom d'utilisateur n'existe pas.")
    else:
        search_form = UserFollowsForm()
    return render(request, 'subscription.html', {'section': 'subscription',
                                                 'search_form': search_form,
                                                 'users_followed': users_followed,
                                                 'followers': followers})


@login_required
def flux(request):
    # On recupere tous les utilisateurs qu'ils suit
    tickets, reviews = get_users_viewable_posts(request.user)
    posts = sorted(itertools.chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    return render(request, 'ticket/flux.html', {'section': 'flux',
                                                'posts': posts})


@login_required
def create_ticket(request):
    sent = False
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, files=request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.time_created = datetime.datetime.now()
            ticket.save()
            sent = True
    else:
        ticket_form = TicketForm()
    return render(request, 'ticket/create_ticket.html', {'section': 'flux',
                                                         'ticket_form': ticket_form,
                                                         'sent': sent})


@login_required
def create_ticket_review(request):
    sent = False
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, files=request.FILES, prefix='ticketForm')
        review_form = ReviewForm(request.POST, prefix='reviewForm')
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.time_created = datetime.datetime.now()
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.time_created = datetime.datetime.now()
            review.save()
            sent = True
    else:
        ticket_form = TicketForm(prefix='ticketForm')
        review_form = ReviewForm(prefix='reviewForm')
    return render(request, 'ticket/create_ticket_review.html', {'section': 'flux',
                                                                'ticket_form': ticket_form,
                                                                'review_form': review_form,
                                                                'sent': sent})


@login_required
def create_review(request, id):
    ticket = Ticket.objects.filter(id=id)[0]
    sent = False

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.time_created = datetime.datetime.now()
            review.user = request.user
            review.save()
            sent = True
    else:
        review_form = ReviewForm()

    return render(request, 'ticket/create_review.html', {'section': 'flux',
                                                         'ticket': ticket,
                                                         'sent': sent,
                                                         'review_form': review_form})


@login_required
def edit_ticket(request, id):
    sent = False
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, instance=ticket, files=request.FILES)
        if ticket_form.is_valid():
            ticket_form.save()
            sent = True
    else:
        ticket_form = TicketForm(instance=ticket)
    return render(request, 'ticket/edit_ticket.html', {'section': 'posts',
                                                       'ticket_form': ticket_form,
                                                       'sent': sent})


@login_required
def edit_review(request, id):
    sent = False
    review = get_object_or_404(Review, id=id)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            sent = True
    else:
        review_form = ReviewForm(instance=review)
    return render(request, 'ticket/edit_review.html', {'section': 'posts',
                                                       'ticket': review.ticket,
                                                       'review_form': review_form,
                                                       'sent': sent})
