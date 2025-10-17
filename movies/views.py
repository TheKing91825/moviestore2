rom django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Reply, Petition, Vote
from .models import Movie, Review, Reply, Petition, Vote, Rating
from .forms import PetitionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Avg

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    
    # Get rating information
    user_rating = None
    if request.user.is_authenticated:
        user_rating = movie.get_user_rating(request.user)
    
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['user_rating'] = user_rating
    template_data['average_rating'] = movie.get_average_rating()
    template_data['rating_count'] = movie.get_rating_count()
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def create_reply(request, id, review_id):
    if request.method == 'POST' and request.POST['comment'] != '':
        review = get_object_or_404(Review, id=review_id)
        reply = Reply()
        reply.comment = request.POST['comment']
        reply.review = review
        reply.user = request.user
        reply.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_reply(request, id, reply_id):
    reply = get_object_or_404(Reply, id=reply_id, user=request.user)
    reply.delete()
    return redirect('movies.show', id=id)

@login_required
@require_POST
def submit_rating(request, id):
    """Submit or update a movie rating"""
    movie = get_object_or_404(Movie, id=id)
    stars = request.POST.get('stars')
    
    if not stars or not stars.isdigit() or int(stars) not in range(1, 6):
        messages.error(request, 'Please select a valid rating (1-5 stars).')
        return redirect('movies.show', id=id)
    
    stars = int(stars)
    
    # Check if user already has a rating for this movie
    existing_rating = movie.get_user_rating(request.user)
    
    if existing_rating:
        # Update existing rating
        existing_rating.stars = stars
        existing_rating.save()
        messages.success(request, f'Your rating has been updated to {stars} stars.')
    else:
        # Create new rating
        Rating.objects.create(
            movie=movie,
            user=request.user,
            stars=stars
        )
        messages.success(request, f'You have rated this movie {stars} stars.')
    
    return redirect('movies.show', id=id)

# Petition Views
def petitions_list(request):
    """Display all active petitions"""
    petitions = Petition.objects.filter(is_active=True)
    template_data = {
        'title': 'Movie Petitions',
        'petitions': petitions
    }
    return render(request, 'movies/petitions_list.html', {'template_data': template_data})

@login_required
def create_petition(request):
    """Create a new movie petition"""
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Your movie petition has been created successfully!')
            return redirect('movies.petitions_list')
    else:
        form = PetitionForm()

    template_data = {
        'title': 'Create Movie Petition',
        'form': form
    }
    return render(request, 'movies/create_petition.html', {'template_data': template_data})

def petition_detail(request, petition_id):
    """Display petition details"""
    petition = get_object_or_404(Petition, id=petition_id, is_active=True)
    user_vote = petition.get_user_vote(request.user) if request.user.is_authenticated else None

    template_data = {
        'title': f'Petition: {petition.movie_title}',
        'petition': petition,
        'user_vote': user_vote
    }
    return render(request, 'movies/petition_detail.html', {'template_data': template_data})

@login_required
@require_POST
def vote_petition(request, petition_id):
    """Handle voting on petitions"""
    petition = get_object_or_404(Petition, id=petition_id, is_active=True)
    vote_type = request.POST.get('vote_type')

    if vote_type not in ['up', 'down']:
        messages.error(request, 'Invalid vote type.')
        return redirect('movies.petition_detail', petition_id=petition_id)

    # Check if user has already voted
    existing_vote = petition.get_user_vote(request.user)

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # User is trying to vote the same way again, remove the vote
            existing_vote.delete()
            messages.info(request, 'Your vote has been removed.')
        else:
            # User is changing their vote
            existing_vote.vote_type = vote_type
            existing_vote.save()
            messages.success(request, f'Your vote has been changed to {vote_type}vote.')
    else:
        # Create new vote
        Vote.objects.create(
            petition=petition,
            user=request.user,
            vote_type=vote_type
        )
        messages.success(request, f'You have {vote_type}voted for this petition.')

    return redirect('movies.petition_detail', petition_id=petition_id)

@login_required
def delete_petition(request, petition_id):
    """Delete a petition (only by creator or admin)"""
    petition = get_object_or_404(Petition, id=petition_id)

    if request.user != petition.created_by and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this petition.')
        return redirect('movies.petition_detail', petition_id=petition_id)

    if request.method == 'POST':
        petition.is_active = False  # Soft delete
        petition.save()
        messages.success(request, 'Petition has been deleted.')
        return redirect('movies.petitions_list')

    template_data = {
        'title': 'Delete Petition',
        'petition': petition
    }
    return render(request, 'movies/delete_petition.html', {'template_data': template_data})