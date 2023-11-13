import unittest
import sourcemap_extract


class CleanUrlsTests(unittest.TestCase):
    def test_clean_non_js_or_map_url(self):
        urls = set(["http://www.example.com",
                   "http://www.example.com/test.js.map"])
        expected = set(["http://www.example.com/test.js.map"])
        self.assertEqual(sourcemap_extract.clean_urls(urls), expected)

    def test_clean_js_if_map_exists(self):
        urls = set(["http://www.example.com/test.js",
                   "http://www.example.com/test.js.map"])
        expected = set(["http://www.example.com/test.js.map"])
        self.assertEqual(sourcemap_extract.clean_urls(urls), expected)

    def test_clean_with_query_params(self):
        urls = set(["http://www.example.com/test.js?foo=bar",
                   "http://www.example.com/test.js.map"])
        expected = set(["http://www.example.com/test.js.map"])
        self.assertEqual(sourcemap_extract.clean_urls(urls), expected)


if __name__ == '__main__':
    unittest.main()
