from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('teacher', 'teacher'),
        ('student', 'student'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    group = models.ForeignKey('portal.Group', on_delete=models.SET_NULL, null=True, blank=True)

    REQUIRED_FIELDS = ['role']
    
    def save(self, *args, **kwargs):
        """
        Generate username automatically based on the id and admission year
        """
        if not self.pk:  # Only generate username for new users
            super().save(*args, **kwargs)
            
            current_year = timezone.now().year
            self.username = f"{current_year}{self.id:04d}"
            
            # Save again with the username
            super().save(update_fields=['username'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.username