from django.utils.deprecation import MiddlewareMixin


class StorePreviousURLMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        Stores the previous URL in the session.

        Parameters:
            request (HttpRequest): The current HTTP request.

        Returns:
            None
        """
        request.session["previous_url"] = request.META.get("HTTP_REFERER")
