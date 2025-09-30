from django.contrib import admin

from .models import Movie, Review, Reply, Petition, Vote
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Reply)

class PetitionAdmin(admin.ModelAdmin):
    list_display = ['movie_title', 'created_by', 'created_at', 'is_active', 'get_vote_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['movie_title', 'created_by__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

class VoteAdmin(admin.ModelAdmin):
    list_display = ['petition', 'user', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['petition__movie_title', 'user__username']
    ordering = ['-created_at']

admin.site.register(Petition, PetitionAdmin)
admin.site.register(Vote, VoteAdmin)
