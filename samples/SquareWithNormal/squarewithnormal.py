from glb import GLB
from gltf import GLTF


def draw_glb():
    glb_asset = GLB()
    glb_asset.import_data(accessor_data=[
        {
            "name": "indices",
            "ele_type": "SCALAR",
            "comptype_id": 5123,
            "count": 4,
            "max_vals": [4],
            "min_vals": [0],
            "byte_offset": 0,
            "data": list(range(4)),
            "vertex_attr": False
        },
        {
            "name": "position",
            "ele_type": "VEC3",
            "comptype_id": 5126,
            "count": 4,
            "max_vals": [0.5, 0, 0.5],
            "min_vals": [-0.5, 0, -0.5],
            "byte_offset": 0,
            "data": [[-0.5, 0, 0.5], [0.5, 0, 0.5], [0.5, 0, -0.5], [-0.5, 0, -0.5]],
            "vertex_attr": True
        },
        {
            "name": "normal",
            "ele_type": "VEC3",
            "comptype_id": 5126,
            "count": 4,
            "max_vals": [1.0, 1.0, 1.0],
            "min_vals": [-1.0, -1.0, -1.0],
            "byte_offset": 0,
            "data": [[0.0, 1.0, 0.0]] * 4,
            "vertex_attr": True
        }
    ])
    glb_asset.create_primitive(name="box",
                               attributes={"POSITION": "position", "NORMAL": "normal"},
                               indices="indices")
    glb_asset.create_mesh(name="mesh1", primitives=["box"])
    glb_asset.create_node(name="node1", mesh="mesh1")
    glb_asset.create_scene(name="scene1", nodes=["node1"])
    glb_asset.export_glb('SquareWithNormal.glb')


def draw_gltf():
    gltf_asset = GLTF()
    gltf_asset.embed_data(buffer_name="buffer1",
                          accessor_data=[
                              {
                                  "name": "indices",
                                  "ele_type": "SCALAR",
                                  "comptype_id": 5123,
                                  "count": 6,
                                  "max_vals": [3],
                                  "min_vals": [0],
                                  "byte_offset": 0,
                                  "data": [0, 1, 2, 2, 3, 0],
                                  "vertex_attr": False
                              },
                              {
                                  "name": "position",
                                  "ele_type": "VEC3",
                                  "comptype_id": 5126,
                                  "count": 4,
                                  "max_vals": [0.5, 0, 0.5],
                                  "min_vals": [-0.5, 0, -0.5],
                                  "byte_offset": 0,
                                  "data": [[-0.5, 0, 0.5], [0.5, 0, 0.5], [0.5, 0, -0.5], [-0.5, 0, -0.5]],
                                  "vertex_attr": True
                              },
                              {
                                  "name": "normal",
                                  "ele_type": "VEC3",
                                  "comptype_id": 5126,
                                  "count": 4,
                                  "max_vals": [0, 1.0, 0],
                                  "min_vals": [0, 1.0, 0],
                                  "byte_offset": 0,
                                  "data": [[0.0, 1.0, 0.0]] * 4,
                                  "vertex_attr": True
                              }
                          ])
    gltf_asset.create_primitive(name="box",
                                attributes={"POSITION": "position", "NORMAL": "normal"},
                                indices="indices")
    gltf_asset.create_mesh(name="mesh1", primitives=["box"])
    gltf_asset.create_node(name="node1", mesh="mesh1")
    gltf_asset.create_scene(name="scene1", nodes=["node1"])
    gltf_asset.export_gltf('SquareWithNormal.gltf')


draw_glb()
draw_gltf()
