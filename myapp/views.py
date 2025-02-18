from django.shortcuts import render, get_object_or_404, redirect
from .models import Naani
from django.contrib.auth.decorators import login_required
from .models import DiscussionThread, Reply
from .forms import DiscussionThreadForm, ReplyForm
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
    experience = request.GET.get('experience')
    age = request.GET.get('age')
    rating = request.GET.get('rating')

    # Filter the nannies based on the attributes
    nannies = Naani.objects.all()

    if experience:
        nannies = nannies.filter(experience__gte=experience)
    if age:
        nannies = nannies.filter(age__lte=age)
    if rating:
        nannies = nannies.filter(rating__gte=rating)

    return render(request, 'get_naani.html', {'nannies': nannies})

@login_required
def book_naani(request, nanny_id):
    nanny = get_object_or_404(Naani, id=nanny_id)
    return render(request, 'book_naani.html', {'nanny': nanny})

@login_required
def confirm_booking(request, nanny_id):
    if request.method == "POST":
        nanny = get_object_or_404(Naani, id=nanny_id)
        date = request.POST['date']
        time = request.POST['time']
        duration = request.POST['duration']
        
        Booking.objects.create(user=request.user, nanny=nanny, date=date, time=time, duration=duration, status='Pending')
        
        return redirect('naani_dashboard')

@login_required
def naani_dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'naani_dashboard.html', {'bookings': bookings})


def parenting_tips(request):
  return render(request, "parenting_tips.html")

def discussion_forum(request):
  return render(request, "discussion_forum.html")


def discussion_forum(request):
    threads = DiscussionThread.objects.all().order_by('-created_at')
    return render(request, 'discussion_forum.html', {'threads': threads})

def discussion_detail(request, pk):
    thread = get_object_or_404(DiscussionThread, pk=pk)
    replies = thread.replies.all()
    if request.method == "POST":
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.thread = thread
            reply.created_by = request.user
            reply.save()
            return redirect('discussion_detail', pk=pk)
    else:
        reply_form = ReplyForm()
    return render(request, 'discussion_detail.html', {'thread': thread, 'replies': replies, 'reply_form': reply_form})

def discussion_create(request):
    if request.method == "POST":
        form = DiscussionThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.created_by = request.user
            thread.save()
            return redirect('discussion_forum')
    else:
        form = DiscussionThreadForm()
    return render(request, 'discussion_create.html', {'form': form})

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