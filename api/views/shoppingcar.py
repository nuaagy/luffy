import redis
import sys
import json

from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.response import Response

from api.models import Course
from api.utils.response import BaseResponse

USER_ID = 1

CONN = redis.Redis(host='192.168.11.169', port=6379)


class ShoppingCarView(ViewSetMixin, APIView):
    """JSON格式"""
    parser_classes = (JSONParser, FormParser)

    def list(self, request, *args, **kwargs):
        ret = {'code': 10000, 'data': None, 'error': ''}
        try:
            shopping_car_course_list = []
            pattern = 'shopping_car_%s*' % USER_ID
            keys = CONN.keys(pattern)
            for key in keys:
                course = {
                    'id': CONN.hget(key, 'id'),
                    'name': CONN.hget(key, 'name'),
                    'img': CONN.hget(key, 'img'),
                    'selected_price_id': CONN.hget(key, 'selected_price_id'),
                    'price_policy_dict': json.loads(CONN.hget(key, 'price_policy_dict').decode('utf-8'))
                }
                print(course)
                shopping_car_course_list.append(course)
                ret['data'] = shopping_car_course_list
        except Exception as e:
            print(e, file=sys.stderr)
            ret['code'] = 10005
            ret['error'] = '获取购物车数据失败'

        return Response(ret)

    def create(self, request, *args, **kwargs):
        """ {"courseid": 1, "policyid": 2}
        """

        courseid = request.data.get('courseid')
        policyid = request.data.get('policyid')

        # 判断课程ID合法性
        #   - 判断价格策略有效
        course = Course.objects.filter(pk=courseid).first()
        if not course:
            return Response({'code': 10001, 'data': '无效的课程'})

        price_policy_queryset = list(course.price_policy.all())
        price_policy_dict = dict()
        for policy in price_policy_queryset:
            temp = {
                'id': policy.id,
                'valid_period': policy.valid_period,
                'price': policy.price,
                'valid_period_display': policy.get_valid_period_display()
            }
            price_policy_dict[policy.id] = temp

        if policyid not in price_policy_dict:
            return Response({'code': 10005, 'data': '价格策略无效'})

        # 添加购物车 课程ID 课程名称 课程所有价格策略 选择价格策略 课程img
        pattern = 'shopping_car_%s*' % USER_ID

        # 购物车数量限制?
        # length = len(CONN.keys(pattern))
        # print(CONN.keys(pattern))
        # if length >= 3:
        #     return Response({'code': 10009, 'error': '购物车无法继续添加商品'})

        key = 'shopping_car_%s_%s' % (USER_ID, courseid)
        CONN.hset(key, 'id', courseid)
        CONN.hset(key, 'name', course.name)
        CONN.hset(key, 'price_policy_dict', json.dumps(price_policy_dict))
        CONN.hset(key, 'img', course.course_img)
        CONN.hset(key, 'selected_price_id', policyid)

        # 过期移除商品
        # CONN.expire(key, 20 * 60)  # 写入配置文件
        return Response({'code': 10000, 'data': '购买成功'})

    def destroy(self, request, courseid, *args, **kwargs):
        response = BaseResponse()
        try:
            key = 'shopping_car_%s_%s' % (USER_ID, courseid)
            print(CONN.exists(key))
            print(CONN.keys())
            if not CONN.exists(key):
                response.code = 10008
                response.error = '商品不存在无法删除'
                return Response(response.dict)
            CONN.delete(key)
            response.data = '删除成功'
        except Exception as e:
            response.code = 10006
            response.error = '删除失败'
        return Response(response.dict)

    def update(self, request, *args, **kwargs):
        response = BaseResponse()
        try:
            courseid = request.data.get('courseid')
            price = request.data.get('policyid')
            policyid = str(price) if price else None
            key = 'shopping_car_%s_%s' % (USER_ID, courseid)
            if not CONN.exists(key):
                response.code = 10003
                response.error = '要修改的课程不存在'
                return Response(response.dict)
            print(CONN.hget(key, "price_policy_dict"))
            price_policy_dict = json.loads(CONN.hget(key, "price_policy_dict"))  # 3.6支持bytes反序列化

            if policyid not in price_policy_dict:
                response.code = 10004
                response.error = '价格策略不存在'
                return Response(response.dict)

            CONN.hset(key, 'selected_price_id', policyid)
            response.code = 10000
            response.data = '修改商品信息成功'
        except Exception as e:
            print(e)
            response.code = 100010
            response.error = '修改商品数据失败'

        return Response(response.dict)