import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import tensorflow as tf
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Load the trained model
MODEL_PATH = "/Users/rajendran/Desktop/BabyCare/BabyCare/myapp/ml_models/cry_classification_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

def preprocess_audio(file_path, img_path):
    """
    Convert audio file to Mel spectrogram and save as an image.
    """
    y, sr = librosa.load(file_path, sr=22050)
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    
    # Save spectrogram as image
    plt.figure(figsize=(5, 5))
    librosa.display.specshow(mel_spectrogram_db, sr=sr, cmap='inferno')
    plt.axis('off')
    plt.savefig(img_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    # Load the saved image for model input
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@csrf_exempt
def predict_audio(request):
    """
    Handle uploaded audio, process it, and return a prediction.
    """
    if request.method == "POST" and request.FILES.get("audio"):
        audio_file = request.FILES["audio"]
        file_path = default_storage.save(f"temp/{audio_file.name}", audio_file)
        img_path = f"temp/{audio_file.name}.png"
        
        try:
            img_array = preprocess_audio(default_storage.path(file_path), default_storage.path(img_path))
            prediction = model.predict(img_array)
            predicted_class = np.argmax(prediction, axis=1)[0]
            labels = ['Hungry', 'Tired', 'Uncomfortable', 'Fussy', 'Happy']
            result = labels[predicted_class]
            
            return JsonResponse({"prediction": result})
        except Exception as e:
            return JsonResponse({"error": str(e)})
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(img_path):
                os.remove(img_path)
    
    return render(request, "prediction.html")


