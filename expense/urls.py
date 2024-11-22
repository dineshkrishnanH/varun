"""
URL configuration for expense project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path

from budget import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("exp/add/",views.ExpenseCreateView.as_view(),name="exp-add"),

    path("exp/list/",views.ExpenseListView.as_view(),name="exp-list"),

    path("exp/<int:pk>/update/",views.ExpenseUpdateView.as_view(),name="exp-update"),

    path("exp/<int:pk>/remove/",views.ExpenseDeleteView.as_view(),name="exp-delete"),

    path("exp/sum/",views.ExpenseSummaryView.as_view(),name="exp-summary"),

    path("register/",views.SignUpView.as_view(),name="signup"),

    path("signin/",views.SignInView.as_view(),name="signin"),

    path("signout/",views.SignOutView.as_view(),name="signout"),

    path("about/",views.AboutPageView.as_view(),name="about"),

    path("dashboard/",views.DashBoardView.as_view(),name="dashboard"),

]
