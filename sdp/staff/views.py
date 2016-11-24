from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Instructor, Participant


def all_instructors(request):
    instructors = []
    for instructor in Instructor.objects.all():
        instructors.append(model_to_dict(instructor))
    return JsonResponse({'all_instructors': instructors})


def all_participants(request):
    participants = []
    for participant in Participant.objects.all():
        participants.append(model_to_dict(participant))
    return JsonResponse({'all_participants': participants})
