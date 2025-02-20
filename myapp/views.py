from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Naani, DiscussionThread, Reply, Pediatrician
from .forms import DiscussionThreadForm, ReplyForm
from .ml_models.predict import model, preprocess_audio
import numpy as np
import json
import os

# --------- BASIC VIEWS ------------
def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def sign_up(request):
    return render(request, "sign_up.html")

def cry_detection(request):
    return render(request, "cry_detection.html")

def play_audio(request):
    return render(request, "play_audio.html")

def health_tips(request):
    return render(request, "health_tips.html")

def milestone_tracker(request):
    return render(request, "milestone_tracker.html")

def moms_corner(request):
    return render(request, "moms_corner.html")

def parenting_tips(request):
    return render(request, "parenting_tips.html")

def memory_book(request):
    return render(request, "memory_book.html")

def growth_track(request):
    return render(request, "growth_track.html")

def about(request):
    return render(request, "about.html")

def profile(request):
    return render(request, "profile.html")

def contact(request):
    return render(request, "contact.html")

def emergency_care(request):
    return render(request, "emergency_care.html")


# --------- NAANI FILTERING ------------
def get_naani(request):
    experience = request.POST.get('experience', '')
    age = request.POST.get('age', '')
    rating = request.POST.get('rating', '')

    nannies = Naani.objects.all()

    if experience:
        nannies = nannies.filter(experience__gte=experience)
    if age:
        nannies = nannies.filter(age__lte=age)
    if rating:
        nannies = nannies.filter(rating__gte=rating)

    return render(request, 'get_naani.html', {'nannies': nannies})


@login_required
def book_naani(request):
    return render(request, 'book_naani.html')


# --------- DISCUSSION FORUM ------------
def discussion_forum(request):
    threads = DiscussionThread.objects.all().order_by('-created_at')
    return render(request, 'discussion_forum.html', {'threads': threads})


def discussion_list(request):
    """ Fetch all discussion threads and return JSON response """
    threads = list(DiscussionThread.objects.values("id", "title", "content", "created_by__username", "created_at"))
    return JsonResponse({"threads": threads})


@login_required
@csrf_exempt
def create_discussion(request):
    """ Create a new discussion thread """
    try:
        if request.method == "POST":
            data = json.loads(request.body.decode("utf-8"))
            title = data.get("title")
            content = data.get("content")

            if title and content:
                thread = DiscussionThread.objects.create(title=title, content=content, created_by=request.user)
                return JsonResponse({"message": "Discussion created successfully!", "thread_id": thread.id}, status=201)

        return JsonResponse({"error": "Invalid request"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def discussion_detail(request, pk):
    thread = get_object_or_404(DiscussionThread, pk=pk)
    replies = thread.replies.all()
    
    if request.method == "POST":
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.thread = thread
            reply.created_by = request.user  # Using actual logged-in user
            reply.save()
            return redirect('discussion_detail', pk=pk)

    else:
        reply_form = ReplyForm()

    return render(request, 'discussion_detail.html', {'thread': thread, 'replies': replies, 'reply_form': reply_form})


@login_required
def discussion_create(request):
    """ Create a discussion thread via a form """
    if request.method == "POST":
        form = DiscussionThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.created_by = request.user
            thread.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check for AJAX request
                return JsonResponse({
                    'id': thread.id,
                    'title': thread.title,
                    'content': thread.content,
                    'created_by': thread.created_by.username,
                    'created_at': thread.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }, status=201)

            return redirect('discussion_forum')  # Redirect for normal form submissions
    else:
        form = DiscussionThreadForm()

    return render(request, 'discussion_create.html', {'form': form})


# --------- TELEHEALTH ------------
def telehealth(request):
    pediatricians = Pediatrician.objects.all()
    return render(request, "telehealth.html", {'doctors': pediatricians})


# --------- INFANT CRY PREDICTION ------------
@csrf_exempt
def prediction(request):
    if request.method == "POST" and request.FILES.get("audio_file"):
        try:
            # Save uploaded file with a unique name
            audio_file = request.FILES["audio_file"]
            file_name = f"temp_{get_random_string(8)}.wav"
            file_path = default_storage.save(file_name, ContentFile(audio_file.read()))

            # Process the audio file
            img_array = preprocess_audio(default_storage.path(file_path))

            # Make prediction
            predictions = model.predict(img_array)
            predicted_class = np.argmax(predictions, axis=1)[0]

            # Map class index to label
            class_labels = ["Hungry", "Sleepy", "Uncomfortable", "Fussy", "Pain"]
            predicted_label = class_labels[predicted_class]

            # Delete temporary file
            default_storage.delete(file_path)

            return JsonResponse({"prediction": predicted_label}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def book_naani(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        mobile = data.get("mobile")
        date = data.get("date")
        nanny_name = data.get("nanny_name")

        # Here, save booking details in the database
        # Example:
        # Booking.objects.create(user_name=name, mobile=mobile, date=date, nanny=nanny_name)

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False}, status=400)