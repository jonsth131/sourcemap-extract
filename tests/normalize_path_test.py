import unittest
import sourcemap_extract


class NormalizePathTests(unittest.TestCase):
    def test_normalize_path_no_change(self):
        self.assertEqual(
            sourcemap_extract.normalize_path('foo/bar.js'),
            'foo/bar.js'
        )

    def test_normalize_path_remove_dot_slash(self):
        self.assertEqual(
            sourcemap_extract.normalize_path('./foo/bar.js'),
            'foo/bar.js'
        )

    def test_normalize_path_remove_dot_dot_slash(self):
        self.assertEqual(
            sourcemap_extract.normalize_path('../foo/bar.js'),
            'foo/bar.js'
        )

    def test_normalize_path_remove_webpack_prefix(self):
        self.assertEqual(
            sourcemap_extract.normalize_path('webpack:///foo/bar.js'),
            'foo/bar.js'
        )

    def test_normalize_path_remove_webpack_prefix_with_dot_slash(self):
        self.assertEqual(
            sourcemap_extract.normalize_path('webpack:///./foo/bar.js'),
            'foo/bar.js'
        )

    def test_normalize_path_remove_webpack_prefix_with_dot_dot_slash(self):
        self.assertEqual(
            sourcemap_extract.normalize_path('webpack:///../foo/bar.js'),
            'foo/bar.js'
        )


if __name__ == '__main__':
    unittest.main()
