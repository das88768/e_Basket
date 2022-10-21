from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="Home"),
    path("about/", views.about_us, name="About"),
    path("contact/", views.contact_us, name="ContactUs"),
    path("search/", views.search_product, name="Search"),
    path("track/", views.track_order, name="TrackOrder"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="Checkout"),
    path("product_detail/<int:id>", views.product_view, name="ProductView"),

    path("update-item/", views.updateItem, name="update-item"),
    path("process_order/", views.processOrder, name="process_order"),

    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
]
