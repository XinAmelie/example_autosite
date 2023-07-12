# # -*- coding:utf-8 -*-
# """"
# ============================
# Time : 2022/9/2 12:10
# Author : 王新科
# File : serializers.py 序列化
# software : PyCharm
# ============================
# """
# from rest_framework import serializers
# from sqtp.models import Step,Request,Case,Config,Project,Environment,User
# from rest_framework.exceptions import ValidationError
# from django.contrib import auth
#
#
# # 序列化狭义的理解为转换 序列化后端 从数据库 -- 模型 -- json
# # 反序列化  前端  json -- 模型 --> 从数据库
# # # 序列化器是针对数据模型，一个序列化器对应一个模型
#
# # 命名规则 模型名+serializer
# # class RequestSerializer(serializers.Serializer):
# #     method_choices = (  # method可选的字段，
# #         (0, 'GET'),  # 参数1:实际存储在数据库中的值, 参数2：对外显示的值
# #         (1, 'POST'),
# #         (2, 'PUT'),
# #         (3, 'DELETE')
# #     )
# #     # serializers的RelatedField关系字段 queryset查询集
# #     step = serializers.RelatedField(queryset=Step.objects.all(),allow_null=True)
# #     method = serializers.ChoiceField(choices=method_choices, default=0)
# #     url = serializers.CharField()
# #     params = serializers.JSONField(allow_null=True)
# #     headers = serializers.JSONField( allow_null=True)
# #     cookies = serializers.JSONField( allow_null=True)
# #     data = serializers.JSONField( allow_null=True)
# #     json = serializers.JSONField( allow_null=True)
# #
# #
# #     # 确定数据类型,框架调用序列化去创建序列化的数据，再经过校验器校验之后，传到validated_data中
# #     # 重写创建和修改方法
# #     def create(self, validated_data):
# #         '''
# #             validated_data：经过校验之后的数据，字典类型
# #         '''
# #         return Request.objects.create(**validated_data) # 字典解包   相当于: name=xx,age=yyy
# #
# #
# #
# #     def update(self, instance, validated_data):
# #         '''
# #             instance:被修改的数据对象、实例
# #             validated_data：经过校验之后的数据，字典类型
# #         '''
# #
# #         # get可以指定默认返回值 get('',default=)
# #         instance.step = validated_data.get('step',instance.step)
# #         instance.method = validated_data.get('step',instance.method)
# #         instance.url = validated_data.get('step',instance.url)
# #         instance.params = validated_data.get('step',instance.params)
# #         instance.headers = validated_data.get('step',instance.headers)
# #         instance.cookies = validated_data.get('step', instance.cookies)
# #         instance.data = validated_data.get('step',instance.data)
# #         instance.json = validated_data.get('step',instance.json)
#
#
# # 请求
# class RequestSerializer(serializers.ModelSerializer):
#     method = serializers.SerializerMethodField()  # 声明字段通过该字段通过get_method_display方法获取
#     # 框架会自动的把method给注入到方法中
#     def get_method(self,method):
#         return method.get_method_display()
#     # 元类
#     class Meta:
#         model = Request # 指定序列器对应的模型
#         # fields = ['step','method','url','params','headers'] # 指定序列化模型中的字段
#         fields = '__all__' # 序列化所有字段
#
#
# class ConfigSerializer(serializers.ModelSerializer):
#     project = ProjectSerializer()
#     class Meta:
#         model = Config
#         fields = '__all__'
#
#
# class StepSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Step
#         fields = '__all__'
#
# # 测试用例
# class CaseSerializer(serializers.ModelSerializer):
#     config = ConfigSerializer() # config字段就对应其序列化器返回的内容，case模型类中包含config字段。所以需要指定一下  之前是config = 1,现在是展示所有的config的内容
#     teststeps  = StepSerializer(read_only=True) # # read_only=True为只读参数，required=False 表示非必填，就不会校验入参
#                                                     # many=True展示为列表形式, 如果不加的话teststeps默认返回字典
#                                                     # 这边需要在case的详情页中显示步骤。所以我直接在序列化器中先传过来了
#     class Meta:
#         model = Case                 # 指定序列器对应的模型 ;   case包含config字段。所以需要指定一下
#
#         # fields = ['step','method','url','params','headers'] # 指定序列化模型中的字段
#
#         # fields = '__all__' # 序列化所有字段，也就是显示字段
#         fields = ['config','teststeps']
#
#
#
#
# # 项目
# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ['id', 'admin', 'name', 'status', 'version', 'desc'] # 指定序列化模型中的字段
#         # fields = '__all__'
#
#
# # 环境
# class EnvironmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Environment
#         fields = '__all__'
#
#
# from django.conf import settings
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'   # __all__全部校验
#
#
# # 注册序列化器
# class RegisterSerializer(serializers.ModelSerializer):
#     # 因为数据库没有admin_code,所以我们要显性的校验。就是声明一个
#     admin_code = serializers.CharField(default='')
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'email', 'phone', 'realname', 'admin_code'] # 选择性的进行校验
#
#     # 手写校验器，入参是否合法;自定义校验规则    is_valid（）是序列化器自带的校验
#     def validate(self, attrs): # attrs为入参数的字典形式。是序列化器进行序列化之后的值，被转化为字典
#         # 检验admin_code是否正确
#         # get方法
#         #	key: 要设置默认值的Key
#         #	default: 要返回key的值，可以是任何值，如整形、字符串、列表、字典等
#         #	return: 如果字典中key本来有值，那么返回的是字典中Key所对应的值，如果没有，那么返回“default”中的值。
#         # 程序走到这里发现，get的结果什么都没有。就代表不执行
#         if attrs.get('admin_code') and attrs['admin_code'] !='sqtp':
#             raise ValidationError('错误的admin code')
#         return attrs # 返回校验之后的入参，我后期需要新建数据
#
#     # 注册用户，相当于创建用户数据,我把他写到序列器中了。无所谓
#     def register(self):
#         # 获取入参数 此时的data是rf框架 data 代表校验之后的数据_validated_dat，框架会自己传attrs
#         in_param = self.data
#         if 'admin_code' in in_param: # 创建管理员
#             in_param.pop('admin_code') # 用户表无admin_code的字段，硬传会报错
#             user=User.objects.create_superuser(**in_param)  # 继承的是AbstractUser，父类有方法创建
#         else:
#             user=User.objects.create_user(**in_param) # 创建普通
#         return user
#
# # 登录序列化器
# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#
#     def validate(self, attrs):
#         # 验证用户名和密码
#         user = auth.authenticate(**attrs)
#         if not user:
#             raise ValidationError('用户名或密码错误')   # ValidationError报的错误会储存在serializer.errors中
#         return user #已有的数据
#
#
#
#
#
