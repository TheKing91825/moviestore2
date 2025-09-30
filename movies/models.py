from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    
    def get_replies(self):
        """Get all replies for this review ordered by date"""
        return self.reply_set.all().order_by('date')
    
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Reply by {self.user.username} to review {self.review.id}"
    
    class Meta:
        verbose_name_plural = "Replies"

class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    movie_title = models.CharField(max_length=255)
    description = models.TextField()
    reason = models.TextField(help_text="Why should this movie be added to the catalog?")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petitions')
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def get_vote_count(self):
        """Get total number of votes for this petition"""
        return self.votes.count()
    
    def get_upvotes(self):
        """Get number of upvotes"""
        return self.votes.filter(vote_type='up').count()
    
    def get_downvotes(self):
        """Get number of downvotes"""
        return self.votes.filter(vote_type='down').count()
    
    def user_has_voted(self, user):
        """Check if user has already voted on this petition"""
        if user.is_authenticated:
            return self.votes.filter(user=user).exists()
        return False
    
    def get_user_vote(self, user):
        """Get user's vote on this petition"""
        if user.is_authenticated:
            try:
                return self.votes.get(user=user)
            except Vote.DoesNotExist:
                return None
        return None
    
    def __str__(self):
        return f"Petition for '{self.movie_title}' by {self.created_by.username}"
    
    class Meta:
        ordering = ['-created_at']

class Vote(models.Model):
    VOTE_CHOICES = [
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    ]
    
    id = models.AutoField(primary_key=True)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=4, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} {self.vote_type}voted petition {self.petition.id}"
    
    class Meta:
        unique_together = ('petition', 'user')  # Ensure one vote per user per petition