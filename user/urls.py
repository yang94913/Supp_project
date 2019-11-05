"""Supp_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# admin: (user:admin, password:admin123)
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from Supp_project.settings import MEDIA_ROOT
from user import views

urlpatterns = [
    path('', views.login),
    path('index', views.index),
    path('welcome', views.welcome),
    path('winning_bid_info', views.winning_bid_info),
    path('winning_detail', views.winning_detail),
    path('admin_info', views.admin_info),
    path('demo_add', views.demo_add),
    path('demo_edit', views.demo_edit),
    path('entrust_add', views.entrust_add),
    path('entrust_edit', views.entrust_edit),
    path('menu1', views.menu1),
    path('menu2', views.menu2),
    path('menu_add', views.menu_add),
    path('menu_see', views.menu_see),
    path('menu_edit', views.menu_edit),
    path('supplier_management', views.supplier_management),
    path('qualification_management', views.qualification_management),
    path('qua_mana_edit', views.qua_mana_edit),
    path('winning_detail_child', views.winning_detail_child),
    path('winning_detail_child_add', views.winning_detail_child_add),
    path('winning_detail_child_edit', views.winning_detail_child_edit),
    path('winning_bid_consum_deta', views.winning_bid_consum_deta),

    # path('upload', views.upload_img),

    # 接口
    path('sign_in/', views.sign_in, name='sign_in/'),
    path('zb_info/', views.zb_info, name='zb_info/'),
    path('test_api/', views.test_api, name='test_api/'),
    path('jbxx_info/', views.jbxx_info, name='jbxx_info/'),
    path('wtxx_info/', views.wtxx_info, name='wtxx_info/'),
    path('jbxx_edit/', views.jbxx_edit, name='jbxx_edit/'),
    path('jbxx_add/', views.jbxx_add, name='jbxx_add/'),
    path('wtxx_edit/', views.wtxx_edit, name='wtxx_edit/'),
    path('wtxx_add/', views.wtxx_add, name='wtxx_add/'),
    path('cglb_info/', views.cglb_info, name='cglb_info/'),
    path('cgmx_info/', views.cgmx_info, name='cgmx_info/'),
    path('shxx_info/', views.shxx_info, name='shxx_info/'),
    # path('menu_see_info/', views.menu_see_info, name='menu_see_info/'),
    path('get_menu_see/', views.get_menu_see, name='get_menu_see/'),
    path('menu_edit_info/', views.menu_edit_info, name='menu_edit_info/'),
    path('menu_add_info/', views.menu_add_info, name='menu_add_info/'),
    path('jbxx_del/', views.jbxx_del, name='jbxx_del/'),
    path('wtxx_del/', views.wtxx_del, name='wtxx_del/'),
    path('shxx_del/', views.shxx_del, name='shxx_del/'),
    path('upload_img/', views.upload_img, name='upload_img/'),
    path('jbxx_see/', views.jbxx_see, name='jbxx_see/'),
    path('jbxx_add/', views.jbxx_add, name='jbxx_add/'),
    path('winning_bid_consumables/', views.winning_bid_consumables, name='winning_bid_consumables/'),
    path('winning_bid_consumables_detailed/', views.winning_bid_consumables_detailed, name='winning_bid_consumables_detailed/'),
]
