from rest_framework.permissions import BasePermission


class Auto_Detect_UserDevice(BasePermission):
    def has_permission(self, request, view):
        print(view.action)
        token = view.kwargs.get('pk', None)
        if token:
            try:
                user_profile = request.user.UserDevice.get(token=token)
                user_type = user_profile.type

                have_permission = user_profile.type.permissions.filter(
                    name=view.action).exists()
                print(have_permission)
                return have_permission
            except:
                return False
        else:
            return False
