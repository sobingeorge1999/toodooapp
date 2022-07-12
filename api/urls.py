from django.urls import path
from  api import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("todosviewset",views.TodosViewsetView,basename="todosviewset")
router.register("todosmodelviewset",views.TodoModelViewsetView,basename="todosmodelview")

urlpatterns=[
    path("todos",views.TodosView.as_view()),
    path("todos/<int:todo_id>",views.TodoDEtails.as_view()),
    path("users/accounts/signup",views.UserCreationView.as_view()),
    path("users/accounts/login",views.SignINView.as_view()),
    path("todosmixin",views.TodosMixinView.as_view()),
    path("todosmixin/details/<int:todo_id>",views.TodomixDetailsView.as_view())

]+router.urls