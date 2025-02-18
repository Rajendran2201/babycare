from myapp.models import DiscussionThread, Reply
from typing import Any
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
  help = "This command inserts the discussion data"

  def handle(self, *args: Any, **kwargs: Any): 
        # List of titles for discussion threads
    thread_titles = [
        "Best Practices for Baby Care",
        "How to Handle Infant Crying",
        "Nutrition Tips for Infants",
        "Choosing the Right Nanny for Your Child",
        "How to Soothe a Fussy Baby",
        "Tips for New Parents in India",
        "Managing Sleep Schedules for Babies",
        "The Importance of Baby's First Year",
        "Dealing with Colic in Babies",
        "Baby Milestones and Growth Tracking"
    ]

    # List of content for the discussion threads
    thread_content = [
        "As new parents, it's important to learn about baby care practices. Here are some best practices to follow...",
        "Infant crying can be distressing, but understanding the causes can help you respond appropriately...",
        "Breastfeeding, formula feeding, and introducing solids — what's best for your baby's nutrition? Let's discuss...",
        "When looking for a nanny, consider experience with infants, certifications, and their approach to child care...",
        "A fussy baby can be challenging. Here's how you can calm your little one during those tough times...",
        "Being a parent in India comes with its own set of challenges, from managing family expectations to handling childcare...",
        "Sleep routines for babies vary, but establishing a good pattern is key for their development. Here are some tips...",
        "The first year of your baby's life is full of milestones, from rolling over to their first steps. Celebrate every moment!",
        "Colic is a common condition that can cause severe discomfort in babies. Here's what you can do to help your baby...",
        "Tracking your baby's growth and milestones is essential. Let's discuss the key milestones you should be watching for..."
    ]

    # List of created_by user names (Indian names)
    thread_created_by = [
        "Ananya Sharma", "Ravi Kumar", "Priya Gupta", "Arvind Yadav", "Sanya Patel",
        "Rahul Mehta", "Simran Kaur", "Vikram Singh", "Neha Desai", "Kunal Verma"
    ]

    # List of created_at dates (for example, from the last 30 days)
    from datetime import datetime, timedelta
    import random

    thread_created_at = [
        (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S") for _ in range(10)
    ]

        # List of content for the replies
    reply_content = [
        "I agree! Baby care can be overwhelming, but following a routine helps a lot.",
        "For soothing a baby, I found that rocking them gently in a cradle works wonders.",
        "Breastfeeding is definitely a great choice, especially in the first 6 months.",
        "I personally believe that choosing a nanny who has prior experience with newborns is crucial.",
        "When my baby had colic, we found that tummy massages and holding them upright helped relieve some discomfort.",
        "It's so helpful to have support from family members in the early months, especially in Indian households.",
        "Sleep routines can be challenging, but it's all about consistency. I try to follow the same bedtime every day.",
        "Yes, tracking milestones gives us so much joy! My baby just turned one and it’s been a wonderful journey.",
        "Colic can be tough on both the baby and parents, but there are ways to alleviate the pain.",
        "Watching my baby's first steps was one of the happiest moments of my life!"
    ]

    # List of created_by user names (Indian names)
    reply_created_by = [
        "Priya Patel", "Ankit Mehra", "Deepika Nair", "Suresh Reddy", "Rajesh Jain",
        "Sanya Kapoor", "Vikash Kumar", "Manju Sharma", "Amit Verma", "Rani Soni"
    ]

    # List of created_at dates (for example, from the last 7 days)
    reply_created_at = [
        (datetime.now() - timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d %H:%M:%S") for _ in range(10)
    ]


   # Assuming we have a list of Users to assign created_by (you can create some sample users)
    users = User.objects.all()

    # Populate the DiscussionThread model
    for i in range(10):
        thread = DiscussionThread.objects.create(
            title=random.choice(thread_titles),
            content=random.choice(thread_content),
            created_by=random.choice(users),
            created_at=random.choice(thread_created_at)
        )

        # Populate the Reply model for each thread
    for _ in range(random.randint(1, 3)):  # Each thread can have 1 to 3 replies
            Reply.objects.create(
                thread=thread,
                content=random.choice(reply_content),
                created_by=random.choice(users),
                created_at=random.choice(reply_created_at)
            )

    self.stdout.write(self.style.SUCCESS("completed inserting data"))
