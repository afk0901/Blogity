import logging
import time
from datetime import date

import user_agents


class LoggingMiddleWare:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        today = date.today()
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        response_time = end_time - start_time
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        browser_type = user_agents.parse(user_agent).browser.family
        browser_version = user_agents.parse(user_agent).browser.version_string

        logger = logging.getLogger("django")
        logger.warning(
            f"{today} - user_id: {request.user.id}, "
            f"user: {request.user.username}, "
            f"browser: {browser_type}/{browser_version}, "
            f"response time: {response_time} seconds"
        )
        return response
