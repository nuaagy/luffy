from rest_framework import serializers
from operator import attrgetter
from api.models import Course, CourseOutline


class CourseSerializer(serializers.Serializer):
    # choice
    id = serializers.IntegerField()
    name = serializers.CharField()
    course_type = serializers.CharField(source='get_course_type_display')
    level = serializers.CharField(source='get_level_display')

    hours = serializers.CharField(source='coursedetail.hours')


    class Meta:
        model = Course
        fields = ('id', 'name', 'course_type', 'level', 'hours')


class CourseDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    level = serializers.CharField(source='get_level_display')
    why_study = serializers.SerializerMethodField()
    what_to_study_brief = serializers.SerializerMethodField()
    recommend_courses = serializers.SerializerMethodField()

    def get_why_study(self, obj):
        return obj.coursedetail.why_study

    def get_what_to_study_brief(self, obj):
        return obj.coursedetail.what_to_study_brief

    def get_recommend_courses(self, obj):
        # print(obj.coursedetail.recommend_courses.all().values())  # 一对一反向查询
        return [attrgetter('name')(i) for i in obj.coursedetail.recommend_courses.all()]
    class Meta:
        model = Course
        fields = ('name', 'level', 'why_study')


class CourseQuestionSerializer(serializers.Serializer):
    name = serializers.CharField()
    # questions = serializers.CharField(source='asked_question.all.values')
    questions = serializers.SerializerMethodField()

    def get_questions(self, obj):
        return obj.asked_question.all().values('question', 'answer')
    class Meta:
        model = Course
        fields = ('name', 'questions')

class CourseOutlineSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseOutline
        fields = '__all__'

