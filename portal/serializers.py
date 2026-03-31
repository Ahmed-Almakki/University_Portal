from rest_framework import serializers
from .models import Grade, Discipline, Lesson

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['title']

class GradeSerializer(serializers.ModelSerializer):
    discipline = DisciplineSerializer(read_only=True)
    is_debt = serializers.ReadOnlyField() 

    class Meta:
        model = Grade
        fields = ['discipline', 'score', 'is_debt', 'date_recorded']

class ScheduleSerializer(serializers.ModelSerializer):
    discipline_name = serializers.CharField(source='discipline.title', read_only=True)
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True) # or use username
    classroom_number = serializers.CharField(source='classroom.room_number', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'discipline_name', 'group_name', 'teacher_name', 'classroom_number', 'start_time', 'end_time']