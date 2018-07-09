from glb import GLB
from gltf import GLTF

accessor_data = [
    {
        "name": "indices",
        "ele_type": "SCALAR",
        "comptype_id": 5123,
        "count": 36,
        "max_vals": [23],
        "min_vals": [0],
        "byte_offset": 0,
        "data": [0, 3, 1, 3, 2, 1,
                 4, 6, 7, 4, 5, 6,
                 8, 9, 11, 8, 11, 10,
                 12, 14, 13, 12, 15, 14,
                 19, 16, 17, 19, 17, 18,
                 20, 21, 22, 20, 23, 21],
        "vertex_attr": False
    },
    {
        "name": "position",
        "ele_type": "VEC3",
        "comptype_id": 5126,
        "count": 24,
        "max_vals": [0.5, 0.5, 0.5],
        "min_vals": [-0.5, -0.5, -0.5],
        "byte_offset": 0,
        "data": [[-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, -0.5, -0.5], [-0.5, -0.5, -0.5],
                 [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5],
                 [-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, -0.5], [0.5, 0.5, 0.5],
                 [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
                 [-0.5, -0.5, 0.5], [-0.5, 0.5, 0.5], [-0.5, 0.5, -0.5], [-0.5, -0.5, -0.5],
                 [0.5, -0.5, -0.5], [0.5, 0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, -0.5]],
        "vertex_attr": True
    },
    {
        "name": "normal",
        "ele_type": "VEC3",
        "comptype_id": 5126,
        "count": 24,
        "max_vals": [1.0, 1.0, 1.0],
        "min_vals": [-1.0, -1.0, -1.0],
        "byte_offset": 0,
        "data": [[0, -1, 0]] * 4 + [[0, 0, 1]] * 4 + [[0, 1, 0]] * 4
                + [[0, 0, -1]] * 4 + [[-1, 0, 0]] * 4 + [[1, 0, 0]] * 4,
        "vertex_attr": True
    }
]


def draw_glb():
    glb_asset = GLB()
    glb_asset.import_data(accessor_data=accessor_data)
    glb_asset.create_primitive(name="box",
                               attributes={"POSITION": "position", "NORMAL": "normal"},
                               indices="indices")

    glb_asset.create_mesh(name="mesh1", primitives=["box"])
    glb_asset.create_node(name="node1", mesh="mesh1")
    glb_asset.create_scene(name="scene1", nodes=["node1"])
    glb_asset.export_glb('Box.glb')


def draw_gltf():
    gltf_asset = GLTF()
    gltf_asset.embed_data(buffer_name="buffer1",
                          accessor_data=accessor_data)
    gltf_asset.create_primitive(name="box",
                                attributes={"POSITION": "position", "NORMAL": "normal"},
                                indices="indices")
    gltf_asset.create_mesh(name="mesh1", primitives=["box"])
    gltf_asset.create_node(name="node1", mesh="mesh1")
    gltf_asset.create_scene(name="scene1", nodes=["node1"])
    gltf_asset.export_gltf('Box.gltf')


draw_glb()
draw_gltf()
