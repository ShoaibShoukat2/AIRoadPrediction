from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    
    path('', views.index, name='index'),
    
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('report-options/', views.Report_Options, name='report-options'),
    path('report-status/', views.Report_Status, name='report-status'),
    
    path('admin-reports/', views.Admin, name='admin-reports'),
    path('success/', views.success, name='success-page'),
    path('report/<int:report_id>/accept/', views.manual_accept_report, name='manual_accept_report'),
    path('report/<int:report_id>/reject/', views.manual_reject_report, name='manual_reject_report'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('logout/', views.logout_view, name='logout'),
    
    
]



























