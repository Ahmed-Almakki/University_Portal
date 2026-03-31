from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator


class Group(models.Model):
    """Student groups (e.g., 'CS-2024')"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    """Physical rooms for the schedule"""
    room_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.room_number


class Discipline(models.Model):
    """Subjects being taught"""
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title
    

class Lesson(models.Model):
    """The Schedule System"""
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='schedule')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'teacher'}
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.discipline.title} - {self.group.name}"
    

class Grade(models.Model):
    """Grades recorded by teachers for students"""
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='grades',
        limit_choices_to={'role': 'student'}
    )
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField()
    date_recorded = models.DateTimeField(auto_now_add=True)

    @property
    def is_debt(self):
        """Automatically calculates if the subject is failed (e.g., score < 50)"""
        return self.score < 50

    def __str__(self):
        return f"{self.student.username} - {self.discipline.title}: {self.score}"
    

class Application(models.Model):
    """Applications submitted by students for various requests (e.g., certificate, retake)"""
    APPLICATION_TYPES = [
        ('certificate', 'Certificate of Study'),
        ('retake', 'Retake Referral'),
        ('scholarship', 'Increased Scholarship'),
    ]
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=APPLICATION_TYPES)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.student.username}"
    


class Announcement(models.Model):
    """Announcements posted by teachers for students"""
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # If target_group is NULL, the announcement is for ALL students
    target_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Document(models.Model):
    """Documents uploaded by students or teachers (e.g., application attachments, announcement files)"""
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'jpg'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id}"