import unittest
from gltf import GLTF
import filecmp


# TODO: Finish test cases for all public methods
class TestConverter(unittest.TestCase):
    def test_create_scene(self):
        gltf_asset = GLTF()

        # Test 1
        scene_index = gltf_asset.create_scene(name="test_scene1")
        self.assertDictEqual(gltf_asset.scenes[scene_index], {})

        # Test 2
        scene_index = gltf_asset.create_scene(name="test_scene2", nodes=[5, 2, 3])
        self.assertDictEqual(gltf_asset.scenes[scene_index], {"nodes": [5, 2, 3]})

    def test_create_node(self):
        gltf_asset = GLTF()

        # Test 1
        node_index = gltf_asset.create_node(name="test_node1")
        self.assertDictEqual(gltf_asset.nodes[node_index], {})

        # Test 2
        node_index = gltf_asset.create_node(name="test_node2",
                                            matrix=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        self.assertDictEqual(gltf_asset.nodes[node_index],
                             {"matrix": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]})

        # Test 3
        node_index = gltf_asset.create_node(name="test_node3",
                                            mesh=0,
                                            rotation=[1, 2, 3, 4],
                                            scale=[1, 2, 3],
                                            translation=[1, 2, 3])
        self.assertDictEqual(gltf_asset.nodes[node_index],
                             {"mesh": 0,
                              "rotation": [1, 2, 3, 4],
                              "scale": [1, 2, 3],
                              "translation": [1, 2, 3]})

        # Test 4
        node_index = gltf_asset.create_node(name="test_node4",
                                            children=["test_node1", 1, "test_node3"])
        self.assertDictEqual(gltf_asset.nodes[node_index],
                             {"children": [0, 1, 2]})

    def test_full_asset1(self):
        """This test data is taken from https://github.com/KhronosGroup/glTF-Sample-Models/blob/master/2.0/Triangle/
        """
        gltf_asset = GLTF()
        gltf_asset.embed_data(buffer_name="vertices",
                              accessor_data=[{
                                  "name": "vertices",
                                  "data": [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
                                  "ele_type": "VEC3",
                                  "comptype_id": 5126,
                                  "count": 3,
                                  "max_vals": [1.0, 1.0, 0.0],
                                  "min_vals": [0.0, 0.0, 0.0],
                                  "byte_offset": 0,
                                  "target": 34962,
                                  "vertex_attr": True
                              }])
        gltf_asset.create_primitive(name="primitive1",
                                    attributes={
                                        "POSITION": "vertices"
                                    })
        gltf_asset.create_mesh(name="mesh1", primitives=["primitive1"])
        gltf_asset.create_node(name="node1", mesh="mesh1")
        gltf_asset.create_scene(name="scene1", nodes=["node1"])

        self.assertDictEqual(gltf_asset.to_dict(),
                             {
                                 "scenes": [
                                     {
                                         "nodes": [0]
                                     }
                                 ],
                                 "nodes": [
                                     {
                                         "mesh": 0
                                     }
                                 ],
                                 "meshes": [
                                     {
                                         "primitives": [{
                                             "attributes": {
                                                 "POSITION": 0
                                             }
                                         }]
                                     }
                                 ],
                                 "buffers": [
                                     {
                                         "uri": "data:application/octet-stream;base64,AAAAAAAAAAAAAAAAAACAPwAAAAAAAAAAA"
                                                "AAAAAAAgD8AAAAA",
                                         "byteLength": 36
                                     }
                                 ],
                                 "bufferViews": [
                                     {
                                         "buffer": 0,
                                         "byteOffset": 0,
                                         "byteLength": 36,
                                         "target": 34962
                                     }
                                 ],
                                 "accessors": [
                                     {
                                         "bufferView": 0,
                                         "byteOffset": 0,
                                         "componentType": 5126,
                                         "count": 3,
                                         "type": "VEC3",
                                         "max": [1.0, 1.0, 0.0],
                                         "min": [0.0, 0.0, 0.0]
                                     }
                                 ],
                                 "asset": {
                                     "version": "2.0"
                                 }
                             })

    def test_full_asset2(self):
        """This test data is taken from https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/Triangle
        """
        gltf_asset = GLTF()
        gltf_asset.embed_data(buffer_name="buffer1",
                              accessor_data=[
                                  {
                                      "name": "indices",
                                      "ele_type": "SCALAR",
                                      "comptype_id": 5123,
                                      "target": 34963,
                                      "count": 3,
                                      "max_vals": [2],
                                      "min_vals": [0],
                                      "byte_offset": 0,
                                      "data": [0, 1, 2],
                                      "vertex_attr": False
                                  },
                                  {
                                      "name": "vertices",
                                      "ele_type": "VEC3",
                                      "comptype_id": 5126,
                                      "target": 34962,
                                      "count": 3,
                                      "max_vals": [1.0, 1.0, 0.0],
                                      "min_vals": [0.0, 0.0, 0.0],
                                      "byte_offset": 0,
                                      "data": [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
                                      "vertex_attr": True
                                  }
                              ])
        gltf_asset.create_primitive(name="primitive1",
                                    attributes={
                                        "POSITION": "vertices"
                                    },
                                    indices="indices")
        gltf_asset.create_mesh(name="mesh1", primitives=["primitive1"])
        gltf_asset.create_node(name="node1", mesh="mesh1")
        gltf_asset.create_scene(name="scene1", nodes=["node1"])

        self.assertDictEqual(gltf_asset.to_dict(),
                             {
                                 "scenes": [
                                     {
                                         "nodes": [0]
                                     }
                                 ],
                                 "nodes": [
                                     {
                                         "mesh": 0
                                     }
                                 ],
                                 "meshes": [
                                     {
                                         "primitives": [{
                                             "attributes": {
                                                 "POSITION": 1
                                             },
                                             "indices": 0
                                         }]
                                     }
                                 ],
                                 "buffers": [
                                     {
                                         "uri": "data:application/octet-stream;base64,AAABAAIAAAAAAAAAAAAAAAAAAAAAAIA/A"
                                                "AAAAAAAAAAAAAAAAACAPwAAAAA=",
                                         "byteLength": 44
                                     }
                                 ],
                                 "bufferViews": [
                                     {
                                         "buffer": 0,
                                         "byteOffset": 0,
                                         "byteLength": 6,
                                         "target": 34963
                                     },
                                     {
                                         "buffer": 0,
                                         "byteOffset": 8,
                                         "byteLength": 36,
                                         "target": 34962
                                     }
                                 ],
                                 "accessors": [
                                     {
                                         "bufferView": 0,
                                         "byteOffset": 0,
                                         "componentType": 5123,
                                         "count": 3,
                                         "type": "SCALAR",
                                         "max": [2],
                                         "min": [0]
                                     },
                                     {
                                         "bufferView": 1,
                                         "byteOffset": 0,
                                         "componentType": 5126,
                                         "count": 3,
                                         "type": "VEC3",
                                         "max": [1.0, 1.0, 0.0],
                                         "min": [0.0, 0.0, 0.0]
                                     }
                                 ],

                                 "asset": {
                                     "version": "2.0"
                                 }
                             })

    def test_export_gltf1(self):
        """This test data is taken from https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/Triangle
        """
        gltf_asset = GLTF()
        gltf_asset.embed_data(buffer_name="buffer1",
                              accessor_data=[
                                  {
                                      "name": "indices",
                                      "ele_type": "SCALAR",
                                      "comptype_id": 5123,
                                      "target": 34963,
                                      "count": 3,
                                      "max_vals": [2],
                                      "min_vals": [0],
                                      "byte_offset": 0,
                                      "data": [0, 1, 2],
                                      "vertex_attr": False
                                  },
                                  {
                                      "name": "vertices",
                                      "ele_type": "VEC3",
                                      "comptype_id": 5126,
                                      "target": 34962,
                                      "count": 3,
                                      "max_vals": [1.0, 1.0, 0.0],
                                      "min_vals": [0.0, 0.0, 0.0],
                                      "byte_offset": 0,
                                      "data": [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
                                      "vertex_attr": True
                                  }
                              ])
        gltf_asset.create_primitive(name="primitive1",
                                    attributes={
                                        "POSITION": "vertices"
                                    },
                                    indices="indices")
        gltf_asset.create_mesh(name="mesh1", primitives=["primitive1"])
        gltf_asset.create_node(name="node1", mesh="mesh1")
        gltf_asset.create_scene(name="scene1", nodes=["node1"])

        self.assertDictEqual(gltf_asset.to_dict(),
                             {
                                 "scenes": [
                                     {
                                         "nodes": [0]
                                     }
                                 ],
                                 "nodes": [
                                     {
                                         "mesh": 0
                                     }
                                 ],
                                 "meshes": [
                                     {
                                         "primitives": [{
                                             "attributes": {
                                                 "POSITION": 1
                                             },
                                             "indices": 0
                                         }]
                                     }
                                 ],
                                 "buffers": [
                                     {
                                         "uri": "data:application/octet-stream;base64,AAABAAIAAAAAAAAAAAAAAAAAAAAAAIA/A"
                                                "AAAAAAAAAAAAAAAAACAPwAAAAA=",
                                         "byteLength": 44
                                     }
                                 ],
                                 "bufferViews": [
                                     {
                                         "buffer": 0,
                                         "byteOffset": 0,
                                         "byteLength": 6,
                                         "target": 34963
                                     },
                                     {
                                         "buffer": 0,
                                         "byteOffset": 8,
                                         "byteLength": 36,
                                         "target": 34962
                                     }
                                 ],
                                 "accessors": [
                                     {
                                         "bufferView": 0,
                                         "byteOffset": 0,
                                         "componentType": 5123,
                                         "count": 3,
                                         "type": "SCALAR",
                                         "max": [2],
                                         "min": [0]
                                     },
                                     {
                                         "bufferView": 1,
                                         "byteOffset": 0,
                                         "componentType": 5126,
                                         "count": 3,
                                         "type": "VEC3",
                                         "max": [1.0, 1.0, 0.0],
                                         "min": [0.0, 0.0, 0.0]
                                     }
                                 ],

                                 "asset": {
                                     "version": "2.0"
                                 }
                             })
        gltf_asset.export_gltf('gltf_output/test1.gltf')
        self.assertTrue(filecmp.cmp('gltf_output/test1.gltf', 'sample_gltf/test1.gltf', shallow=False))
