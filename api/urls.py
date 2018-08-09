from django.conf.urls import url

from api.views.course import CourseView, CourseDetailView, \
    DegreeCourseView, DegreeCourseDetailView

from api.views.shoppingcar import ShoppingCarView

urlpatterns = [
    url(r'^course/$', CourseView.as_view(), name='course'),
    url(r'^course/(?P<pk>\d+)/$', CourseDetailView.as_view()),
    # 学位课
    url(r'^degreecourse/$', DegreeCourseView.as_view()),
    # 学位课详情
    url(r'^degreecourse/(?P<pk>\d+)/$', DegreeCourseDetailView.as_view()),

    url(r"^shoppingcar/$", ShoppingCarView.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
    })),
    url(r"^shoppingcar/(?P<courseid>\d+)/$", ShoppingCarView.as_view({
        # 'get': 'retrieve',
        # 'put': 'update',
        'delete': 'destroy'
    })),
]
