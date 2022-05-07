from django.urls import include, path
from rest_framework import routers

from users.views import MyUserViewSet, SignUpViewSet, TokenViewSet, UserViewSet
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/auth/token/', TokenViewSet.as_view(), name='token'),
    path('v1/auth/signup/', SignUpViewSet.as_view(), name='signup'),
    path('v1/users/me/', MyUserViewSet.as_view(), name='me_user'),
    path('v1/', include(router.urls)),
]
