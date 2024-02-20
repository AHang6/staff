from django.db import models


# Create your models here.

class Admin(models.Model):
    """  管理员  """
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)

    def __str__(self):
        return self.username


class Department(models.Model):
    """ 部门表  """
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """  员工表  """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=8, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职日期")

    # 无约束
    # depart_id = models.IntegerField(verbose_name="部门标号")

    # 1、有约束 [外键]
    #    - to, 与那张表关联
    #    - to_files, 表中的那一列关联
    # 2、django自动
    #    - 写的depart
    #    - 生成数据列  depart_id  [结尾自动拼接  _id]
    # 3、部门表被删除
    # ### 3.1 级联删除 ###
    depart = models.ForeignKey(verbose_name="部门编号", to="Department", to_field="id", on_delete=models.CASCADE)
    # ### 3.2 置空    ###
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    gender_choices = (
        (1, "男"),
        (2, "女"),
    )

    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class Task(models.Model):
    """   任务   """
    level_choices = (
        (1, '紧急'),
        (2, '重要'),
        (3, '临时'),
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)
    title = models.CharField(verbose_name='标题', max_length=64)
    detail = models.TextField(verbose_name='详细信息')

    user = models.ForeignKey(verbose_name='负责人', to="Admin", to_field='id', on_delete=models.CASCADE)


class Mobile_Num(models.Model):
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2)

    level_choices = (
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
        (4, '四级'),
        (5, '五级'),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices)

    status_choices = (
        (1, '已占用'),
        (2, '未占用'),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices)


class Order(models.Model):
    oid = models.CharField(verbose_name='订单号', max_length=64)
    title = models.CharField(verbose_name='商品名称', max_length=32)
    price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2)

    status_choices = (
        (1, '待支付'),
        (2, '已支付'),
    )

    status = models.SmallIntegerField(verbose_name='状态', default=1, choices=status_choices)
    user = models.ForeignKey(verbose_name='管理员', to="Admin", on_delete=models.CASCADE)


class City(models.Model):
    title = models.CharField(verbose_name='用户名', max_length=32)
    count = models.IntegerField(verbose_name='人口')
    img = models.FileField(verbose_name='LOGO', max_length=128, upload_to='city/')


