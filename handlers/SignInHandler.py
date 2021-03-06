# coding=utf-8


import tornado.web
from handlers.base import BaseHandler
from common.pagination import Pagination
from settings import BASE_URL


class SignInHandler(BaseHandler):
    def get(self):
        if self.current_user:
            return self.redirect("/index")
        next_url = self.get_argument("next", "")
        self.render("login.html", next_url=next_url)

    def post(self):
        user_name = self.get_argument("email", None)
        password = self.get_argument("password", None)
        next_url = self.get_argument("next", "/")
        user = self.datastore.check_user(user_name, password)
        if not user:
            return self.render("login.html", error=u'用户名或密码错误', next_url=next_url)
        self.set_current_user(user.user_name, user.id, 1)
        if next_url:
            return self.redirect(next_url)
        return self.redirect("/index")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('app_qr_code')
        return self.redirect('/')


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        page = int(self.get_argument("page", 1))
        if page < 1:
            page = 1
        count = int(self.get_argument("count", 10))
        total_count = self.datastore.get_qr_count()
        qrs = self.datastore.get_qr(page, count)
        menu = self.active_menu("QrManage")
        pagination = Pagination(page, count, total_count)
        return self.render("index_demo.html", menu=menu, pagination=pagination, qrs=qrs, base_url=BASE_URL)


class RedictHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        return self.redirect("/index")

class TestHandler(BaseHandler):
    def get(self):
        return self.render("test.html")
