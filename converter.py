"""Converters to build glTF/glb files

This module contains converters that convert/encode raw geometric data into data that can be used to build a glTF or glb
file. Currently, for the purpose of simple demonstration, it only supports one scene, one node, one mesh, one buffer,...
Basically it does not do much.
"""

from .rfc2397 import RFC2397


# TODO: Make unittest
class Converter:
    def __init__(self):
        # Initialize objects according to the glTF specs
        self.scenes_map = {}
        self.scenes = []
        self.nodes_map = {}
        self.nodes = []
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
        self.asset = {"version": "2.0"}

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

    def _build_scene(self, nodes):
        """Create a scene with the specified properties but do not save it to the object's list of scenes.
        Return scene <dict>
        """
        new_scene = {}

        new_nodes_ind = self._resolve_mapping(inp=nodes, mapping=self.nodes_map)
        new_scene["nodes"] = new_nodes_ind

        return new_scene

    def create_scene(self, name, nodes):
        """Create a scene with the specified properties. Return the index of the scene."""
        new_scene = self._build_scene(nodes=nodes)
        self.scenes.append(new_scene)

        # Update scenes map
        self.scenes_map[name] = self._last_index(self.scenes)

        return self._last_index(self.scenes)

    def add_to_scene(self, scene_id, nodes):
        """Add properties to an existing scene. Return the index of the scene."""
        scene_id = self._resolve_mapping(inp=scene_id, mapping=self.scenes_map)

        scene = self.scenes[scene_id]

        new_nodes_ind = self._resolve_mapping(inp=nodes, mapping=self.nodes_map)

        scene["nodes"] += new_nodes_ind

        return scene_id

    def _build_mesh(self, primitives):
        """Create a mesh with the specified properties but do not save it to the object's list of meshes.
        Return mesh <dict>
        """
        new_mesh = {}

        primitives_ind = self._resolve_mapping(inp=primitives, mapping=self.primitives_map)
        new_primitives = [self.primitives[i] for i in primitives_ind]

        new_mesh["primitives"] = new_primitives

        return new_mesh

    def create_mesh(self, name, primitives):
        """Create a mesh with the specified properties. Return the index of the mesh."""
        new_mesh = self._build_mesh(primitives=primitives)
        self.meshes.append(new_mesh)

        # Update meshes map
        self.meshes_map[name] = self._last_index(self.meshes)

        return self._last_index(self.meshes)

    def add_to_mesh(self, mesh_id, primitives):
        """Add properties to an existing mesh. Return the index of the mesh."""
        mesh_id = self._resolve_mapping(inp=mesh_id, mapping=self.meshes_map)
        mesh = self.meshes[mesh_id]

        new_primitives_ind = self._resolve_mapping(inp=primitives, mapping=self.primitives_map)
        new_primitives = [self.primitives[i] for i in new_primitives_ind]
        mesh["primitives"] += new_primitives

        return mesh_id

    def _build_primitive(self, attributes, indices, material, mode):
        """Create a primitive with the specified properties but do not save it to the object's list of primitives.
        Return primitive <dict>
        """
        new_primitive = {}

        properties_key = ["attributes", "indices", "material", "mode"]
        properties_val = [attributes, indices, material, mode]
        for key, val in properties_key, properties_val:
            if val:
                new_primitive[key] = self._resolve_mapping(inp=val, mapping=self.accessors_map)

        return new_primitive

    def create_primitive(self, name, attributes, indices, material, mode):
        """Create a primitive with the given properties. Return the primitive index."""
        new_primitive = self._build_primitive(attributes=attributes,
                                              indices=indices,
                                              material=material,
                                              mode=mode)

        self.primitives.append(new_primitive)

        self.primitives_map[name] = self._last_index(self.primitives)

        return self._last_index(self.primitives)

    def add_to_primitive(self, primitive_id, attributes, indices, material, mode):
        """Add properties to an existing primitive. Return the primitive index."""
        primitive_id = self._resolve_mapping(inp=primitive_id, mapping=self.primitives_map)

        primitive = self.primitives[primitive_id]

        properties_key = ["attributes", "indices", "material", "mode"]
        properties_val = [attributes, indices, material, mode]
        for key, val in properties_key, properties_val:
            if val:
                primitive[key] = self._resolve_mapping(inp=val, mapping=self.accessors_map)

        return primitive_id

    def build_add_accessor(self, name, data, ele_type, comptype_id, count, max_vals, min_vals, byte_length, uri, target,
                           byte_offset=0, normalized=False):
        """Build an accessor from raw data and generate the appropriate buffer and bufferView.
        Then, add all three properties to the glTF object. All these properties will be stored in the respective lists
        and mapped to the same key (name) in their respective maps.

        :return: (accessor <dict>, bufferView <dict>, buffer <dict>)
        """
        assert ele_type and comptype_id and count or data or (byte_length and uri)

        new_accessor = {
            "byteOffset": byte_offset,
            "componentType": comptype_id,
            "type": ele_type,
            "count": count,
            "normalized": normalized
        }

        properties_names = ["max", "min"]
        properties_values = [max_vals, min_vals]

        for prop_name, prop_val in properties_names, properties_values:
            if prop_val:
                new_accessor[prop_name] = prop_val

        new_buffer, new_buffer_view = self._generate_buffer(name=name,
                                                            data=data,
                                                            ele_type=ele_type,
                                                            comptype_id=comptype_id,
                                                            target=target,
                                                            byte_length=byte_length,
                                                            uri=uri)

        new_accessor["bufferView"] = len(self.bufferViews) - 1
        new_accessor["byteLength"] = new_buffer["byteLength"]

        self.accessors.append(new_accessor)

        if name:
            self.accessors_map[name] = len(self.accessors) - 1

        return new_accessor, new_buffer_view, new_buffer

    def _generate_buffer(self, name, data, ele_type, comptype_id, target, byte_length=None, uri=None):
        """Build a buffer from raw data and generate a corresponding bufferView and add them both to the glTF object.
        If uri is defined, only byte_length and uri are used to build the buffer.
        Otherwise, encode the data according to ele_type and comp_type.

        :return: (buffer <dict>, bufferView <dict>)
        """
        new_buffer = Converter.build_buffer(data=data,
                                            ele_type=ele_type,
                                            comptype_id=comptype_id,
                                            byte_length=byte_length,
                                            uri=uri)

        self.buffers.append(new_buffer)

        if name:
            self.buffers_map[name] = len(self.buffers) - 1

        new_buffer_view = self._generate_bufferview(name=name,
                                                    buffer_index=len(self.buffers) - 1,
                                                    target=target,
                                                    byte_length=new_buffer["byteLength"])

        return new_buffer, new_buffer_view

    @staticmethod
    def build_buffer(data, ele_type, comptype_id, byte_length=None, uri=None):
        """Build a buffer from raw data.
        If uri is defined, only byte_length and uri are used to build the buffer.
        Otherwise, encode the data according to ele_type and comp_type.

        :return: buffer <dict>
        """

        new_buffer = {}

        if byte_length and uri:
            new_buffer["byteLength"] = byte_length
            new_buffer["uri"] = uri
        elif data and ele_type and comptype_id:
            new_buffer["uri"], new_buffer["byteLength"] = RFC2397.get_embedded_uri(data=data,
                                                                                   comptype_id=comptype_id,
                                                                                   ele_type=ele_type)
        else:
            raise ValueError("Illegal arguments")

        return new_buffer

    def _generate_bufferview(self, name, buffer_index, target, byte_length):
        """Automatically generate a simple bufferView and add it to the glTF structure.

        Only buffer and byteLength are supported. byteStride and byteOffset are not yet modifiable.
        The name of the bufferView is the same as that of the buffer.

        :return: bufferView <dict>
        """
        new_buffer_view = {
            "buffer": buffer_index,
            "byteLength": byte_length
        }

        if target:
            new_buffer_view["target"] = target

        self.bufferViews.append(new_buffer_view)

        if name:
            self.bufferViews_map[name] = len(self.bufferViews) - 1

        return new_buffer_view

    @staticmethod
    def _resolve_mapping(inp, mapping):
        """Turn all names to their corresponding indices stored in the given mapping.
        :param inp: takes in a list, a dict a literal
        :param mapping: the dict map
        :return: a copy of inp with all accessor names replaced with the corresponding indices
        """
        if isinstance(inp, dict):
            output = inp.copy()
            for key, value in inp:
                if isinstance(value, str):
                    inp[key] = mapping[value]
        elif type(inp) == list:
            output = list.copy()
            output = list(map(lambda x: mapping[x] if isinstance(x, str) else x, output))
        elif type(inp) == int:
            output = inp
        elif isinstance(inp, str):
            output = mapping[inp]

        return output

    @staticmethod
    def _last_index(lst):
        return len(lst) - 1
