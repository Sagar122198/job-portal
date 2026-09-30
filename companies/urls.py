from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.CreateJobs.as_view(), name='create'),
    path('jobs/', views.jobs, name='jobs'),
    path('companies/', views.companies, name='companies'),
    path('manage-jobs/', views.ManageJobsView.as_view(), name='manage_jobs'),
    path('detail/<int:pk>/', views.DetailPageView.as_view(), name='detail'),
    path('detail/<int:pk>/apply/', views.apply_for_job, name='apply'),
    path('update/<int:pk>/',views.UpdatePageView.as_view(), name = 'update'),
    path('delete/<int:pk>/' , views.DeleteJob.as_view() , name =  'delete'),
    path('job/<int:job_pk>/applicants/', views.get_applicants, name='get_applicants'),
    path('job/<int:job_pk>/applicant/<int:application_id>/', views.ApplicantDetailView.as_view(), name='applicant_detail'),
    path('applicant/<int:application_id>/status/', views.update_applicant_status, name='update_applicant_status'),
    path('api/my-applications/', views.get_job_seeker_applications, name='my_applications'),
]
