"""Define your api customized throttle classes"""

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AnonMinThrottle(AnonRateThrottle):
    """Throttle class of anonymous user rate with customized attributes"""

    # Set scope object that defined in settings.py file within
    # 'DEFAULT_THROTTLE_RATES'
    scope = 'anon_min'


class UserMinThrottle(UserRateThrottle):
    """Throttle class of user rate with customized attributes"""

    # Set scope object that defined in settings.py file within
    # 'DEFAULT_THROTTLE_RATES'
    scope = 'user_min'
