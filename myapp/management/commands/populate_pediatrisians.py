from django.core.management.base import BaseCommand
from myapp.models import Pediatrician
from typing import Any

class Command(BaseCommand):
    help = 'Populate the database with sample pediatricians'

    def handle(self, *args, **kwargs):
        pediatricians_data = [
            {
                "name": "Dr. Karthick Annamalai",
                "specialty": "Cardiologist",
                "experience": "10 years",
                "description": "Highly skilled cardiologist specializing in pediatric heart conditions.",
                "contact": "123-456-7890",
                "image": "assests/Pediatrics-KarthickAnnamalai-5173be-removebg-preview.png"
            },
            {
                "name": "Dr. Siva Bharathi",
                "specialty": "Pediatrician",
                "experience": "22 years",
                "description": "Expert in general pediatric care, with a focus on newborn health.",
                "contact": "987-654-3210",
                "image": "assests/Pediatrics-SivaBharathi-Coimbatore-cba9f5__1_-removebg-preview.png"
            },
            {
                "name": "Dr. Shera Fatima",
                "specialty": "Pediatrician",
                "experience": "15 years",
                "description": "Dedicated pediatrician providing exceptional care for children of all ages.",
                "contact": "555-123-4567",
                "image": "assests/SheraFatima-21f697-removebg-preview.png"
            },
            {
                "name": "Dr. Sruthi S Nair",
                "specialty": "Pediatric Orthopedic Surgeon",
                "experience": "12 years",
                "description": "Specializes in pediatric musculoskeletal disorders and orthopedic surgery.",
                "contact": "333-444-5555",
                "image": "assests/SruthiSNair-6be1f4-removebg-preview.png"
            },
            {
                "name": "Dr. Rajendran K",
                "specialty": "MBBS., MD",
                "experience": "8 years",
                "description": "Specializes in pediatric musculoskeletal disorders",
                "contact": "4323604",
                "image": "assests/3Dr.K.Rajendran-removebg-preview.png"
            },
            {
                "name": "Dr. MANONMANI GANESAN",
                "specialty": "MBBS., MRCPCH (UK)",
                "experience": "10 years",
                "description": "Specializes in pediatric  orthopedic surgery.",
                "contact": "333-444-5555",
                "image": "assests/Dr.G.Manonmani-removebg-preview.png"
            }
        ]
        
        for data in pediatricians_data:
            Pediatrician.objects.create(
                name=data["name"],
                specialty=data["specialty"],
                experience=data["experience"],
                description=data["description"],
                contact=data["contact"],
                image=data["image"]
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated pediatricians'))
