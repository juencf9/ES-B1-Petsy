from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^products/$', views.products, name='products'),
    # url(r'^products/(?P<username>.*)/$', views.products, name='products'),
    url(r'^register/$', views.signup, name="register"),
    url(r'^login/$', views.login_user, name="login"),
    url(r'^logout/$', views.logout_user, name="logout"),
    url(r'^create/$', views.create, name="create"),
    url(r'^profile/(?P<id>.*)/(?P<type>.*)/$', views.show_profile_followers, name="profile_followers"),
    url(r'^profile/(?P<id>.*)$', views.profile, name="profile"),
    url(r'^shop/(?P<id_shop>.*)$', views.shop, name="shop"),

    url(r'^product/(?P<id_product>.*)/$', views.get_product_by_id, name='product_by_id'),
    url(r'^product/$', views.create_product, name='create_product'),
    url(r'^review_product_by_id/$', views.review_product_by_id, name='review_product_by_id'),
    url(r'^follow/$', views.following_users, name="follow_user"),
    url(r'^favorited/$', views.favorite_shop, name="follow_user"),
    url(r'^profile/(?P<id>.*)/(?P<type>.*)/$', views.show_profile_followers, name="profile_followers"),
    url(r'search/$', views.search2, name='search')
]
