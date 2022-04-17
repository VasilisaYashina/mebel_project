import datetime

from pony.orm import *


# Тут нужно проверить пароль на корректонос
def check_password(pwd):
    return bool(pwd)


db = Database()

db.bind(provider='mysql', host='127.0.0.1', user='simple', passwd='simple', db='simple',
        charset='utf8mb4')


class Users(db.Entity):
    id = PrimaryKey(int, auto=True)
    login = Required(str)
    nick = Optional(str)
    password = Optional(str)


@db_session
def auth(_login, _password):
    if Users.exists(login=_login):
        c = Users.get(login=_login)
        if _password == c.password:
            return dict({"status": "ok", "user_id": c.id})
        else:
            return dict({"status": "pass"})
    return dict({"status": "not_found"})


@db_session
def register(_login, _password, _nick):
    errors = []
    if Users.exists(login=_login):
        errors.append("login_taked")
    if Users.exists(nick=_nick):
        errors.append("nick_taked")
    if not check_password(_password):
        errors.append("pass_incorrect")
    if len(errors) == 0:
        p = Users(login=u"" + _login, nick=u"" + _nick, password=u"" + _password)
        commit()
        return dict({"status": "ok", "user_id": p.id})


class Comment(db.Entity):
    id = PrimaryKey(int, auto=True)
    user_id = Required(int)
    date_push = Required(datetime.datetime)
    content = Required(str)


@db_session
def send_comment(u_i, c):
    o = Comment(user_id=u_i, date_push=datetime.datetime.now(), content=u"" + str(c))
    commit()
    return dict({"status": "ok", "comment_id": o.id})


@db_session
def list_comments():
    c = Comment.select(lambda l: l.id > 0)[:]
    return c


db.generate_mapping()
