from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    path('<int:id>/rating/submit/', views.submit_rating, name='movies.submit_rating'),
    path('<int:id>/review/<int:review_id>/reply/create/', views.create_reply, name='movies.create_reply'),
    path('<int:id>/reply/<int:reply_id>/delete/', views.delete_reply, name='movies.delete_reply'),
    path('petitions/', views.petitions_list, name='movies.petitions_list'),
    path('petitions/create/', views.create_petition, name='movies.create_petition'),
    path('petitions/<int:petition_id>/', views.petition_detail, name='movies.petition_detail'),
    path('petitions/<int:petition_id>/vote/', views.vote_petition, name='movies.vote_petition'),
    path('petitions/<int:petition_id>/delete/', views.delete_petition, name='movies.delete_petition'),
]
