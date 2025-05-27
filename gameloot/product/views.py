from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from .models import sign, Produit, Commande
import random

class bibliotequeview(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login_page')

        user = sign.objects.get(id=user_id)
        # Récupère toutes les commandes validées (payées) de l'utilisateur
        commandes = Commande.objects.filter(user=user, est_validee=True).order_by('-date_commande')

        # Crée une liste des produits achetés (sans doublons)
        produits_achetes = []
        produits_ids = set()
        
        for commande in commandes:
            if commande.produit.id not in produits_ids:
                produits_achetes.append(commande.produit)
                produits_ids.add(commande.produit.id)

        return render(request, 'product/biblioteque.html', {
            'produits': produits_achetes
        })

class commentsview(View):
    def get(self, request):
        return render(request, 'product/comments.html')

class consoleview(View):
    def get(self, request):
        produits = Produit.objects.filter(deals=False)
        return render(request, 'product/console.html', {'produits': produits})

class panierview(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login_page')

        user = sign.objects.get(id=user_id)
        commandes = Commande.objects.filter(user=user, est_validee=False).order_by('-date_commande')

        total_general = sum(c.quantite * c.produit.price for c in commandes)

        return render(request, 'product/panier.html', {
            'commandes': commandes,
            'total_general': total_general
        })

class simulationview(View):
    def get(self, request):
        produits = Produit.objects.filter(category__name='simulation')
        return render(request, 'product/simulation.html', {'produits': produits})

class conduite_et_courseview(View):
    def get(self, request):
        produits = Produit.objects.filter(category__name='conduite_et_course')
        return render(request, 'product/conduite_et_course.html', {'produits': produits})

class shootview(View):
    def get(self, request):
        produits = Produit.objects.filter(category__name='shoot')
        return render(request, 'product/shoot.html', {'produits': produits})

class actionview(View):
    def get(self, request):
        produits = Produit.objects.filter(category__name='action')
        return render(request, 'product/action.html', {'produits': produits})

class adventureView(View):
    def get(self, request):
        produits = Produit.objects.filter(category__name='adventure')
        return render(request, 'product/adventure.html', {'produits': produits})

class sportView(View):
    def get(self, request):
        produits = Produit.objects.filter(category__name='sports')
        return render(request, 'product/sport.html', {'produits': produits})

class consulter2View(View):
    def get(self, request):
        produits = list(Produit.objects.filter(deals=True))
        random.shuffle(produits)
        return render(request, 'product/consulter2.html', {'produits': produits})

class productView(View):
    def get(self, request):
        produits = Produit.objects.all()
        return render(request, 'product/consulter.html', {'produits': produits})

class signView(View):
    def get(self, request):
        return render(request, 'product/sign.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if sign.objects.filter(username=username).exists():
            return render(request, 'product/sign.html', {'messages': 'Username already exists!'})

        if sign.objects.filter(email=email).exists():
            return render(request, 'product/sign.html', {'messages': 'Email already exists!'})

        new_user = sign(username=username, email=email, password=password)
        new_user.save()

        return render(request, 'product/sign.html', {'message': 'User created successfully!'})

class loginview(View):
    def get(self, request):
        return render(request, 'product/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = sign.objects.filter(username=username, password=password).first()
        if user:
            request.session['user_id'] = user.id
            return redirect('consulter2_page')
        else:
            return render(request, 'product/login.html', {'error': 'Invalid username or password!'})
class ValiderCommandeView(View):
    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login_page')

        user = sign.objects.get(id=user_id)
        Commande.objects.filter(user=user, est_validee=False).update(est_validee=True)
        
        messages.success(request, "Commande validée avec succès ! mrc pour votre confiance :)")
        return redirect('panier_page')

class CommandeView(View):
    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login_page')

        produit_id = request.POST.get('produit_id')
        quantite = request.POST.get('quantite', '1')

        # Validation
        if not produit_id or not quantite.isdigit() or int(quantite) < 1:
            messages.error(request, "Quantité invalide")
            return redirect(request.META.get('HTTP_REFERER', 'consulter2_page'))

        try:
            user = sign.objects.get(id=user_id)
            produit = get_object_or_404(Produit, id=produit_id)

            # Création/mise à jour de la commande
            commande, created = Commande.objects.get_or_create(
                user=user,
                produit=produit,
                est_validee=False,
                defaults={'quantite': quantite}
            )

            if not created:
                commande.quantite += int(quantite)
                commande.save()

            # Stocker le message et indiquer qu'il faut rediriger
            request.session['confirmation_message'] = "Produit ajouté au panier !"
            request.session['should_redirect'] = True  # Nouveau flag
            return redirect(reverse('commande_detail', kwargs={'produit_id': produit_id}))

        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
            return redirect('consulter2_page')
    def get(self, request, produit_id=None):
      user_id = request.session.get('user_id')
      if not user_id:
        return redirect('login_page')

      if produit_id:
        produit = get_object_or_404(Produit, id=produit_id)
        context = {'produit': produit}
        
        # Récupère et supprime le message de la session
        if 'confirmation_message' in request.session:
            context['confirmation_message'] = request.session.pop('confirmation_message')
            context['should_redirect'] = request.session.pop('should_redirect', False)
        
        return render(request, 'product/commande.html', context)
    
      return redirect('panier_page')

class ClearMessageView(View):
    def post(self, request):
        if 'confirmation_message' in request.session:
            del request.session['confirmation_message']
        if 'should_redirect' in request.session:
            del request.session['should_redirect']
        return JsonResponse({'status': 'success'})