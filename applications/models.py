from django.db import models
from accounts.models import User
from opportunities.models import Opportunity

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    portfolio = models.FileField(upload_to='portfolios/', blank=True, null=True)  
    certificates = models.FileField(upload_to='certificates/', blank=True, null=True)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.opportunity.title}"
