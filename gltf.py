"""Converters to build glTF files

This module contains converters that convert/encode raw geometric data into data that can be used to build a glTF file.
This is just a simple demonstration of a glTF builder. Not all features are supported, such as animation, skinning,
camera, and texture.
"""

from bufferutility import BufferUtility
import json


# TODO: add support for material
class GLTF:
    def __init__(self):
        # Initialize objects according to the glTF specs
        self.scenes_map = {}
        self.scenes = []
        self.nodes_map = {}
        self.nodes = []
        self.cameras = []
        self.cameras_map = {}
        self.materials = []
        self.materials_map = {}
        self.meshes_map = {}
        self.meshes = []
        self.primitives_map = {}
        self.primitives = []
        self.buffers_map = {}
        self.buffers = []
        self.bufferViews_map = {}
        self.bufferViews = []
        self.accessors_map = {}
        self.accessors = []
        self.asset = {"version": "2.0", "generator": "timweri.simple-gltf-glb"}

        # Map parameter names to the corresponding map and singleton value
        self.para_name_map = {
            "scene": (self.scenes_map, True),
            "node": (self.nodes_map, False),
            "mesh": (self.meshes_map, True),
            "primitive": (self.primitives_map, False),
            "buffer": (self.buffers_map, True),
            "buffer_view": (self.bufferViews_map, True),
            "accessor": (self.accessors_map, True)
        }

    # ---------------------------------------------------------------------
    # SCENE METHODS:
    # ---------------------------------------------------------------------

    def _build_scene(self, nodes):
        """Create a scene with the specified properties but do not save it to the object's list of scenes.

        :return: scene <dict>
        """
        new_scene = {}

        new_nodes_ind = self._resolve_mapping(inp=nodes, mapping=self.nodes_map)
        if new_nodes_ind:
            new_scene["nodes"] = new_nodes_ind

        return new_scene

    def create_scene(self, name, nodes=None):
        """Create a scene with the specified properties.

        :return: scene index
        """
        new_scene = self._build_scene(nodes=nodes)
        self.scenes.append(new_scene)

        # Update scenes map
        self.scenes_map[name] = self._last_index(self.scenes)

        return self._last_index(self.scenes)

    def add_to_scene(self, scene_id, nodes):
        """Add properties to an existing scene.

        :return: scene index
        """
        scene_id = self._resolve_mapping(inp=scene_id, mapping=self.scenes_map)

        scene = self.scenes[scene_id]

        new_nodes_ind = self._resolve_mapping(inp=nodes, mapping=self.nodes_map)

        scene["nodes"] += new_nodes_ind

        return scene_id

    # ---------------------------------------------------------------------
    # NODE METHODS:
    # ---------------------------------------------------------------------

    def _build_node(self, camera, children, skin, matrix, mesh, rotation, scale, translation, weights):
        """Create a node.

        :return: node <dict>
        """
        new_node = {}

        properties_keys = ["camera", "children", "skin", "matrix", "mesh", "rotation", "scale", "translation",
                           "weights"]
        properties_values = [camera, children, skin, matrix, mesh, rotation, scale, translation, weights]
        properties_mapping = [self.cameras_map, self.nodes_map, None, None, self.meshes_map, None, None, None, None]

        for key, val, mapping in zip(properties_keys, properties_values, properties_mapping):
            if val is not None:
                new_node[key] = self._resolve_mapping(inp=val, mapping=mapping)

        return new_node

    def create_node(self, name, camera=None, children=None, skin=None, matrix=None, mesh=None, rotation=None,
                    scale=None, translation=None, weights=None):
        """Create a node and add it to the glTF object.

        :return: node index
        """
        new_node = self._build_node(camera=camera,
                                    children=children,
                                    skin=skin,
                                    matrix=matrix,
                                    mesh=mesh,
                                    rotation=rotation,
                                    scale=scale,
                                    translation=translation,
                                    weights=weights)

        self.nodes.append(new_node)

        if name:
            self.nodes_map[name] = self._last_index(self.nodes)

        return self._last_index(self.nodes)

    # ---------------------------------------------------------------------
    # MESH METHODS:
    # ---------------------------------------------------------------------

    def _build_mesh(self, primitives):
        """Create a mesh with the specified properties but do not save it to the object's list of meshes.

        :return: mesh <dict>
        """
        new_mesh = {}

        primitives_ind = self._resolve_mapping(inp=primitives, mapping=self.primitives_map)
        new_primitives = [self.primitives[i] for i in primitives_ind]

        new_mesh["primitives"] = new_primitives

        return new_mesh

    def create_mesh(self, name, primitives):
        """Create a mesh with the specified properties.

        :return: mesh index.
        """
        new_mesh = self._build_mesh(primitives=primitives)
        self.meshes.append(new_mesh)

        # Update meshes map
        self.meshes_map[name] = self._last_index(self.meshes)

        return self._last_index(self.meshes)

    def add_to_mesh(self, mesh_id, primitives):
        """Add properties to an existing mesh.

        :return: mesh index
        """
        mesh_id = self._resolve_mapping(inp=mesh_id, mapping=self.meshes_map)
        mesh = self.meshes[mesh_id]

        new_primitives_ind = self._resolve_mapping(inp=primitives, mapping=self.primitives_map)
        new_primitives = [self.primitives[i] for i in new_primitives_ind]
        mesh["primitives"] += new_primitives

        return mesh_id

    def _build_primitive(self, attributes, indices, material, mode):
        """Create a primitive with the specified properties but do not save it to the object's list of primitives.

        :return: primitive <dict>
        """
        new_primitive = {}

        properties_key = ["attributes", "indices", "material", "mode"]
        properties_val = [attributes, indices, material, mode]
        for key, val in zip(properties_key, properties_val):
            if val is not None:
                new_primitive[key] = self._resolve_mapping(inp=val, mapping=self.accessors_map)

        return new_primitive

    def create_primitive(self, name, attributes=None, indices=None, material=None, mode=None):
        """Create a primitive with the given properties.

        :return: primitive index.
        """
        new_primitive = self._build_primitive(attributes=attributes,
                                              indices=indices,
                                              material=self._resolve_mapping(inp=material,
                                                                             mapping=self.materials_map),
                                              mode=mode)

        self.primitives.append(new_primitive)

        self.primitives_map[name] = self._last_index(self.primitives)

        return self._last_index(self.primitives)

    def add_to_primitive(self, primitive_id, attributes, indices, material, mode):
        """Add properties to an existing primitive.

        :return: primitive index.
        """
        primitive_id = self._resolve_mapping(inp=primitive_id, mapping=self.primitives_map)

        primitive = self.primitives[primitive_id]

        properties_key = ["attributes", "indices", "material", "mode"]
        properties_val = [attributes, indices, material, mode]
        for key, val in zip(properties_key, properties_val):
            if val is not None:
                primitive[key] = self._resolve_mapping(inp=val, mapping=self.accessors_map)

        return primitive_id

    # ---------------------------------------------------------------------
    # MATERIAL METHODS:
    # ---------------------------------------------------------------------

    @staticmethod
    def _build_material(pbrmr, emissive):
        """Build a material

        :return: material <dict>
        """
        new_material = {}

        properties_keys = ["pbrMetallicRoughness", "emissiveFactor"]
        properties_vals = [pbrmr, emissive]

        for key, val in zip(properties_keys, properties_vals):
            if val is not None:
                new_material[key] = val

        return new_material

    def create_material(self, name, pbmr=None, emissive=None):
        """Create a material and add it to the glTF object.

        :param pbmr: metallic-roughness material model <dict>
        :param emissive: controls color and intensity of the light being emitted by the material <list>
        :return: material index
        """
        new_material = self._build_material(pbmr, emissive)

        self.materials.append(new_material)

        if name:
            self.materials_map[name] = self._last_index(self.materials)

        return self._last_index(self.materials)

    @staticmethod
    def build_pbrmr(base_color_fac=None, metallic_fac=None, roughness_fac=None):
        """Build a metallic-roughness material model

        :param base_color_fac: baseColorFactor e.g. [ 1.0, 1.0, 0.5, 1.0 ]
        :param metallic_fac: metallicFactor e.g. 1
        :param roughness_fac: roughnessFactor e.g. 1

        :return: metallic-roughness material model <dict>
        """
        new_pbrmr = {}

        properties_keys = ["baseColorFactor", "metallicFactor", "roughnessFactor"]
        properties_vals = [base_color_fac, metallic_fac, roughness_fac]

        for key, val in zip(properties_keys, properties_vals):
            if val is not None:
                new_pbrmr[key] = val

        return new_pbrmr

    # ---------------------------------------------------------------------
    # BUFFER DATA METHODS:
    # ---------------------------------------------------------------------

    def embed_data(self, buffer_name, accessor_data):
        """Create pairs of accessors and one buffer from raw data. Add them all to the glTF object.

        :param buffer_name: name of the buffer
        :param accessor_data: [{
                                 name: name of the bufferView and accessor
                                 data: raw data
                                 ele_type: type of each element in data
                                 count: number of elements in data
                                 comptype_id: type of each component of each element in data
                                 max_vals: maximum values of data
                                 min_vals: minimum values of data
                                 target: target that GPU buffer should be bound to
                                 normalized: specifies whether integer data should be normalized
                                 vertex_attr: specifies whether the data is a vertex attribute
                              }, ...]

        :return: (buffer index, accessor indices, bufferView indices)
        """
        accessor_indices = []
        buffer_view_indices = []

        buffer_data, buffer_byte_length, buffer_view_data = BufferUtility.get_embedded_uri(accessor_data)

        buffer_index = self._create_buffer(name=buffer_name, uri=buffer_data, byte_length=buffer_byte_length)

        bv_required_keys = ["name", "target"]
        ac_required_keys = ["name", "bufferview", "byte_offset", "ele_type", "comptype_id", "count", "max_vals",
                            "min_vals", "normalized"]
        for bv, ac in zip(buffer_view_data, accessor_data):
            bv_required_args = {key: ac[key] for key in bv_required_keys if key in ac}
            bv_index = self._create_bufferview(buffer=buffer_index,
                                               byte_offset=bv["byteOffset"],
                                               byte_length=bv["byteLength"],
                                               byte_stride=bv["byteStride"],
                                               **bv_required_args)
            buffer_view_indices.append(bv_index)

            ac_required_args = {key: ac[key] for key in ac_required_keys if key in ac}
            ac_index = self._create_accessor(bufferview=bv_index,
                                             **ac_required_args)
            accessor_indices.append(ac_index)

        return buffer_index, accessor_indices, buffer_view_indices

    def _create_buffer(self, name, uri, byte_length):
        """Add buffer to glTF object

        :return: buffer index
        """
        new_buffer = self._build_buffer(uri=uri, byte_length=byte_length)

        self.buffers.append(new_buffer)

        if name:
            self.buffers_map[name] = self._last_index(self.buffers)

        return self._last_index(self.buffers)

    @staticmethod
    def _build_buffer(uri, byte_length):
        """Build a buffer

        :return: buffer <dict>
        """
        new_buffer = {}
        properties_keys = ["uri", "byteLength"]
        properties_values = [uri, byte_length]
        for key, val in zip(properties_keys, properties_values):
            if val is not None:
                new_buffer[key] = val
        return new_buffer

    def _create_accessor(self, name, bufferview, byte_offset, ele_type, comptype_id, count, max_vals, min_vals,
                         normalized=False):
        """Create an accessor based on an existing bufferView and add the accessor to the glTF object.

        :return: accessor index
        """
        new_accessor = self._build_accessor(bufferview=self._resolve_mapping(inp=bufferview,
                                                                             mapping=self.bufferViews_map),
                                            ele_type=ele_type,
                                            count=count,
                                            max_vals=max_vals,
                                            min_vals=min_vals,
                                            byte_offset=byte_offset,
                                            comptype_id=comptype_id,
                                            normalized=normalized)

        self.accessors.append(new_accessor)

        if name:
            self.accessors_map[name] = self._last_index(self.accessors)

        return self._last_index(self.accessors)

    @staticmethod
    def _build_accessor(bufferview, ele_type, comptype_id, count, max_vals, min_vals, byte_offset, normalized):
        """Build an accessor based on an existing bufferView.

        :return: accessor <dict>
        """
        normalized = None if not normalized else normalized

        new_accessor = {
            "bufferView": bufferview,
            "componentType": comptype_id,
            "type": ele_type,
            "count": count,
        }

        properties_keys = ["byteOffset", "normalized", "max", "min"]
        properties_values = [byte_offset, normalized, max_vals, min_vals]

        for key, val in zip(properties_keys, properties_values):
            if val is not None:
                new_accessor[key] = val

        return new_accessor

    def _create_bufferview(self, name, buffer, byte_length, byte_offset, byte_stride, target=None):
        """Add bufferView to glTF object

        :return: bufferView index
        """
        new_buffer_view = self._build_bufferview(buffer=self._resolve_mapping(inp=buffer, mapping=self.buffers_map),
                                                 target=target,
                                                 byte_length=byte_length,
                                                 byte_offset=byte_offset,
                                                 byte_stride=byte_stride)

        self.bufferViews.append(new_buffer_view)

        if name:
            self.bufferViews_map[name] = self._last_index(self.bufferViews)

        return self._last_index(self.bufferViews)

    @staticmethod
    def _build_bufferview(buffer, target, byte_length, byte_offset, byte_stride):
        """Automatically generate a simple bufferView and add it to the glTF structure.

        Only buffer and byteLength are supported. byteStride and byteOffset are not yet modifiable.
        The name of the bufferView is the same as that of the buffer.

        :return: bufferView <dict>
        """
        new_buffer_view = {
            "buffer": buffer,
            "byteLength": byte_length,
            "byteOffset": byte_offset
        }

        properties_keys = ["target", "byteStride"]
        properties_values = [target, byte_stride]

        for key, val in zip(properties_keys, properties_values):
            if val is not None:
                new_buffer_view[key] = target

        return new_buffer_view

    # ---------------------------------------------------------------------
    # UTILITY METHODS:
    # ---------------------------------------------------------------------

    @staticmethod
    def _resolve_mapping(inp, mapping):
        """Turn all names to their corresponding indices stored in the given mapping.

        :param inp: takes in a list, a dict a literal
        :param mapping: the dict map

        :return: a copy of inp with all accessor names replaced with the corresponding indices
        """
        if not inp:
            return inp
        elif isinstance(inp, dict):
            output = inp.copy()
            for key, value in inp.items():
                if isinstance(value, str):
                    output[key] = mapping[value]
        elif type(inp) == list:
            output = inp.copy()
            output = list(map(lambda x: mapping[x] if isinstance(x, str) else x, output))
        elif type(inp) == int:
            output = inp
        elif isinstance(inp, str):
            output = mapping[inp]
        else:
            raise ValueError("Unexpected input")

        return output

    @staticmethod
    def _last_index(lst):
        return len(lst) - 1

    # ---------------------------------------------------------------------
    # EXPORT METHODS:
    # ---------------------------------------------------------------------

    def to_dict(self):
        """Compile all properties and return a glTF asset <dict>"""
        gltf_asset = {}
        properties_keys = ["scenes", "nodes", "meshes", "buffers", "bufferViews", "accessors", "materials", "asset"]
        properties_vals = [self.scenes, self.nodes, self.meshes, self.buffers, self.bufferViews, self.accessors,
                           self.materials, self.asset]

        for key, val in zip(properties_keys, properties_vals):
            if val:
                gltf_asset[key] = val

        return gltf_asset

    def export_gltf(self, path):
        """Export the glTF asset to a .gltf file
        """
        with open(path, 'w') as gltf_f:
            json.dump(self.to_dict(), gltf_f)
