import unittest
from app import app  # Import your Flask app

class PlusTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_plus_floats(self):
        res = self.app.get('/plus/8.4/4')
        self.assertEqual(res.json, {'result': 12.4})

    def test_plus_floats_both(self):
        res = self.app.get('/plus/8.4/4.6')
        self.assertEqual(res.json, {'result': 13.0})

    def test_plus_negative_numbers(self):
        res = self.app.get('/plus/-5/-6')
        self.assertEqual(res.json, {'result': -11})

    def test_plus_mixed_negative_positive(self):
        res = self.app.get('/plus/-5/6')
        self.assertEqual(res.json, {'result': 1})

    def test_plus_zeros(self):
        res = self.app.get('/plus/0/0')
        self.assertEqual(res.json, {'result': 0})

    def test_plus_invalid_input(self):
        res = self.app.get('/plus/8/zero')
        self.assertEqual(res.json, {'error_msg': 'inputs must be numbers'})


if __name__ == '__main__':
    unittest.main()
