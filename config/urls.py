from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from products import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),
    path(
    "products/",
    views.product_list,
    name="product_list",
    ),

    path(
    "products/add/",
    views.product_form,
    name="product_add",
    ),

    path(
    "products/edit/<int:pk>/",
    views.product_form,
    name="product_edit",
    ),

    path(
    "products/view/<int:pk>/",
    views.product_detail,
    name="product_detail",
    ),

    path(
    "products/delete/<int:pk>/",
    views.product_delete,
    name="product_delete",
    ),

]