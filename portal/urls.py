from django.urls import path

from portal.views import StudentDashboardAPI,StudentGradesAPI,OfficialCertificateRequestAPI,RetakeExamReferralAPI,ScholarshipIncreaseApplicationAPI


urlpatterns = [
    path('student/dashboard/', StudentDashboardAPI.as_view(), name='student-dashboard'),
    path('student/grades/', StudentGradesAPI.as_view(), name='student-grades'),
    path('student/certificate/', OfficialCertificateRequestAPI.as_view(), name='official-certificate'),
    path('student/retake/', RetakeExamReferralAPI.as_view(), name='retake-referral'),
    path('student/scholarship/', ScholarshipIncreaseApplicationAPI.as_view(), name='scholarship-increase'),
]