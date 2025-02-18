from django.db import models
from django.contrib.auth.models import User

class Naani(models.Model):
    name = models.CharField(max_length=100)
    experience = models.IntegerField()
    rating = models.FloatField()
    availability = models.CharField(max_length=100)
    image = models.ImageField(upload_to='nanni_images/')

    def __str__(self):
        return self.name

class DiscussionThread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Reply(models.Model):
    thread = models.ForeignKey(DiscussionThread, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reply by {self.created_by.username} on {self.thread.title}"

class Pediatrician(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, default='Pediatrician')
    experience = models.CharField(max_length=50, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='pediatricians/', null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name