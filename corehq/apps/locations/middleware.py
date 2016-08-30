from .permissions import is_location_safe, location_restricted_response


class LocationAccessMiddleware(object):
    """
    Many large projects want to restrict data access by location.
    Views which handle that properly are called "location safe". This
    middleware blocks access to any non location safe features by users who
    have such a restriction. If these users do not have an assigned location,
    they cannot access anything.
    """

    def process_view(self, request, view_fn, view_args, view_kwargs):
        user = getattr(request, 'couch_user', None)
        domain = getattr(request, 'domain', None)
        if not user or not domain:
            request.can_access_all_locations = True
        elif user.has_permission(domain, 'access_all_locations'):
            request.can_access_all_locations = True
        else:
            request.can_access_all_locations = False
            if (
                not is_location_safe(view_fn, view_args, view_kwargs)
                or not user.get_sql_location(domain)
            ):
                return location_restricted_response(request)
