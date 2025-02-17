from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("sign_up", views.sign_up, name="sign_up"),
    path("get_naani", views.get_naani, name="get_naani"),
    path("cry_detection", views.cry_detection, name="cry_detection"),
    path("parenting_tips", views.parenting_tips, name="parenting_tips"),
    path("discussion_forum", views.discussion_forum, name="discussion_forum"),
    path("telehealth", views.parenting_tips, name="telehealth"),
    path("memory_book", views.memory_book, name="memory_book"),
    path("growth_track", views.growth_track, name="growth_track"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("profile", views.profile, name="profile"),
]
