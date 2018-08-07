import json

from django.shortcuts import HttpResponse
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning
from rest_framework.pagination import PageNumberPagination

from api.serializer.course import CourseSerializer, CourseDetailSerializer, \
    CourseQuestionSerializer, CourseOutlineSerializer
from api.pagination.course import CoursePagination
from api.serializer.degreecourse import DegreeCourseSerializer, DegreeCourseDetailSerializer



from api.models import Course, DegreeCourse

from django.utils.translation import ugettext_lazy as _

from api.utils.response import BaseResponse
class CourseVersioning(URLPathVersioning):
    invalid_version_message = _('版本无效')
    default_version = 'v1'
    ordering = 'id'
    allowed_versions = ('v1', 'v2')
    version_param = 'version'


class CourseView(APIView):
    """专题课或学位课模块视图
    """
    versioning_class = CourseVersioning
    def get(self, request, version):
        response = BaseResponse()
        try:
            # print(version)
            # print(request.version)
            # print(request.query_params)
            # course_list = Course.objects.all().values('id', 'name')
            # return HttpResponse(json.dumps(list(course_list), ensure_ascii=False))
            # list(QuerySet)-->list
            # JsonResponse non-dict safe=False
            # queryset = Course.objects.all().values()
            # return JsonResponse(list(queryset), safe=False)
            if request.query_params.get('a'):
                # 专题课
                queryset = Course.objects.filter(degree_course__isnull=True)
            else:
                # 学位课模块
                queryset = Course.objects.all()
            # 分页
            # p = PageNumberPagination()
            p = CoursePagination()
            course_list = p.paginate_queryset(queryset=queryset, request=request, view=self)
            print(course_list)
            serializer = CourseSerializer(course_list, many=True)
            # serializer.data OrderedDict有序字典列表
            print(serializer.data)
            response.data = serializer.data
            print()
        except Exception as e:
            response.code = 0
            response.error = '获取数据失败'
        return Response(response.dict)  # vars(object)
        # return p.get_paginated_response(response.dict)




class CourseDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_object = Course.objects.get(id=pk)

            if request.query_params.get('question'):
                print(request.query_params)
                # 课程常见问题http://127.0.0.1:8008/api/v2/course/1/?question=1
                serializer = CourseQuestionSerializer(course_object)
            elif request.query_params.get('outline'):
                # 课程大纲http://127.0.0.1:8008/api/v2/course/1/?outline=1
                serializer = CourseOutlineSerializer(course_object.coursedetail.courseoutline_set, many=True)
            else:
                # 课程详细http://127.0.0.1:8008/api/v2/course/1/
                serializer = CourseDetailSerializer(course_object)
            ret.data = serializer.data
        except Exception as e:
            ret.code = 0
            ret.error = '获取数据失败'
            raise
        return Response(ret.dict)


class DegreeCourseView(APIView):
    versioning_class = CourseVersioning
    def get(self, request, version):
        ret = BaseResponse()
        try:
            queryset = DegreeCourse.objects.all()
            serializer = DegreeCourseSerializer(queryset, many=True)
            ret.data = serializer.data
        except Exception as e:
            print(e)
            ret.data = 0
            ret.error = '获取数据失败'
        return Response(ret.dict)


class DegreeCourseDetailView(APIView):
    versioning_class = CourseVersioning
    def get(self, request, pk, *args, **kwargs):  # version关键字参数
        degreecourse = DegreeCourse.objects.get(pk=pk)
        serializer = DegreeCourseDetailSerializer(degreecourse)
        return Response(serializer.data)



