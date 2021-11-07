from rest_framework.permissions import DjangoObjectPermissions

class GenericObjectPermissions(DjangoObjectPermissions):
    def set_perms_map(self, perms_map={}):
        for k, v in perms_map.items():
            self.perms_map[k] = v

    def has_permission(self, request, view):
        self.set_perms_map(getattr(view, 'perms_map', {}))
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        self.set_perms_map(getattr(view, 'perms_map', {}))
        return super().has_object_permission(request, view, None)