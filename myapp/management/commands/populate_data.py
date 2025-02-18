from myapp.models import Naani
from typing import Any
from django.core.management.base import BaseCommand

class Command(BaseCommand):
  help = "This command inserts the naani data"

  def handle(self, *args: Any, **kwargs: Any): 
    names = [
        "Sunita Verma", "Meera Iyer", "Anita Sharma", "Radha Kapoor", "Pooja Joshi",
        "Kavita Reddy", "Geeta Nair", "Lakshmi Pillai", "Sarita Chauhan", "Neha Dixit",
        "Savita Patil", "Jyoti Mishra", "Indira Das", "Uma Shankar", "Rekha Thakur",
        "Sushma Yadav", "Manju Saxena", "Kamala Rao", "Deepa Ghosh", "Mala Menon"
    ]

    experience = [
        6, 8, 5, 10, 4,
        7, 9, 3, 12, 6,
        5, 8, 7, 11, 4,
        6, 9, 3, 10, 5
    ]

    ratings = [
        4.7, 4.9, 4.5, 5.0, 4.2,
        4.8, 4.6, 4.0, 5.0, 4.7,
        4.5, 4.8, 4.6, 4.9, 4.3,
        4.7, 4.9, 4.1, 5.0, 4.4
    ]

    availability = [
        "Monday - Friday", "Weekends", "Full-time", "Monday - Saturday", "Part-time",
        "Flexible Hours", "Morning Shift", "Evening Shift", "24/7", "Monday - Thursday",
        "Friday - Sunday", "On Call", "Only Weekdays", "Only Weekends", "Overnight",
        "Afternoon Shift", "Morning & Evening", "Rotational Shifts", "Custom Schedule", "Full-time"
    ]

    images = [
        "nanni_images/sunita.jpg", "nanni_images/meera.jpg", "nanni_images/anita.jpg",
        "nanni_images/radha.jpg", "nanni_images/pooja.jpg", "nanni_images/kavita.jpg",
        "nanni_images/geeta.jpg", "nanni_images/lakshmi.jpg", "nanni_images/sarita.jpg",
        "nanni_images/neha.jpg", "nanni_images/savita.jpg", "nanni_images/jyoti.jpg",
        "nanni_images/indira.jpg", "nanni_images/uma.jpg", "nanni_images/rekha.jpg",
        "nanni_images/sushma.jpg", "nanni_images/manju.jpg", "nanni_images/kamala.jpg",
        "nanni_images/deepa.jpg", "nanni_images/mala.jpg"
    ]

    for name, experience, rating, availability, image in zip(names, experience, ratings, availability, images):
        Naani.objects.create(
            name = name,
            experience = experience,
            rating = rating,
            availability = availability,
            image = image
        )

    self.stdout.write(self.style.SUCCESS("completed inserting data"))
