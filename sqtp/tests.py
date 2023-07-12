from django.db.models import Value
from django.test import TestCase

# Create your tests here.

# 单元测试
from sqtp.models import Case,Config,Step,Request

class TestRelatedQuery(TestCase):
    # 创建数据源
    def setUp(self) -> None:
        config1 = Config.objects.create(name='case001', baseurl='http://localhost')
        config2 = Config.objects.create(name='case002', baseurl='http://localhost')
        self.case1 = Case.objects.create(config=config1)
        self.case2 = Case.objects.create(config=config2)


    def test_steps_query(self):
        step1 = Step.objects.create(belong_case=self.case1)
        step2 = Step.objects.create(belong_case=self.case2)
        step1.linked_case = self.case2
        step1.save()
        # 正向查询
        print('======================正向查询start query===============================')
        print(step1.belong_case)
        print(step2.belong_case)

        # 反向查询
        print('===========================反向查询==============================================')
        # print(self.case1.step_set.all())
        print(self.case1.teststeps.all())
        print(self.case2.linked_steps.all())


class TestJsonField(TestCase):
    def setUp(self) -> None:
        req1 = Request.objects.create(method=1,url='/Mgr/course/',data={"name":"小明","age":16,"address":"nanjing"})

    def test_json01(self):
        req = Request.objects.all().first()
        print(req)
        # 测试修改--整体
        req.data={"name":"小强","age":18,"address":"shanghai","school":{"name":"北大","level":"top1"}}
        req.save()
        print(Request.objects.all().first().data) # 查看修改后的内容

        # 修改局部
        req=Request.objects.all().first()
        print(req.data['name']) # 修改前
        req.data['name'] = '星辰大海'
        req.save()
        print(Request.objects.all().first().data['name']) # 修改后
        # 过滤
        print('#######################过滤###########################')
        # 忽略大小写的精确匹配
        print(Request.objects.filter(url__iexact='/mgr/course/'))


        # json删除操作
        # 删除整体
        # req.data=Value('null')  #设置成json的null
        # # req.data=None            设置成sql的null
        # req.save()
        # print(Request.objects.all().first().data)

        # # 删除局部
        req.data.pop('name')
        req.save()
        print(Request.objects.all().first().data)
        #
        # # 条件查询--根据json字段的某个值来查询，json字段__嵌套字段
        res=Request.objects.filter(data__age=18)
        res=Request.objects.filter(data__school__name="北大")
        print('======json条件查询=====')
        print(res)



#字段条件查询
class TestFieldQuery(TestCase):
    def setUp(self) -> None:
        req1 = Request.objects.create(method=1,url='/mgr/course/',data={"name":"小明","age":16,"address":"nanjing"})
        req2 = Request.objects.create(method=1,url='/mgr/teacher/',data={"name":"小刚","age":18,"address":"beijing"})
        req3 = Request.objects.create(method=1,url='/mgr/course/',data={"name":"小明","age":16,"address":"nanjing"})

    def test_iquery(self):
        req = Request.objects.all().first()
        print(req)
        # 测试修改--整体
        print('************************************')
        # 字段条件查询的语法是:字段__条件名
        # print(Request.objects.filter(url__iexact='/MGR/course/'))
        # 包含模式
        # print(Request.objects.filter(url__contains='course/'))
        print('#######################测试##############################')
        print(Request.objects.filter(data__name='小刚'))



    def test_in_query(self):
        # in就是存在，然后就把结果返回，精确的查询
        print(Request.objects.filter(url__in=['/mgr/course/','/mgr/teacher/']))


#跨关系查询
class TestOverRelations(TestCase):
    def setUp(self) -> None:
        # 创建用例
        config1 = Config.objects.create(name='case001',baseurl='http://localhost')
        config2 = Config.objects.create(name='case002',baseurl='http://localhost')
        self.case1 = Case.objects.create(config=config1)
        self.case2 = Case.objects.create(config=config2)

    def test_step_request(self):
        # 准备测试数据 步骤和请求
        step1 = Step.objects.create(belong_case=self.case1,name='step1')
        step2= Step.objects.create(belong_case=self.case1,name='step2')
        step3 = Step.objects.create(belong_case=self.case2,name='step3')
        step4 = Step.objects.create(belong_case=self.case2,name='step4')

        req1 = Request.objects.create(method=1,url='/mgr/teacher1/',data={"name":"小刚","age":18,"address":"beijing"},step=step1)
        req2 = Request.objects.create(method=2,url='/mgr/teacher2/',data={"name":"小刚","age":18,"address":"beijing"},step=step2)
        req3 = Request.objects.create(method=3,url='/mgr/teacher3/',data={"name":"小刚","age":18,"address":"beijing"},step=step3)
        req4 = Request.objects.create(method=1,url='/mgr/teacher4/',data={"name":"小刚","age":18,"address":"beijing"},step=step4)

        print(req1.step.belong_case) #链式语法
        # 跨关系查询的语法: 字段__关联字段
        # print(Request.objects.filter(step__belong_case=self.case2))
        print(Request.objects.filter(step__belong_case__config__name='case001').filter(url__contains='teacher2'))

