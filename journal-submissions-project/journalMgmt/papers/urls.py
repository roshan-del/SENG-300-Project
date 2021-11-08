from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    # paths for non-logged-in user pages
    path('', views.login_page, name='login'),
    path('register/', views.registration_page, name='register'),

    # paths for general user pages
    path('logout/', views.logout_page, name='logout'),
    path('home/', views.home, name='home'),
    path('publications/', views.publications, name='publications'),
    path('staff/', views.staff, name='staff'),

    # paths for researcher pages
    path('researcher_account/', views.researcher_account, name='researcher_account'),
    path('researcher_account/submit/', views.submit, name='submit'),
    path('researcher_account/submission_history/', views.submission_history, name='submissions'),
    path('researcher_account/update_paper/<int:id>', views.update_paper, name='submissions'),

    # paths for reviewer pages
    path('reviewer_account/', views.reviewer_account, name='reviewer_account'),
    path('reviewer_account/assigned_papers/', views.assigned_papers, name='assigned_papers'),
    path('reviewer_account/review_paper/<int:id>', views.review_paper, name='review_paper'),

    # paths for editor pages
    path('editor_account/', views.editor_account, name='editor_account'),
    path('editor_account/editor_papers/', views.editor_papers, name='editor_papers'),
    path('editor_account/editor_papers/journals/<int:id>', views.journal, name='journal'),
    path('editor_account/assign_reviewer/<int:id>', views.assign_reviewer, name='assign_reviewer'),
    path('editor_account/accept_paper/', views.accept_paper, name='accept_paper'),

    path('account/submit/', views.submit, name='submit'),
    path('account/submissions/', views.submissions, name='submissions'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
