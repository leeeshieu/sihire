from rest_framework import permissions

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Return True if user role is Admin, False otherwise
        """

        return request.user.is_authenticated and request.user.role.lower() == 'admin'

class IsApplicant(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Return True if user role is Applicant, False otherwise
        """

        return request.user.is_authenticated and request.user.role.lower() == 'applicant'

class IsInternal(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Return True if user role is Internal Company, False otherwise
        """

        return request.user.is_authenticated and (request.user.role.lower() == 'project manager' or request.user.role.lower() == 'director' or request.user.role.lower() == 'general affairs')

class IsGeneralAffairs(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Return True if user role is General Affairs, False otherwise
        """

        return request.user.is_authenticated and request.user.role.lower() == 'general affairs'