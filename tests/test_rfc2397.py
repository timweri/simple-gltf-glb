import unittest
from rfc2397 import RFC2397


class TestRFC2397(unittest.TestCase):
    """Tests for `rfc2397.py`."""

    def test_get_embedded_uri(self):
        # Taken from https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/TriangleWithoutIndices
        test_data = {
            "data": [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            "comptype_id": 5126,
            "ele_type": "VEC3"
        }

        self.assertEqual(RFC2397.get_embedded_uri(**test_data),
                         ("data:application/octet-stream;base64,AAAAAAAAAAAAAAAAAACAPwAAAAAAAAAAAAAAAAAAgD8AAAAA",
                          36))

        test_data = {
            "data": [1, 2, 3, 4],
            "comptype_id": 5120,
            "ele_type": "SCALAR"
        }

        self.assertEqual(RFC2397.get_embedded_uri(**test_data),
                         ("data:application/octet-stream;base64,AQIDBA==",
                          4))

        test_data = {
            "data": [[[1, 2], [3, 4]]],
            "comptype_id": 5122,
            "ele_type": "MAT2"
        }

        self.assertEqual(RFC2397.get_embedded_uri(**test_data),
                         ("data:application/octet-stream;base64,AQACAAMABAA=",
                          8))

        test_data = {
            "data": [[[1, 2, 3], [2, 3, 4], [3, 4, 5]],
                     [[5, 5, 5], [6, 6, 6], [7, 7, 7]]],
            "comptype_id": 5122,
            "ele_type": "MAT3"
        }

        self.assertEqual(RFC2397.get_embedded_uri(**test_data),
                         ("data:application/octet-stream;base64,AQACAAMAAgADAAQAAwAEAAUABQAFAAUABgAGAAYABwAHAAcA",
                          36))
