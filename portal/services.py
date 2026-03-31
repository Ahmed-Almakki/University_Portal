from .models import Grade, Application, Document, Discipline

def get_student_academic_record(student_user):
    """Fetches all grades for a specific student."""
    grades = Grade.objects.filter(student=student_user).select_related('discipline')
    return grades


def request_official_certificate(student_user):
    """Creates a certificate request application for the student."""
    Application.objects.create(student=student_user, type='certificate')


def request_retake_referral(student_user, subject_id):
    """Creates a retake referral application for the specified subject."""
    discipline = Discipline.objects.get(id=subject_id)
    Application.objects.create(student=student_user, type='retake', discipline=discipline)


def apply_for_scholarship_increase(student_user, files):
    """Creates a scholarship increase application and attaches the uploaded files."""
    application = Application.objects.create(student=student_user, type='scholarship')
    for file in files:
        Document.objects.create(application=application, file=file)