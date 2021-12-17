import unittest
import app


class TestUrlShortener(unittest.TestCase):

    def test_shortened_length(self):
        urla = 'http://www.google.com'
        urlb = 'https://en.wikipedia.org/wiki/2018_FIFA_World_Cup/'
        
        for _ in range(5):
            short_a = app.shorten(urla)
            short_b = app.shorten(urlb)

            self.assertEqual(4, len(short_a))
            self.assertEqual(4, len(short_b))

    def test_url_with_http_valid(self):
        url = 'http://www.google.com'

        self.assertTrue(app.url_valid(url))

    def test_url_with_https_valid(self):
        url = 'https://www.google.com'

        self.assertTrue(app.url_valid(url))

    def test_url_with_htp_not_valid(self):
        url = 'htp://www.google.com'

        self.assertFalse(app.url_valid(url))

    def test_url_without_protocol_not_valid(self):
        url = 'www.google.com'

        self.assertFalse(app.url_valid(url))

    def test_empty_url_not_valid(self):
        url = ''

        self.assertFalse(app.url_valid(url))

if __name__ == '__main__':
    unittest.main()