from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "scholar"

urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),

    path('register/', views.register_page, name="register"),
    path('student/home/', views.logged_in_home, name="home"),
    path('student/scholarship/', views.view_available_scholarship, name="open-scholarship"),
    path('student/scholarship/view/<int:id>/', views.view_scholarship, name="view-scholarship"),
    path('student/schlarship/apply/<int:scholarship_id>/', views.apply_scholarship, name="apply-scholarship"),
    
    path('student/application_status/', views.application_status, name="application-status"),
    
    path('student/profile/', views.profile, name="profile"),
    path('student/information/', views.information, name="information"),

    path('administrator/dashboard/', views.admin_dashboard, name="admin-dashboard"),
    path('administrator/manage-scholarship/', views.admin_manage_scholarship, name="manage-scholarship"),
    path('administrator/update-scholarship/<int:pk>/', views.update_scholarship, name="update-scholarship"),
    path('administrator/archive-scholarship/<int:pk>/<str:action>/', views.update_scholarship_status, name="update-scholarship-status"),
    
    path('administrator/manage-user/', views.admin_manage_user, name="manage-user"),
    path('administrator/activity-logs/', views.activity_logs, name="activity-logs"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)