from myapp.models import Naani
from typing import Any
from django.core.management.base import BaseCommand

class Command(BaseCommand):
  help = "This command inserts the naani data"

  def handle(self, *args: Any, **kwargs: Any): 
    names = [
        "Sunita Verma", "Meera Iyer", "Anita Sharma", "Radha Kapoor", "Pooja Joshi",
        "Kavita Reddy", "Geeta Nair", "Lakshmi Pillai"
    ]

    experience = [
        12, 6,
        5, 8, 7, 11, 4,
        6
    ]

    ratings = [
        4.7, 4.9, 4.5, 5.0, 4.2,
        4.8,  4.0, 5.0
    ]

    availability = [
        "Monday - Friday", "Full-time", "Monday - Saturday", "Part-time",
        "Flexible Hours", "Morning Shift", "Evening Shift", "24/7"
    ]

    images = [
       "nannyImages/gayathri3.avif",
       "nannyImages/jansy2.avif",
       "nannyImages/jenifer5.avif",
       "nannyImages/nanny1.avif",
       "nannyImages/nanny4.avif",
       "nannyImages/sony6.avif",
       "nannyImages/usha8.avif",
       "nannyImages/v7.avif"

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
