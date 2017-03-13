# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

from .forms import LoginForm, LoginClientForm

urlpatterns = patterns('',

    #login
    url(r'^auth/$', auth_views.login, {'template_name': 'signup/login.html',
                                       'authentication_form': LoginForm}, name='url_login_auth'),

    #login
    url(r'^clientauth/$', auth_views.login, {'template_name': 'signup/login.html',
                                       'authentication_form': LoginClientForm}, name='url_client_login_auth'),    

    #logout
    url(r'^logout/$', auth_views.logout,
                {'template_name': 'signup/logout.html'}, name='auth_logout'),

    url(r'', include('django.contrib.auth.urls')),    

    url(r'^password/reset/$', auth_views.password_reset,
            {'template_name': 'signup/password_reset_form.html'}, name='url_login_password_reset'),

    url(r'^password/reset/done/$', auth_views.password_reset_done,
                {'template_name': 'signup/password_reset_done.html'}, name='password_reset_done'),

    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, 
                {'template_name': 'signup/password_reset_confirm.html'}, name='auth_password_reset_confirm'),

    url(r'^password/reset/complete/$', auth_views.password_reset_complete,
                {'template_name': 'signup/password_reset_complete.html'}, name='auth_password_reset_complete'),

)
