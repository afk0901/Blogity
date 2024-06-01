from datetime import datetime
from http import HTTPStatus
from unittest.mock import MagicMock, patch

from django.http import HttpRequest, HttpResponse
from django.test.testcases import SimpleTestCase
from model_bakery import baker

from middleware.logging import LoggingMiddleWare
from Users.models import CustomUser


class LoggingMiddleWareTests(SimpleTestCase):
    logger: str
    log_level: str

    user_id: int
    middleware: LoggingMiddleWare

    request: HttpRequest
    username: str
    date: str
    browser: str
    browser_version: str
    logging_message: str
    response_time: float
    mock_date: datetime

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.date = "1997-05-20"
        # today attribute is immutable, so this is the way we do it.
        date_patcher = patch("middleware.logging.date")
        cls.mock_date = date_patcher.start()
        cls.mock_date.today.return_value = cls.date
        cls.response_time = 0.0
        patch("middleware.logging.time.time", return_value=cls.response_time)
        cls.logger = "django"
        cls.log_level = "WARNING"
        cls.user_id = 1
        cls.username = "testuser"
        cls.browser = "Chrome"
        cls.browser_version = "91.0.4472"
        get_response = MagicMock(return_value=HttpResponse(status=HTTPStatus.OK))
        cls.middleware = LoggingMiddleWare(get_response)

    def setUp(self):
        super().setUp()
        self.request = HttpRequest()

        self.request.user = baker.prepare(
            CustomUser, username=self.username, id=self.user_id
        )

        self.logging_message = (
            f"{self.log_level}:{self.logger}:{self.date} "
            f"- user_id: {self.request.user.id}, "
            f"user: {self.request.user.username}, "
            "browser: {}/{}, response time: "
            f"{self.response_time} seconds"
        )

    def test_log_message(self) -> None:

        with self.assertLogs(self.logger, level=self.log_level) as cm:

            self.request.META["HTTP_USER_AGENT"] = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
            self.middleware(self.request)
            logging_message = self.logging_message.format(
                self.browser, self.browser_version
            )
            self.assertEqual([logging_message], cm.output)

    def test_no_http_user_agent_value(self) -> None:
        with self.assertLogs(self.logger, level=self.log_level) as cm:
            self.middleware(self.request)
            logging_message = self.logging_message.format("Other", "")
            self.assertEqual([logging_message], cm.output)
