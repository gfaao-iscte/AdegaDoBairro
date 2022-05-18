from django.urls import include, path
from . import views
# (. significa que importa views da mesma directoria)

urlpatterns = [
 path("", views.home, name="home"),
 path("login/", views.loginUser, name="loginUser"),
 path("register/", views.register, name="register"),
 path("logout/", views.logoutUser, name="logoutUser"),
 path("minhaconta/", views.minhaconta, name="minhaconta"),
 path("sobre/", views.sobre, name="sobre"),
 path("termos/", views.termos, name="termos"),
 path("dashboard/", views.dashboard, name="dashboard"),
 path("dashboardcolab/", views.dashboardcolab, name="dashboardcolab"),
 path("dashboardvinho/", views.dashboardvinho, name="dashboardvinho"),
 path("dashboardpedidos/", views.dashboardpedidos, name="dashboardpedidos"),
 path("editarcolab/<str:pk>", views.editarcolab, name="editarcolab"),
 path("apagarcolab/<str:pk>", views.apagarcolab, name="apagarcolab"),
 path("editarvinho/<str:pk>", views.editarvinho, name="editarvinho"),
 path("apagarvinho/<str:pk>", views.apagarvinho, name="apagarvinho"),
 path("vinhos/", views.vinhos, name="vinhos"),
 path("vinho/<str:pk>", views.vinho, name="vinho"),
 path("checkout/<str:pk>", views.checkout, name="checkout"),
 path("cesto/", views.cesto, name="cesto"),
 path('update_item/', views.update_item, name="update_item"),
 path("pagar/<str:pk>", views.pagar, name="pagar"),
 path("cancelar/<str:pk>", views.cancelar, name="cancelar"),
 path("preparar/<str:pk>", views.preparar, name="preparar"),
 path("enviar/<str:pk>", views.enviar, name="enviar"),
 path("cancelarloja/<str:pk>", views.cancelarloja, name="cancelarloja"),
 path("verencomenda/<str:pk>", views.verencomenda, name="verencomenda"),
]