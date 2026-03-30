from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class User(AbstractUser):
    admission_year = models.IntegerField()
    student_id = models.CharField(max_length=20, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['student_id', 'admission_year', 'email']


    def save(self, *args, **kwargs):
        """
        Override save method to instead of saving the username, we will save the student_id and the admission year,
        and the username will be generated automatically based on the student_id and the admission year.
        """
        self.username = f"{self.student_id}{self.admission_year}"
        super().save(*args, **kwargs)


    def __str__(self):
        return self.username