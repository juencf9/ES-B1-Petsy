from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

from petsy.forms import *
from petsy.models import *
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from itertools import chain
import ast
import time


# Petsy

class SearchProductView(ListView):
    model = Product
    template_name = 'petsy/show_products.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        list_items = Product.objects.filter(nameProduct__icontains=query)

        return list_items


class SearchShopView(ListView):
    model = Shop
    template_name = 'petsy/show_products.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        list_items = Shop.objects.filter(shop_name__icontains=query)

        return list_items


class SearchUserView(ListView):
    model = User
    template_name = 'petsy/show_products.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        list_items = User.objects.filter(username__icontains=query)

        return list_items


def index(request):
    if request.user.is_authenticated:
        user = UserPetsy.objects.all().get(email=request.user.email)
        shops = Shop.objects.all().filter(user_owner=user)
        context = {
            "user": user,
            "list_shops": shops
        }
        return render(request, 'petsy/homepage.html', context)

    return render(request, 'petsy/homepage.html')

def signup(request):
    """
    Register a new user into database

    :param request: Request
    :return: ????????
    """
    if request.method == 'POST':
        username = (request.POST['username'])
        email = (request.POST['email'])
        password = (request.POST['password'])

        try:
            user = User.objects.get(username=username)
            return JsonResponse({
                'signup_successful': False,
                'response_code': 403  # That username already exists
            })
        except:
            try:
                user = User.objects.get(email=email)
                return JsonResponse({
                    'signup_successful': False,
                    'response_code': 402  # That email already exists
                })
            except:
                user = UserPetsy.objects.create_user(username=username, email=email, password=password)
                user.save()

                shop_user = Shop(
                    shop_name="Shop",
                    user_owner=user
                )
                shop_user.save()

                return JsonResponse({
                    'signup_successful': True,
                    'response_code': 200  # That username already exists
                })


def login_user(request):
    """
    This method checks whether the combination user/password exists or not

    :param request: Request
    :return: User if connected, None otherwise
    """

    if request.method == 'POST':
        mail = request.POST["email_login"]
        password = request.POST["password_login"]
        # print(mail)
        # print(password)

        try:
            username = User.objects.get(email=mail).username
        except:
            return JsonResponse({
                'login_successful': False,
                'response_code': 404  # Username with that email does not exists
            })

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            print(user, " has logged in.")
            return JsonResponse({
                'login_successful': True,
                'response_code': 200
            })
        else:
            print("User is None :/")
            return JsonResponse({
                'login_successful': False,
                'response_code': 403  # Wrong password
            })


def _check_user_connected(request):
    """
    Returns the User connected

    :param request: Request
    :return: User connected or None
    """
    if request.user.is_authenticated():
        return request.user
    else:
        return None


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def create(request):
    user = UserPetsy.objects.all().get(email=request.user.email)
    context = {
        'user': user,
        'dict_cat': Product._d_categories,
        'product_form': ProductForm()
    }
    return render(request, 'petsy/createProduct.html', context)


"""
# Vista de productos (testing)
def products(request, username=None):
    print("REQUEST: ", request)
    if username:
        response = "You are looking for %s's products" % username
    else:
        response = "You are looking for featured products"
    return HttpResponse(response)

"""


def profile(request, id=None):
    user = UserPetsy.objects.all().get(id=id)
    shops = Shop.objects.all().filter(user_owner=user)
    followers = user.follower.all().count()
    following = user.following.all().count()
    fav_shops = user.shop_faved.all()
    products = Product.objects.all()

    """
    product_list = []
    for shop in shops:
        product_list.append(Product.objects.all().filter(shop=shop.id_shop))
    """

    if request.user.is_authenticated:
        yo = UserPetsy.objects.all().get(id=request.user.id)
        context = {
            "user": user,
            "followers": followers,
            "following": following,
            "list_shops": shops,
            "list_items": fav_shops,
            "follow": yo.following.filter(following=user).count() == 1,
            "list_products": products
        }
    else:
        context = {
            "user": user,
            "followers": followers,
            "following": following,
            "list_shops": shops,
            "list_items": fav_shops,
            "follow": False,
            "list_products": products
        }
    return render(request, 'petsy/profile.html', context)


def shop(request, id_shop=None):
    _shop = Shop.objects.all().get(id_shop=id_shop)
    product_list = list(Product.objects.all().filter(shop=_shop))
    user = UserPetsy.objects.all().get(email=_shop.user_owner.email)

    if request.user.is_authenticated:
        yo = UserPetsy.objects.all().get(id=request.user.id)
        context = {
            "shop": _shop,
            "list_products": product_list,
            "user": user,
            "favorited": yo.shop_faved.filter(shop_faved=_shop).count() == 1
        }
    else:
        context = {
            "shop": _shop,
            "list_products": product_list,
            "user": user
        }
    return render(request, 'petsy/shop.html', context)


def get_product_by_id(request, id_product=None):
    """
    :param request:
    :param id_product:
    :return:
    """

    if request.method == 'GET':
        product_id = id_product if id_product is not None else request.GET['product_id']
        user = UserPetsy.objects.all().get(email=request.user.email)

        try:
            product = Product.objects.get(idProduct=product_id)

        except:
            return JsonResponse({
                "response_msg": "Error: El producto no existe",
                "response_code": 404  # Product not found
            })

        return render(request, 'petsy/product.html', {
            "product": product,
            "reviews": ast.literal_eval(product.reviews)
        })


def get_user(request):
    """

    :param request:
    :return: {
                "user": ESdinou,
                "photo": photo.png
                "description": hola soc ESdinou
                "follower_count:
    """
    shop = Shop.objects.get(user_owner=request.user)
    products = Product.objects.get(id_shop=shop.id_shop)
    print(products)
    product_array = []
    for i in range(4):
        product_array.append(products[i])

    return render(request, 'petsy/profile.html', {
        "user": request.POST['username'],
        "photo": request.POST['photo'],
        "description": request.POST['description'],
        "follower_count": request.POST['follower_count'],
        "following_users": request.POST['following_users'],
        "favorite_products": request.POST['favorite_products'],
        "shop_name": shop.shop_name,
        "id_shop": shop.id_shop,
        "products_array": product_array
    })



@login_required()
def following_users(request):
    if request.method == 'POST':
        follower = get_object_or_404(UserPetsy, id=request.user.id)
        following = get_object_or_404(UserPetsy, id=request.POST['following'])

        relation = follower.following.filter(following=following)
        if relation:
            relation.delete()
            return JsonResponse({
                "response_msg": "Dejar de seguir OK!",
                "response_code": 200
            })
        else:
            follower.following.add(UserFollowing(following=following), bulk=False)
            return JsonResponse({
                "response_msg": "Seguir usuario OK!",
                "response_code": 201
            })

    return JsonResponse({
        "response_msg": "Error: GET encontrado",
        "response_code": 400
    })


@login_required()
def favorite_shop(request):
    if request.method == 'POST':
        # print(request.POST['shop_favorited'])
        follower = get_object_or_404(UserPetsy, id=request.user.id)
        shop_favorited = get_object_or_404(Shop, id_shop=request.POST['following'])

        relation = follower.shop_faved.filter(shop_faved=shop_favorited)
        if relation:
            relation.delete()
            return JsonResponse({
                "response_msg": "Dejar de seguir tienda OK!",
                "response_code": 200
            })
        else:
            follower.shop_faved.add(ShopFavorited(shop_faved=shop_favorited), bulk=False)
            return JsonResponse({
                "response_msg": "Seguir tienda OK!",
                "response_code": 201
            })

    return JsonResponse({
        "response_msg": "Error: GET encontrado",
        "response_code": 400
    })


def review_product_by_id(request):
    """
    That function expects a request with the following body:
        {
            "product_id": 4,
            "review": "Very good quality, I really recommend it bc...",
            "rate": 3,
            "username": "joseluis"
        }
    And then, updates the field 'reviews' from the 'product_id' product.

    :param request
    :return: JsonResponse
    """
    id_product = request.POST['product_id']
    product_to_update = Product.objects.get(idProduct=id_product)
    new_review = request.POST['review']
    new_rate = request.POST['rate']
    user = request.user.username  # "joseluis"  # request.POST['username']
    id = request.user.id

    actual_reviews = product_to_update.reviews
    review_array = ast.literal_eval(actual_reviews)

    new_review_obj = {
        "user": {
            "profile_pic": "default_user.png",
            "username": user,
            "id": id
        },
        "date": time.strftime('%y/%m/%d %X'),
        "message": new_review
    }

    review_array.append(new_review_obj)

    updated_sum_votes = product_to_update.sum_votes + float(new_rate)
    updated_num_votes = product_to_update.num_votes + 1

    Product.objects. \
        filter(idProduct=id_product). \
        update(sum_votes=updated_sum_votes, num_votes=updated_num_votes, reviews=str(review_array))

    product = Product.objects.get(idProduct=id_product)

    return redirect(get_product_by_id, id_product=product.idProduct)


def show_profile_followers(request, id=None, type="follower"):
    user = UserPetsy.objects.all().get(id=id)
    if type == "following":
        list_users = user.following.filter(follower=user)
        aux = [user.following for user in list_users]

    else:
        list_users = user.follower.filter(following=user)
        aux = [user.follower for user in list_users]

    context = {
        "type": "user",
        "list_items": aux,
    }
    return render(request, 'petsy/show_products.html', context)


def remove_product(request, id_product=None):
    """
    :param request:
    :param id_product:
    :return:
    """
    if request.method == 'GET':
        product_id = id_product if id_product is not None else request.GET['product_id']

        try:
            product = Product.objects.get(idProduct=product_id)
            product.remove()

        except:
            return JsonResponse({
                "response_msg": "Error: El producto no existe",
                "response_code": 404  # Product not found
            })

        return JsonResponse({
            "result_code": 200
        })


def create_product(request):
    """
    Register a new user into database

    :param request: Request
    :return: ????????
    """
    if request.method == 'POST':

        username = request.user
        user = UserPetsy.objects.get(username=username)

        try:
            shop = Shop.objects.get(user_owner=user).id_shop
            print("Shop already exists.")
        except:
            print("No shop yet, creating a new one.")
            shop = Shop(
                shop_name="Shop",
                user_owner=user
            )
            shop.save()

        shop = Shop.objects.get(user_owner=user)
        product = ProductForm(request.POST, request.FILES)
        if product.is_valid():
            p = product.save(commit=False)
            p.shop = shop
            p.save()
            return redirect(get_product_by_id, id_product=p.idProduct)
    return HttpResponse('')


def searching(object, search, edit_distance):
    from .levenshtein import levenshtein_func

    if (object == 'product'):
        result = list(set(Product.objects.values_list('result', flat=True)))

    elif (object == 'username'):
        result = list(set(UserPetsy.objects.values_list('result', flat=True)))

    elif (object == 'shop'):
        result = list(set(Shop.objects.values_list('result', flat=True)))

    search_dist = [(x, levenshtein_func(x.lower(), search.lower())) for x in result if
                   levenshtein_func(x.lower(), search.lower()) <= edit_distance]
    search_dist += [(x, len(x) - len(search)) for x in result if search.lower() in x.lower()]
    search_dist.sort(key=lambda x: x[1])
    if len(search_dist) == 0:
        return []

    result, _ = zip(*search_dist)
    return list(set(result))


def search(request):
    if request.method['GET']:
        return JsonResponse({
            "result_code": 200,
            "results": searching(request.GET['object'], request.GET['search'], 10)
        })


def search2(request):
    if request.method == 'GET':
        type = request.GET.get('type')
        query = request.GET.get('q')
        if type == "product":
           list_items = Product.objects.filter(nameProduct__icontains=query)
        elif type == "shop":
            list_items = Shop.objects.filter(shop_name__icontains=query)
        else:
            list_items = User.objects.filter(username__icontains=query)

        context = {
            "list_items": list_items,
            "type": type
        }

        return render(request, 'petsy/show_products.html', context)

