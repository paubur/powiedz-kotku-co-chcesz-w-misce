"""project URL Configuration

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
from django.contrib import admin
from django.urls import path, re_path
from project_diet.views import AddUserView, LoginView, LogoutView, CatsListView, AddCatView, CatDataView, FoodListView, \
    FoodDataView, AddFoodView, AddCompositionAndContentView, CompositionAndContentListView, CompareCompositionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_user/', AddUserView.as_view(), name='add_user'),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cats/', CatsListView.as_view(), name="cats"),
    path('add_cat/', AddCatView.as_view(), name="add_cat"),
    re_path(r'^cats/(?P<name>(\w)+)$', CatDataView.as_view()),
    re_path(r'^food_list/(?P<cat_id>(\d)+)$', FoodListView.as_view(), name="food_list"),
    re_path(r'^food/(?P<food>(\w)+)$', FoodDataView.as_view()),
    re_path(r'^add_food/(?P<cat_id>(\d)+)$', AddFoodView.as_view(), name="add_food"),
    re_path(r'^(?P<food_id>(\d)+)/add_composition$', AddCompositionAndContentView.as_view(), name="add_composition"),
    re_path(r'^(?P<food_id>(\d)+)/composition$', CompositionAndContentListView.as_view(), name='composition'),
    re_path(r'^food_list/(?P<cat_id>(\d)+)/compare$', CompareCompositionView.as_view(), name='compare_composition'),
]
