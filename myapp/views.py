from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
  return render(request, "index.html")

def login(request):
  return render(request, "login.html")

def sign_up(request):
  return render(request, "sign_up.html")

def cry_detection(request):
  return render(request, "cry_detection.html")

def get_naani(request):
  return render(request, "get_naani.html")

def parenting_tips(request):
  return render(request, "parenting_tips.html")

def discussion_forum(request):
  return render(request, "discussion_forum.html")

def telehealth(request):
  return render(request, "telehealth.html")

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