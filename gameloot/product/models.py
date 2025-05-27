from django.db import models

class sign(models.Model):
    username=models.CharField(max_length=50)
    email=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    
    def __str__(self):
        return self.username
class category(models.Model):
  name=models.CharField(max_length=250,unique=True)
  slug = models.SlugField(max_length=50,unique=True)
   
  def __str__(self):
     return self.name

class Produit (models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10 , decimal_places= 2)
    category = models.ForeignKey(category,on_delete=models.SET_NULL,null=True,related_name='product')
    deals = models.BooleanField(default=False)
    image = models.ImageField(upload_to='media\product')
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    def __str__(self):
      return self.name
    
class Commande(models.Model):
    user = models.ForeignKey(sign, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    date_commande = models.DateTimeField(auto_now_add=True)
    est_validee = models.BooleanField(default=False)  # Ajoutez ce champ

    def __str__(self):
        return f"{self.quantite}x {self.produit.name}"