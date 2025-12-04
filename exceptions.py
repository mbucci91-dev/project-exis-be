class ServiceError(Exception):
    pass

class ResourceNotFound(ServiceError):
    pass

class PermissionDenied(ServiceError):
    pass

class AuthenticationError(ServiceError):
    pass