from rest_framework.routers import SimpleRouter
from api.versioned.v1.users.viewsets import UserViewSet

router = SimpleRouter(trailing_slash=False)

router.register('users', UserViewSet)

urlpatterns = [] + router.urls
