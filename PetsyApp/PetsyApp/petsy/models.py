from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

def get_image_filename_post(instance, filename):
    return "%s" % (str(datetime.now()) + filename)

class UserPetsy(User):
    id_user = models.AutoField(primary_key=True)
    photo = models.ImageField(max_length=500, blank=True, default="default_user.png")
    description = models.TextField(blank=True)
    init_date = models.DateField(null=True, blank=True)


class UserFollowing(models.Model):
    follower = models.ForeignKey(UserPetsy, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(UserPetsy, related_name='follower', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')


class Shop(models.Model):
    id_shop = models.AutoField(primary_key=True)
    shop_name = models.TextField(default='Shop')
    user_owner = models.ForeignKey(UserPetsy, on_delete=models.CASCADE)

    def __str__(self):
        return "ID_shop: "+str(self.id_shop)+", " \
                "shop_name: "+self.shop_name+", " \
                "user_owner: "+str(self.user_owner.username)


class ShopFavorited(models.Model):
    follower = models.ForeignKey(UserPetsy, related_name='shop_faved', on_delete=models.CASCADE)
    shop_faved = models.ForeignKey(Shop, related_name='follower', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'shop_faved')


class Product(models.Model):
    CATEGORIES = (
        ("Joya", "Joyeria y complementos"),
        ("Ropa", "Ropa y calzado"),
        ("Casa", "Hogar y decoracion"),
        ("Boda", "Bodas y fiestas"),
        ("Toys", "Juguetes y ocio"),
        ("Cole", "Arte y objetos de decoración"),
        ("Arte", "Herramientas para la artesania"),
        ("Vint", "Vintage"),
        ("Otro", "Otras categorias")
    )
    _d_categories = dict(CATEGORIES)

    nameProduct = models.CharField(max_length=30)
    idProduct = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=5, choices=CATEGORIES, default='Otro')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    materials = models.TextField(default='')
    sold = models.IntegerField(default=0)
    # By default assign a house image to the product
    img = models.ImageField(upload_to=get_image_filename_post)
    rate = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    num_votes = models.IntegerField(default=0)  # numero persones que han votat un producte
    sum_votes = models.IntegerField(default=0)  # suma total del rate dels productes
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    reviews = models.TextField(default='[]')

    def get_human_category(self):
        return self._d_categories[self.category]


class Review(models.Model):
    # id_rev = models.AutoField(primary_key=True)
    # Relation between the User and the Review
    title = models.CharField(max_length=100, blank=False)
    message = models.TextField()
    date = models.DateTimeField()
    rating = models.DecimalField(max_digits=2,
                                 decimal_places=1,
                                 validators=[MinValueValidator(1, "Value must be between 1 and 5"),
                                             MaxValueValidator(5, "Value must be between 1 and 5")
                                             ]
                                 )
    user_rev = models.ForeignKey(UserPetsy, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

