from django.shortcuts import render
import markdown
from rest_framework.decorators import api_view
from rest_framework.response import Response

from itinerary.utils import generate_itinerary, get_local_recommendations, get_weather_forecast


def itinerary_view(request):
    if request.method == 'POST':
        destination = request.POST.get('destination')
        preferences = request.POST.get('preferences')

        if not destination or not preferences:
            return Response({'error': 'Destination and preferences are required'}, status=400)

        itinerary = generate_itinerary(destination, preferences)

        itinerary_html = markdown.markdown(itinerary)

        local_recommendation = get_local_recommendations(destination)

        weather = get_weather_forecast(destination)

        return render(request, 'generate.html', {
            'destination': destination,
            'preferences': preferences,
            'itinerary': itinerary_html,
            'local_recommendation': local_recommendation,
            'weather': weather
        })

    return render(request, 'generate.html')
