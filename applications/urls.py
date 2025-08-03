from django.urls import path
from. import views
urlpatterns = [
    path('<int:pk>/apply/', views.apply_to_opportunity, name='apply_to_opportunity'),
    path('company/dashboard/', views.company_dashboard, name='company_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('status/<int:pk>/<str:status>/', views.update_application_status, name='update_application_status'),
    path('company/<int:opportunity_id>/download_zip/', views.download_applications_zip, name='download_applications_zip'),
    path('student/application/<int:pk>/pdf/', views.download_application_pdf, name='download_application_pdf'),
]
