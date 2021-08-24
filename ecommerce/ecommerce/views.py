from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class BaseAPIView(APIView):
    base_permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Instance and returns the list of permissions required by a view."""

        permissions = self.base_permission_classes
        if self.permission_classes:
            permissions.extend(self.permission_classes)

        self.permission_classes = permissions
        return super().get_permissions()
