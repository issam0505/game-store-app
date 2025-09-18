from django.urls import path
from .views import SearchProduitView , productView,signView,loginview,CommandeView,consulter2View,sportView,adventureView,actionview,shootview,conduite_et_courseview,simulationview,panierview,consoleview,commentsview,ValiderCommandeView,ClearMessageView,bibliotequeview
urlpatterns = [
    path('',productView.as_view(),name='consulter'),
    path("sign/",signView.as_view(),name="sign_page"),
    path("login/",loginview.as_view(),name="login_page"),
     path("biblioteque/",bibliotequeview.as_view(),name="biblioteque_page"),
     path('commande/<int:produit_id>/', CommandeView.as_view(), name='commande_detail'),
    path("commande/",CommandeView.as_view(),name="commande_page"),
     path("consulter2/",consulter2View.as_view(),name="consulter2_page"),
      path("sport/",sportView.as_view(),name="sport_page"),
    path("adventure/",adventureView.as_view(),name="adventure_page"),
    path("action/",actionview.as_view(),name="action_page"),
    path("shoot/",shootview.as_view(),name="shoot_page"),
     path("conduite_et_course/",conduite_et_courseview.as_view(),name="conduite_et_course_page"),
     path("simulation/",simulationview.as_view(),name="simulation_page"),
     path("panier/",panierview.as_view(),name="panier_page"),
     path("console/",consoleview.as_view(),name="console_page"),
     path("comments/",commentsview.as_view(),name="comments_page"),
     path('commander/', ValiderCommandeView.as_view(), name='valider_commande'),
     path('clear-message/', ClearMessageView.as_view(), name='clear_message'),
     path('recherche/', SearchProduitView.as_view(), name='search_produit'),
]