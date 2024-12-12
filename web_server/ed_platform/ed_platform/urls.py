
from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name="login_user"),
    path('profile/', profile_view, name='profile'),
    path('manage_courses/', manage_courses_view, name='manage_courses'),
    path('create_course/', create_course_view, name='create_course'),
    path('add_material/', add_material_view, name='add_material'),
    path('add_student/', add_student_to_course_view, name='add_student'),
    path('remove_student/<int:course_id>/<int:student_id>/', remove_student_from_course_view, name='remove_student'),
    path('courses/<int:course_id>/materials/', course_materials_view, name='course_materials'),
    path('tests/create/', create_test, name='create_test'),

    #path('login/', user_login, name='login'),
    path('', test, name='test'),
]


from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)