from django.urls import path, include
import atlmoodle.views


app_name = 'atlmoodle'
# (. significa que importa views da mesma directoria)


urlpatterns = [
    # path('', atlmoodle.views.main_page, name='main_page'),
    # path('go_quizzes', include('quizzes.urls', namespace='quizzes')),

    path('', atlmoodle.views.main_page, name='main_page'),
    path('go_quizzes', include('quizzes.urls', namespace='quizzes')),
    # path('forum', atlmoodle.views.forum, name="forum"),
    # path('criarPost', atlmoodle.views.criarPost, name="criarpost"),
    path('<int:thread_id>', atlmoodle.views.detalhe, name="detalhe"),
    path('registo', atlmoodle.views.registo, name="registo"),
    # path('eliminarpost', atlmoodle.views.eliminarPost, name='eliminarPost'),
    path('eliminar', atlmoodle.views.eliminar, name='eliminar'),
    path('loginpage', atlmoodle.views.loginpage, name='loginpage'),
    path('logoutview', atlmoodle.views.logoutview, name='logoutview'),
    path('detalhe', atlmoodle.views.detalhe, name="detalhe")

]
