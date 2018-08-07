from django.shortcuts import HttpResponse
from api.models import *

def query(request):
    # 1.查询所有学位课名称奖学金
    # dc = DegreeCourse.objects.all().values('name', 'total_scholarship')
    # print(list(dc))

    # 2.查询所有学位课名称 老师
    # course_name_teacher = DegreeCourse.objects.all().values('name', 'teachers__name')
    # print(course_name_teacher)

    # 3.查询所有专题课
    # course = Course.objects.filter(degree_course__isnull=True).values('name')
    # print(course)

    # 4.查询id=1学位课 所有模块名称
    # dc = DegreeCourse.objects.filter(pk=1).values('course__name')
    # print(dc)
    # course = Course.objects.filter(degree_course__id=1).values('name')
    # print(course)

    obj = DegreeCourse.objects.get(pk=1)
    obj.course_set.all()

    # 5.获取id=1的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses
    # course_queryset = Course.objects.filter(pk=1)
    # course_detail = course_queryset.values('coursedetail__why_study', 'coursedetail__what_to_study_brief', 'coursedetail__recommend_courses__name')
    # course_type = course_queryset.first().get_course_type_display()
    # course_detail[0].update(course_type=course_type)
    # print(course_detail)
    # course_detail = CourseDetail.objects.filter(course__id=1).values('why_study', 'what_to_study_brief', 'recommend_courses__name')

    # 6.获取id=1的专题课，并打印该课程相关的所有常见问题
    course_often_question = Course.objects.get(pk=1).asked_question.all().values('question', 'answer')
    # print(course_often_question)

    # 7.获取id=1的专题课，并打印该课程相关的课程大纲
    # course_outline = Course.objects.filter(pk=1).values('coursedetail__courseoutline__content')
    #
    # # c = CourseOutline.objects.filter(course_detail__course_id__exact=1).values()
    # print(course_outline)

    # 8.获取id=1的专题课，并打印该课程相关的所有章节
    # chapters = Course.objects.filter(pk=1).values('coursechapters__chapter', 'coursechapters__summary')
    # print(chapters)

    # cs = CourseChapter.objects.filter(course__id=1).values()
    # print(cs)

    # 9.获取id=1的专题课，并打印该课程相关的所有课时
    sections = CourseSection.objects.filter(chapter__course_id__exact=1).values('chapter__name', 'chapter__chapter', 'name')


    # sections = Course.objects.filter(pk=1).values('coursechapters__chapter', 'coursechapters__name', 'coursechapters__coursesections__name')
    # print(sections)


    # 10.获取id=1的专题课，并打印该课程相关的所有的价格策略
    price_policy = DegreeCourse.objects.filter(pk=1).first().degreecourse_price_policy.all()
    for obj in price_policy:
        print(obj.get_valid_period_display(), obj.price)
    return HttpResponse('OK', status=200)

