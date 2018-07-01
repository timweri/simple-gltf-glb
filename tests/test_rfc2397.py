import unittest
from rfc2397 import RFC2397


class TestRFC2397(unittest.TestCase):
    """Tests for `rfc2397.py`."""

    def test_get_embedded_uri1(self):
        # Taken from https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/TriangleWithoutIndices
        test_data = [{
            "data": [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            "comptype_id": 5126,
            "ele_type": "VEC3",
            "vertex_attr": True
        }]

        uri, length, buffer_view_data = RFC2397.get_embedded_uri(test_data)
        self.assertEqual(uri, "data:application/octet-stream;base64,AAAAAAAAAAAAAAAAAACAPwAAAAAAAAAAAAAAAAAAgD8AAAAA")
        self.assertEqual(length, 36)
        self.assertEqual(buffer_view_data,
                         [
                             {
                                 "byteLength": 36,
                                 "byteOffset": 0,
                                 "byteStride": 12
                             }
                         ])

    def test_get_embedded_uri2(self):
        test_data = [{
            "data": [1, 2, 3, 4],
            "comptype_id": 5120,
            "ele_type": "SCALAR",
            "vertex_attr": False
        }]

        uri, length, buffer_view_data = RFC2397.get_embedded_uri(test_data)
        self.assertEqual(uri, "data:application/octet-stream;base64,AQIDBA==")
        self.assertEqual(length, 4)
        self.assertEqual(buffer_view_data,
                         [
                             {
                                 "byteLength": 4,
                                 "byteOffset": 0,
                                 "byteStride": 1
                             }
                         ])

    def test_get_embedded_uri3(self):
        test_data = [{
            "data": [[1, 2, 3, 4]],
            "comptype_id": 5122,
            "ele_type": "MAT2",
            "vertex_attr": False
        }]

        uri, length, buffer_view_data = RFC2397.get_embedded_uri(test_data)
        self.assertEqual(uri, "data:application/octet-stream;base64,AQACAAMABAA=")
        self.assertEqual(length, 8)
        self.assertEqual(buffer_view_data,
                         [
                             {
                                 "byteLength": 8,
                                 "byteOffset": 0,
                                 "byteStride": 8
                             }
                         ])

    def test_get_embedded_uri4(self):
        test_data = [{
            "data": [[1, 2, 3, 2, 3, 4, 3, 4, 5], [5, 5, 5, 6, 6, 6, 7, 7, 7]],
            "comptype_id": 5122,
            "ele_type": "MAT3",
            "vertex_attr": False
        }]

        uri, length, buffer_view_data = RFC2397.get_embedded_uri(test_data)
        self.assertEqual(uri, "data:application/octet-stream;base64,AQACAAMAAgADAAQAAwAEAAUABQAFAAUABgAGAAYABwAHAAcA")
        self.assertEqual(length, 36)
        self.assertEqual(buffer_view_data,
                         [
                             {
                                 "byteLength": 36,
                                 "byteOffset": 0,
                                 "byteStride": 18
                             }
                         ])
