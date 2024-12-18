import random
from django.core.cache import cache  # 使用缓存
from django.core.mail import send_mail
from django.conf import settings

def generate_verification_code():
    return str(random.randint(100000, 999999))  # 生成6位验证码


def save_verification_code(email, code):
    cache.set(f'verification_code_{email}', code, timeout=300)  # 过期时间5分钟


def send_verification_email(email):
    code = generate_verification_code()
    save_verification_code(email, code)
    subject = "CloseBI邮箱验证"
    message = f"尊敬的用户您好：您正在进行CloseBI邮箱验证，本次验证码为：{code}，请在5分钟内进行使用。如非本人操作，请忽略此邮件，由此给您带来的不便请谅解！"
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])


def verify_code(email, code):

    # 从缓存中获取验证码
    stored_code = cache.get(f'verification_code_{email}')

    if stored_code is None:
        return False

    if code == stored_code:
        # 验证通过后可以删除验证码，防止重复使用
        cache.delete(f'verification_code_{email}')
        return True
    else:
        return False