import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import UserModel, EmailCaptchaModel
from exts import db


# Form: 验证用户提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误')])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message='验证码长度错误')])
    username = wtforms.StringField(validators=[Length(min=3, max=10, message='用户名长度错误')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码长度错误')])
    password_confirm = wtforms.StringField(validators=[EqualTo('password', message='两次密码不一致')])

    # 自定义验证
    # 1.邮箱是否已经被注册
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError('该邮箱已被注册')

    # 2.验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError('验证码错误')


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码长度错误')])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=20, message='标题长度错误')])
    content = wtforms.StringField(validators=[Length(min=3, message='内容长度错误')])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3, message='内容长度错误')])
    question_id = wtforms.IntegerField(validators=[wtforms.validators.DataRequired(message='问题id不能为空')])