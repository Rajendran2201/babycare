from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Naani, DiscussionThread, Reply, Pediatrician
from .forms import DiscussionThreadForm, ReplyForm
import numpy as np
import json
import os
import librosa
import librosa.display
import tensorflow as tf
import matplotlib.pyplot as plt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import BytesIO
import tensorflow as tf
import numpy as np
import librosa
import librosa.display
import noisereduce as nr  # Noise reduction
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend before importing pyplot
import matplotlib.pyplot as plt
import io
import os
import cv2
from django.http import JsonResponse

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


# Keep your existing model loading and labels
MODEL_PATH = "/Users/rajendran/Desktop/BabyCare/BabyCare/myapp/ml_models/mycnnmodel.h5"
model = tf.keras.models.load_model(MODEL_PATH)
LABELS = ["belly_pain", "hungry", "discomfort", "tired", "burping"]
def preprocess_audio(audio_path):
    try:
        # Load audio with standard parameters
        y, sr = librosa.load(audio_path, sr=22050)  # Back to original sample rate
        
        # Trim silence
        y, _ = librosa.effects.trim(y, top_db=20)
        
        # Basic noise reduction
        y = nr.reduce_noise(y=y, sr=sr, prop_decrease=0.4)
        
        # Generate Mel spectrogram with balanced parameters
        mel_spectrogram = librosa.feature.melspectrogram(
            y=y, 
            sr=sr,
            n_mels=80,     # Standard number of mel bands
            fmin=20,       # Include very low frequencies
            fmax=4000,     # Focus on baby cry frequency range
            hop_length=256 # Shorter hop length for better temporal resolution
        )
        
        # Convert to log scale with moderate compression
        mel_spectrogram_db = librosa.power_to_db(
            mel_spectrogram, 
            ref=np.max,
            top_db=60
        )
        
        # Simple normalization
        mel_spectrogram_db = (mel_spectrogram_db - mel_spectrogram_db.min()) / (mel_spectrogram_db.max() - mel_spectrogram_db.min())
        
        # Create spectrogram image
        plt.figure(figsize=(3, 3))
        librosa.display.specshow(
            mel_spectrogram_db, 
            sr=sr,
            cmap="magma"
        )
        plt.axis('off')
        
        # Save spectrogram
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0, dpi=300)
        plt.close()
        
        # Convert to model input
        buf.seek(0)
        img = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_COLOR)
        img_resized = cv2.resize(img, (224, 224))
        img_normalized = img_resized / 255.0
        
        return np.expand_dims(img_normalized, axis=0)
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None

@csrf_exempt
def predict_cry(request):
    if request.method == "GET":
        return render(request, 'prediction.html')
    
    elif request.method == "POST" and request.FILES.get("audio_file"):
        try:
            audio_file = request.FILES["audio_file"]
            
            # Save temporary file
            temp_path = "temp_audio.wav"
            with open(temp_path, "wb+") as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)
            
            # Process audio
            img_array = preprocess_audio(temp_path)
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            if img_array is None:
                return JsonResponse({
                    "status": "error",
                    "message": "Failed to process audio file"
                }, status=400)
            
            # Make prediction
            raw_predictions = model.predict(img_array)[0]
            
            # Get top 3 predictions with confidences
            top_3_indices = np.argsort(raw_predictions)[-3:][::-1]
            top_3_confidences = raw_predictions[top_3_indices]
            
            # Calculate confidence difference between top predictions
            confidence_diff = top_3_confidences[0] - top_3_confidences[1]
            
            # If the confidence difference is small, return multiple possibilities
            if confidence_diff < 0.2:  # Threshold for confidence difference
                response_text = f"Could be either {LABELS[top_3_indices[0]]} or {LABELS[top_3_indices[1]]}"
                if top_3_confidences[1] - top_3_confidences[2] < 0.1:
                    response_text += f" or {LABELS[top_3_indices[2]]}"
            else:
                response_text = LABELS[top_3_indices[0]]
            
            return JsonResponse({
                "status": "success",
                "prediction": response_text,
                "confidence": float(top_3_confidences[0]),
                "alternatives": [
                    {"label": LABELS[idx], "confidence": float(conf)}
                    for idx, conf in zip(top_3_indices, top_3_confidences)
                ]
            })
            
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)
    
    return JsonResponse({
        "status": "error",
        "message": "Invalid request"
    }, status=400)
# Django view function for classification
def classify_cry(request):
    if request.method == "POST" and request.FILES.get("audio_file"):
        audio_file = request.FILES["audio_file"]
        
        # Save to a temporary file
        temp_path = "temp_audio.wav"
        with open(temp_path, "wb") as f:
            f.write(audio_file.read())

        # Process and predict
        result = predict_cry(temp_path)

        # Clean up temp file
        os.remove(temp_path)

        if result:
            return JsonResponse({"prediction": result})
        else:
            return JsonResponse({"error": "Failed to process audio"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


