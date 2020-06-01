from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from questions import views
from dashboard import views as vw
from likes import views as vs
from profiles import views as vws


urlpatterns = [
    path('admin/', admin.site.urls),
    path('question/<int:id>/', views.single, name='question_single'),
    path('question/', views.home, name='question_home'),

    path('accounts/', include('accounts.urls')),

    path('', vw.home, name='home'),

    path('like/<email>/',vs.like_user, name='like_user'),
    path('profile/edit/', vws.profile_edit, name='profile_edit'),
    path('profile/<email>/',vws.profile_view, name='profile'),
    path('profile/', vws.profile_user, name='profile_user'),
    path('profile/jobs/add/', vws.job_add, name='job_add'),
    path('profile/jobs/edit/', vws.jobs_edit, name='jobs_edit'),

    path('matches', include('matcho.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
