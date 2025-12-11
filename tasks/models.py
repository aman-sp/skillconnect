from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    CATEGORY_CHOICES = (
        ('design', 'Design'),
        ('coding', 'Coding'),
        ('editing', 'Video Editing'),
        ('data', 'Data Work'),
        ('general', 'General Task'),
    )

    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Application(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    sample_file = models.FileField(upload_to='samples/', null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'freelancer')

    def __str__(self):
        return f"{self.freelancer.username} → {self.task.title}"
