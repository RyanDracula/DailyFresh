# coding=utf-8
from django.http import HttpRequest,HttpResponse
from django.middleware.csrf import CsrfViewMiddleware


class my_mid():
    def process_response(self, request, response):
        url_list = [
            '/user/register.html/',
            '/user/login.html/',
            '/user/register_handle/',
            '/user/handle_register/',
            '/user/go_login/',
            '/user/logout/'
        ]
        if not request.is_ajax() and request.path not in url_list:
            response.set_cookie('url', request.get_full_path())
        return response
