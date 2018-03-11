from .models import Session
from datetime import datetime


class CheckSession:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_id = request.COOKIES.get('session_id')

        try:
            session = Session.objects.get(key=session_id, date__gt=datetime.now())
            request.session = session
            request.user = session.user
        except Session.DoesNotExist:
            request.session = None
            request.user = None

        response = self.get_response(request)
        return response
