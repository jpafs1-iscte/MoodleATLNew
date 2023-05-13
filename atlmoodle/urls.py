from django.urls import path, include
import atlmoodle.views


app_name = 'atlmoodle'
# (. significa que importa views da mesma directoria)


urlpatterns = [
    # path('', atlmoodle.views.main_page, name='main_page'),
    # path('go_quizzes', include('quizzes.urls', namespace='quizzes')),

    path('', atlmoodle.views.main_page, name='main_page'),
    path('go_quizzes', include('quizzes.urls', namespace='quizzes')),
    path('registo', atlmoodle.views.registo, name="registo"),
    path('eliminar', atlmoodle.views.eliminar, name='eliminar'),
    path('loginpage', atlmoodle.views.loginpage, name='loginpage'),
    path('logoutview', atlmoodle.views.logoutview, name='logoutview'),
    path('detalhe', atlmoodle.views.detalhe, name="detalhe"),
    path('home', atlmoodle.views.home, name='home'),
    path('addInForum/',atlmoodle.views.addInForum,name='addInForum'),
    path('addInDiscussion/',atlmoodle.views.addInDiscussion,name='addInDiscussion'),
    path('calendar', atlmoodle.views.calendar, name="calendar"),
    path('<int:event_id>', atlmoodle.views.calendar_details, name="calendar_details"),
    path('eventCreator', atlmoodle.views.eventCreator, name="eventCreator"),
    path('upload', atlmoodle.views.fazer_upload, name="fazer_upload"),
    path('file', atlmoodle.views.file, name="file"),
    path('eliminar', atlmoodle.views.eliminar, name="eliminar")
]
