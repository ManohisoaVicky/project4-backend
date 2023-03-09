from django.shortcuts import render
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics

from .models import Event
from .serializers import EventSerializer, PopulatedEventSerializer
# Create your views here.

class EventListCreate(APIView):
    # permission_classes = 

    def get(self, request):
        events = Event.objects.all().order_by('-id')

        name = request.query_params.get("name")

        if name is not None or "":
            events = events.filter(name__icontains=name)

        serializer = PopulatedEventSerializer(events, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        new_event = Event.objects.create(
            name = request.data['name'],
            description = request.data['description'],
            date = request.data['date'],
            time = request.data['time'],
            duration = request.data['duration'],
            host_id = request.user.id
        )
        new_event.save()
        serializer = EventSerializer(new_event)
        return JsonResponse(serializer.data, safe=False)


class EventDetailUpdateDelete(APIView):

    def get(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
            serializer = PopulatedEventSerializer(event)
            return JsonResponse(serializer.data, safe=False)
        except Event.DoesNotExist:
            raise Http404('Event does not exist')

    def post(self, request, pk):
        event = Event.objects.get(id=pk)
        user = request.user.id
        event.participant.add(user)
        serializer = EventSerializer(event, request.data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse({"message":"You've successfully registered to an event"})

    def patch(self, request, pk):
        event = Event.objects.get(id=pk)
        data = request.data
        host = request.data['host']['id']
        data['host'] = host
        serializer = EventSerializer(event, data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(serializer.data)

    def delete(self, request, pk):
        event = Event.objects.get(id=pk)
        event.delete()

        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    
class AllUserEvents(APIView):

    def get(self, request, pk):
        events = Event.objects.filter(host_id=pk).order_by('date')
        serializer = EventSerializer(events, many=True)
        return JsonResponse(serializer.data, safe=False)

class JoinedEvents(APIView):

    def get(self, request, pk):
        events = Event.objects.all().filter(participant=pk).prefetch_related('participant').order_by('date')
        serializer = PopulatedEventSerializer(events, many=True)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, pk):
        event = Event.objects.get(id=pk)
        user = request.user.id
        event.participant.remove(user)
        return JsonResponse({"message":"You've successfully cancelled your participation in the event"})


