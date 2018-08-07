from rest_framework import serializers
from operator import itemgetter
from api.models import DegreeCourse

class DegreeCourseSerializer(serializers.Serializer):
    name = serializers.CharField()
    # teachers = serializers.CharField(source='teachers.all.values_list')
    teachers = serializers.SerializerMethodField()
    # Scholarship = serializers.CharField(source='scholarship_set.all')
    scholarship = serializers.SerializerMethodField()

    def get_scholarship(self, obj):
        # print(obj.scholarship_set.all().values('time_percent', 'value'))
        return obj.scholarship_set.all().values('time_percent', 'value')

    def get_teachers(self, obj):
        return [t.name for t in obj.teachers.all()]


    class Meta:
        model = DegreeCourse


class DegreeCourseDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    # course = serializers.CharField(source='course_set.all.values')
    course = serializers.SerializerMethodField()

    def get_course(self, obj):
        print(obj)
        print(obj.course_set.all().values('name'))
        return [itemgetter('name')(d) for d in obj.course_set.all().values('name')]

    class Meta:
        model = DegreeCourse