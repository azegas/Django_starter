from django.test import Client, TestCase
from django.urls import reverse


class TestViews(TestCase):
    """Class for view tests"""

    def setUp(self):
        """
        setUp method is simply for creating all kinds of objects that we will
        use/reuse in the tests below, later.
        """

        self.client = Client()
        self.index_url = reverse("index")

    def test_index_get(self):
        """test index view"""

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "project/blyn.html")
