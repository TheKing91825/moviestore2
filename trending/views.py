from django.shortcuts import render
from django.db.models import Count, Sum
from cart.models import Item, Order
from movies.models import Movie
from accounts.models import UserProfile

def trending_map(request):
    """Display map showing trending movies by region"""

    # Define regions with coordinates for map display
    regions_data = {
        'northeast': {
            'name': 'Northeast',
            'center_lat': 42.0,
            'center_lng': -73.0,
            'color': '#FF6B6B'
        },
        'southeast': {
            'name': 'Southeast',
            'center_lat': 33.0,
            'center_lng': -84.0,
            'color': '#4ECDC4'
        },
        'midwest': {
            'name': 'Midwest',
            'center_lat': 41.0,
            'center_lng': -93.0,
            'color': '#45B7D1'
        },
        'southwest': {
            'name': 'Southwest',
            'center_lat': 34.0,
            'center_lng': -111.0,
            'color': '#FFA07A'
        },
        'west': {
            'name': 'West',
            'center_lat': 40.0,
            'center_lng': -120.0,
            'color': '#98D8C8'
        }
    }

    # Calculate trending movies for each region
    regional_trending = {}

    for region_code, region_info in regions_data.items():
        # Get users from this region
        users_in_region = UserProfile.objects.filter(region=region_code).values_list('user_id', flat=True)

        # Get orders from users in this region
        orders_in_region = Order.objects.filter(user_id__in=users_in_region)

        # Get movie purchase counts for this region
        trending_movies = (
            Item.objects
            .filter(order__in=orders_in_region)
            .values('movie__id', 'movie__name', 'movie__image')
            .annotate(
                total_purchases=Sum('quantity'),
                order_count=Count('order', distinct=True)
            )
            .order_by('-total_purchases')[:5]  # Top 5 movies
        )

        regional_trending[region_code] = {
            'info': region_info,
            'movies': list(trending_movies)
        }

    # Get overall trending movies across all regions
    overall_trending = (
        Item.objects
        .values('movie__id', 'movie__name', 'movie__image')
        .annotate(
            total_purchases=Sum('quantity'),
            order_count=Count('order', distinct=True)
        )
        .order_by('-total_purchases')[:10]
    )

    # Get user's region if authenticated
    user_region = None
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        user_region = request.user.profile.region

    template_data = {
        'title': 'Local Popularity Map',
        'regional_trending': regional_trending,
        'overall_trending': list(overall_trending),
        'user_region': user_region,
        'regions_data': regions_data
    }

    return render(request, 'trending/map.html', {'template_data': template_data})