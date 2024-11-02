from django.db import models

# Create your models here.

class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Make sure to hash passwords in a real project!

    def __str__(self):
        return self.username
    
class UserContent(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)  # Each user has one content record
    content = models.TextField(max_length=10000, blank=True)  # Store up to 10,000 words (or adjust as necessary)

    def __str__(self):
        return f"Content for {self.user.username}"