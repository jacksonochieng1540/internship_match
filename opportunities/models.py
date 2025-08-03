from django.db import models
from accounts.models import User

class Opportunity(models.Model):
    JOB_TYPE_CHOICES = [
        ('internship', 'Internship'),
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
    ]

    company = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'company'})
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills_required = models.CharField(max_length=300)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='internship')
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
