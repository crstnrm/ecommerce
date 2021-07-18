from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class BaseAPIView(APIView):
    base_permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Instance and returns the list of permissions required by a view."""
        
        self.permission_classes = \
            (self.permission_classes or []) + self.base_permission_classes
        return super().get_permissions()
