from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoObjectPermissions
#
#
# class ObjectPermissionManager:
#     def __init__(self, obj, user):
#         self.obj = obj
#         self.user = user
#         self.permissions = None
#
#     def get_permissions(self):
#         """
#         Instantiates and returns the list of permissions that this view requires.
#         """
#         if self.action == 'list':
#             permission_classes = [IsAuthenticated]
#         else:
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]
#
