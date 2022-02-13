from django.urls import path

from . import views

# 네임스페이스 지정을 통해 추후 개발에 다양한 앱 개발시 혼동 X
app_name = 'pybo'
urlpatterns = [
    path("", views.index, name='index'),
    path("<int:question_id>/", views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path("question/create/", views.question_create, name="question_create"),
]