from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Accepted by AI'),
        ('rejected', 'Rejected by AI'),
        ('pending', 'Pending'),
    ]
    MANUAL_STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_image = models.ImageField(upload_to='images/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    manual_status = models.CharField(
        max_length=10,
        choices=MANUAL_STATUS_CHOICES,
        default='pending'
    )




    def __str__(self):
        return f"Report {self.id} by {self.user.username}"

    def accept_report(self):
        self.status = 'accepted'
        self.save()

    def reject_report(self):
        self.status = 'rejected'
        self.save()
        
        
    def set_manual_pending(self):
        self.manual_status = 'pending'
        self.save()







        
