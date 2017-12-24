import unittest

import dmswitch


class DmswitchTestCase(unittest.TestCase):

    def setUp(self):
        self.app = dmswitch.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to dmswitch', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
