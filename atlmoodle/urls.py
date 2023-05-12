from django.urls import path, include
import atlmoodle.views


app_name = 'atlmoodle'
# (. significa que importa views da mesma directoria)


urlpatterns = [
    path('', atlmoodle.views.main_page, name='main_page'),
    path('go_quizzes', include('quizzes.urls', namespace='quizzes')),


]