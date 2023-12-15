from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel, db, UserModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print('该邮箱未注册')
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password, password):
                # cookie中不适合存储太多的数据，只适合存储少量的数据，比如用户id
                # session: 服务器存储用户数据的地方
                # flask中的session，是经过加密后存储在cookie中的
                session['user_id'] = user.id
                return redirect('/')
            else:
                print('密码错误')
                return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))


# GET: 从服务器获取数据
# POST: 向服务器提交数据
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 验证用户提交的数据
        # 表单验证：flask-wtf：wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.register'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@bp.route('/captcha/email', methods=['GET'])
def get_email_captcha():
    # /captcha/email/<email>
    # /captcha/email?email=xxx@xx.com
    email = request.args.get('email')
    # 4/6位随机数
    source = string.digits * 4
    captcha = random.sample(source, 4)
    captcha = ''.join(captcha)
    # I/O操作 Input/Output
    msg = Message(subject='KMZ问答注册验证码', recipients=[email], body=f'您的验证码为{captcha}，请在5分钟内完成注册。')
    mail.send(msg)
    # memcache/redis
    # 用数据库表的方式存储
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({'code':200, 'msg': '', 'data': None})


@bp.route('/mail/test')
def mail_test():
    msg = Message(subject='test', recipients=['qq1318342521@126.com'], body='test')
    mail.send(msg)
    return 'success'