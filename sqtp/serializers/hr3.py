# -*- coding:utf-8 -*-
""""
============================
Time : 2022/9/13 0:07
Author : 王新科
File : hr3.py
software : PyCharm
============================
"""

from rest_framework import serializers
from sqtp.models import Step, Request, Case, Config, Project
from sqtp.serializers import UserSerializer

from .mgr import ProjectSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer

# 自定义的函数，过滤参数
from sqtp.utils import filter_data


# 请求
class RequestSerializer(serializers.ModelSerializer):
    method = serializers.SerializerMethodField()  # 声明字段通过该字段通过get_method_display方法获取
    # 框架会自动的把method给注入到方法中
    # 对于每个具有choices 的字段，每个对象将具有一个get_xx_display() 方法，其中xx 为该字段的名称。 这个方法返回该字段对“人类可读”的值。
    step_id = serializers.IntegerField(write_only=True, required=False)  # write_only只作为入参数,非必填写的入参数

    def get_method(self, obj):
        return obj.get_method_display()

    # 元类
    class Meta:
        model = Request  # 指定序列器对应的模型
        fields = ['step_id', 'method', 'url', 'params', 'headers', 'json', 'data']  # 指定序列化模型中的字段
        # fields = '__all__' # 序列化所有字段，起显示作用

    def validate(self, attrs):
        template = {
            'params': dict,
            'headers': dict,
            'cookies': dict,
        }
        for param_name, type_name in template.items():
            if param_name in attrs and not isinstance(attrs[param_name], type_name):
                # 数据类型校验
                raise ValidationError(f'请传递正确的{param_name}格式: {type_name}')
        return attrs


class ConfigSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(required=False, read_only=True)  # read_only=True 只作为入参 ,说白了就是嵌套的字段

    class Meta:
        model = Config
        fields = ['project', 'name', 'base_url', 'variables', 'parameters', 'parameters', 'verify', 'export']

    # # 自定义校验器
    # def validate(self, attrs):
    #     if 'variables' in attrs and not isinstance(attrs['variables'],dict):
    #         # type check类型的判断 传参数校验
    #         raise ValidationError('please send right type variables: dict')
    #     if 'parameters' in attrs and not isinstance(attrs['parameters'],dict):
    #         # type check类型的判端 传参数校验
    #         raise ValidationError('please send right type parameters: dict')
    #     if 'export' in attrs and not isinstance(attrs['export'],dict):
    #         # type check类型的判端 传参数校验
    #         raise ValidationError('please send right type export: dict')

    # 自定义校验器
    def validate(self, attrs):
        template = {
            'variables': dict,
            'parameters': dict,
            'export': list
        }
        for param_name, type_name in template.items():
            if param_name in attrs and not isinstance(attrs[param_name], type_name):
                # 数据类型校验
                raise ValidationError(f'请传递正确的{param_name}格式: {type_name}')
        # 再加入base_url格式检测--是否以http://或https://开头
        return attrs


class StepSerializer(serializers.ModelSerializer):
    request = RequestSerializer()
    belong_case_id = serializers.IntegerField(required=False)  # write_only-- 只写入不显示,只进不出参

    class Meta:
        model = Step
        fields = ['name', 'variables', 'request', 'extract', 'validate', 'setup_hooks', 'teardown_hooks',
                  'belong_case_id', 'sorted_no']
        # fields = '__all__'

    def validate(self, attrs):
        template = {
            'variables': dict,
            'request': dict,
            'extract': dict,
            'validate': list,
            'setup_hooks': list,
            'teardown_hooks': list,
        }
        for param_name, type_name in template.items():
            if param_name in attrs and not isinstance(attrs[param_name], type_name):
                # 数据类型校验
                raise ValidationError(f'请传递正确的{param_name}格式: {type_name}')
        return attrs

    def create(self, validated_data):
        req_kws = validated_data.pop('request')
        # 构造步骤
        step_obj = Step.objects.create(**validated_data)
        # 构造请求
        req_kws['step_id'] = step_obj.id
        req_serializer = RequestSerializer(data=req_kws)
        if req_serializer.is_valid(raise_exception=True):
            req_obj = req_serializer.save()
        # else:
        #     raise ValidationError(req_serializer.errors)
        # step_obj = Step.objects.create(request=req_obj, **validated_data) # 这里我不明白
        return step_obj


# 测试用例
class CaseSerializer(serializers.ModelSerializer):
    config = ConfigSerializer()  # config字段就对应其序列化器返回的内容，case模型类中包含config字段。
    # 所以需要指定一下  之前是config = 1,现在是展示所有的config的内容,说白了就是在校验前新增了一个字段

    teststeps = StepSerializer(required=False, many=True)  # # read_only=True为只读参数，required=False 表示非必填，就不会校验入参，作为输出参数
    # many=True展示为列表形式, 如果不加的话teststeps默认返回字典
    # 这边需要在case的详情页中显示步骤。所以我直接在序列化器中先传过来了

    project_id = serializers.CharField(write_only=True, required=False)  # 只做为入参
    create_by = UserSerializer(write_only=True, required=False)
    updated_by = UserSerializer(write_only=True, required=False)

    class Meta:
        model = Case  # 指定序列器对应的模型 ;   case包含config字段。所以需要指定一下
        # fields = '__all__' # 序列化所有字段，也就是显示字段
        fields = ['config', 'teststeps', 'project_id', 'desc', 'id', 'file_path', 'create_time',
                  'update_time', 'create_by', 'updated_by']  # # 序列化所有字段，起显示作用,就接口返回显示  ##序列化器定义的字段必须再此展示

    def validate(self, attrs):
        template = {
            'config': dict,
            'teststeps': list,
        }
        for param_name, type_name in template.items():
            if param_name in attrs and not isinstance(attrs[param_name], type_name):
                # 数据类型校验
                raise ValidationError(f'请传递正确的{param_name}格式: {type_name}')
        return attrs

    # 覆盖父类新增的方法
    def create(self, validated_data):
        '''
        解释器旁边的箭头表示重写父类的方法

        validated_data 为检验后的入参,字典的形式
        '''
        # 创建config
        config_kws = validated_data.pop('config')  # 取出config参数,就是删除cofing
        project = Project.objects.get(pk=validated_data.pop('project_id'))
        config = Config.objects.create(project=project, **config_kws)  # 关联project

        # 取步骤数据
        step_kws = []
        if 'teststeps' in validated_data:
            step_kws = validated_data.pop('teststeps')

        # 创建用例
        file_path = f'{project.name}_{config.name}.json'  # 项目名+用例名.json
        case = Case.objects.create(config=config, file_path=file_path, **validated_data)
        # 创建步骤
        if step_kws:
            for step_kw in step_kws:
                step_kw['belong_case_id'] = case.id
                serializer = StepSerializer(data=step_kw)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

        return case

    # 修改用例
    def update(self, instance, validated_data):
        '''
        instance 当前被修改的数据对象
        validated_data 校验后的入参--字典形式
        '''
        config_kws = validated_data.pop('config')  # config入参
        project = Project.objects.get(pk=validated_data.pop('project_id'))
        # 把project数据传递到config入参中
        config_kws['project'] = project.id
        conf_serializer = ConfigSerializer(instance=instance.config, data=config_kws)
        # 通过序列化器更新数据
        if conf_serializer.is_valid():
            conf_serializer.save()  # 调用save方法之前必须调用检查参数动作
        else:
            raise ValidationError(conf_serializer.errors)  # 发生错误后，信息保存在序列化器的error字段中
        # 更新case数据
        # instance.file_path = validated_data['file_path']
        # instance.desc = validated_data['desc']

        # teststeps更新
        # 先删除当前用例下关联的所有step

        # 我知道了case我反向查询关联我的步骤
        step_qs = instance.teststeps.all()  # 获取到步骤的数据
        for step in step_qs:
            step.delete()  # 逐个删除

        # 重新创建
        teststeps = validated_data.pop('teststeps')
        for step in teststeps:
            # 取出步骤关联的用例ID
            step['belong_case'] = self.instance.id
            ss = StepSerializer(data=step)
            if ss.is_valid():
                ss.save()
            else:
                raise ValidationError(ss.errors)
        # 利用python反射自动赋值
        for k, v in validated_data.items():
            # 注意validated_data不要包含instance数据对象没有的字段参数
            setattr(instance, k, v)
            # 保存到数据库
        instance.save()
        return instance

    # 生成hr3 格式的json文件

    def to_json_file(self, path=None):
        if path is None:
            path = self.instance.file_path  # 如果没传就采用用例自己的文件路径
        if not path.endswith('json'):
            path = path + 'json'

        # 生成的用例文件放在项目目录的testcase目录下
        path = f'testcase/{path}'

        # 过滤输出参数  self.data前端输入的参数
        valid_data = filter_data(self.data)

        # 生成json文件
        # content = JSONRenderer().render(valid_data,accepted_media_type='application/json; indent=4') # 当前序列化的对象self.data ；获取文件内容 --bytes
        content = JSONRenderer().render(valid_data, accepted_media_type='application/json; indent=4')  # 获取文件内容--bytes
        print(content)
        # accepted_media_type接收的类型

        with open(path, 'wb') as f:
            f.write(content)
        return path
