from django.urls import path
from .views import( AddToCartAPIView,ViewCartAPIView,RemoveFromCartAPIView,
                   AddToWishlistAPIView,ViewWishlistAPIView,RemoveFromWishlistAPIView,CheckoutAPIView,
                   OrderHistoryAPIView,DecreaseCartItemAPIView
)

urlpatterns = [
    path('cart/add/', AddToCartAPIView.as_view()),
    path('cart/', ViewCartAPIView.as_view()),
    path('cart/remove/<int:pk>/',RemoveFromCartAPIView.as_view()),
    path('cart/decrease/<int:pk>/', DecreaseCartItemAPIView.as_view()),
    
    path('wishlist/add/', AddToWishlistAPIView.as_view()),
    path('wishlist/',ViewWishlistAPIView.as_view()),
    path('wishlist/remove/<int:pk>/',RemoveFromWishlistAPIView.as_view())
]


urlpatterns +=[
    path('checkout/', CheckoutAPIView.as_view()),
    path('orders/',OrderHistoryAPIView.as_view()),

]


