from django.db import models
from django.contrib.auth.models import User

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
