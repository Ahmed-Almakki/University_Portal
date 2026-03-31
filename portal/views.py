from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.permission import IsStudent 

from . import services
from .serializers import GradeSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class StudentDashboardAPI(APIView):
    """API endpoint for students to view their academic record and debts."""
    permission_classes = [IsStudent] 

    def get(self, request):
        try:
            print(f"Fetching academic record for student {request.user}")
            grades = services.get_student_academic_record(request.user)
            print(f"Fetched grades for student {grades}")
            serializer = GradeSerializer(grades, many=True)
            print(f"Serialized grades: {serializer.data}")
            total_debts = sum(1 for grade in grades if grade.is_debt)
            print(f"Total debts for student {request.user.student_id}: {total_debts}")
            return Response({
                "student_id": request.user.student_id,
                "total_debts": total_debts,
                "grades": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": "An error occurred while fetching the academic record.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StudentGradesAPI(APIView):
    """API endpoint for students to view their academic grades and debts (failed subjects)."""
    permission_classes = [IsStudent]
    def get(self, request):
        try:
            grades = services.get_student_academic_record(request.user)
            serializer = GradeSerializer(grades, many=True)
            failed_subjects = [grade for grade in grades if grade.is_debt]
            failed_serializer = GradeSerializer(failed_subjects, many=True)
            return Response({
                "student_id": request.user.student_id,
                "grades": serializer.data,
                "failed_subjects": failed_serializer.data,
                "total_failed": len(failed_subjects)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": "An error occurred while fetching grades.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OfficialCertificateRequestAPI(APIView):
    """API endpoint for students to request an official certificate of enrollment."""
    permission_classes = [IsStudent]
    def post(self, request):
        try:
            services.request_official_certificate(request.user)
            return Response(
                {"detail": "Certificate request submitted successfully."},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"detail": "Failed to submit certificate request.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RetakeExamReferralAPI(APIView):
    """API endpoint for students to request a referral for a retake exam for a failed subject."""
    permission_classes = [IsStudent]
    def post(self, request):
        subject_id = request.data.get("subject_id")
        if not subject_id:
            return Response(
                {"detail": "Subject ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            services.request_retake_referral(request.user, subject_id)
            return Response(
                {"detail": "Retake referral request submitted successfully."},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"detail": "Failed to submit retake referral request.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ScholarshipIncreaseApplicationAPI(APIView):
    """API endpoint for students to apply for increased scholarship with file uploads."""
    permission_classes = [IsStudent]
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        files = request.FILES.getlist('files')
        total_size = sum(f.size for f in files)
        if total_size > 250 * 1024 * 1024:
            return Response(
                {"detail": "Total upload size must not exceed 250 MB."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            services.apply_for_scholarship_increase(request.user, files)
            return Response(
                {"detail": "Scholarship increase application submitted successfully."},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"detail": "Failed to submit scholarship increase application.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )