from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms

from app01.utils.bootstrap import BootstrapModelForm, BootstrapForm
from app01.models import UserInfo, Mobile_Num, Admin
from app01.utils.encrypt import md5


class UserModelForm(BootstrapModelForm):
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = UserInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']


class MobileModelForm(BootstrapModelForm):
    # 添加校验规则
    # 验证：方式1
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'1[3-9]\d{9}$', '手机号格式错误')],
    )

    class Meta:
        model = Mobile_Num
        fields = ['mobile', 'price', 'level', 'status']
        # fields = '__all__'  # 所有的字段
        # exclude = ['level']  # 排除某个字段

    # 验证：方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = Mobile_Num.objects.filter(mobile=txt_mobile).exists()
        if exists:
            # 验证不通过
            raise ValidationError('手机号已存在')
        # 验证通过
        return txt_mobile


class MobileEditModelForm(BootstrapModelForm):
    # 添加校验规则
    # 手机号input框  禁止使用
    # mobile = forms.CharField(disabled=True, label='手机号')
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = Mobile_Num
        fields = ['mobile', 'price', 'level', 'status']
        # fields = '__all__'  # 所有的字段
        # exclude = ['level']  # 排除某个字段

    # 验证：方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        print(self.instance.pk)
        exists = Mobile_Num.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()

        if exists:
            raise ValidationError('手机号重复')
        return txt_mobile


class AdminModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = Admin
        # fields = ['username', 'password', 'confirm_password']
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def clean_username(self):
        txt_username = self.cleaned_data['username']
        exists = Admin.objects.filter(username=txt_username).exists()
        if exists:
            raise ValidationError('用户名已存在')

        return txt_username

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data['password']
        confirm = md5(self.cleaned_data['confirm_password'])
        if pwd != confirm:
            raise ValidationError('密码输入不一致，请重新输入')

        return confirm


class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = Admin
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data['username']
        exists = Admin.objects.exclude(id=self.instance.pk).filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return username


class AdminResetModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label='重置密码',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Admin
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)
        exists = Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError('新密码不能与原密码相同')
        return md5_pwd

    def clean_confirm_password(self):
        # pwd = self.cleaned_data['password']
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm:
            raise ValidationError('密码输入不一致，请重新输入')

        return confirm


class LoginForm(BootstrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput
    )

    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput
    )

    image_code = forms.CharField(
        label='验证码',
        widget=forms.TextInput
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

