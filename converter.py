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

    def add_scene(self, name, nodes, nodes_name, mesh_name, mesh):
        """Add a scene with the specified configurations. Return the index of the scene."""
        new_scene = {}

        nodes_ind = Converter._fetch_ind(nodes_name, self.nodes_map)
        nodes_ind += nodes
        new_scene["nodes"] = nodes_ind

        if not mesh:
            mesh_ind = Converter._fetch_ind(mesh_name, self.meshes_map, singleton=True)
            new_scene["mesh"] = mesh_ind
        else:
            new_scene["mesh"] = mesh

        self.scenes.append(new_scene)

        # Update scenes map
        self.scenes_map[name] = len(self.scenes) - 1

        return len(self.scenes) - 1

    def add_mesh(self, name, primitives):
        """Add a mesh with the specified configurations. Return the index of the mesh."""
        new_mesh = {"primitives": primitives if primitives else []}

        self.meshes.append(new_mesh)

        # Update meshes map
        self.meshes_map[name] = len(self.meshes) - 1

        return len(self.meshes) - 1

    def build_add_primitive(self, name, mesh_ind, mesh_name, attributes, indices, material, mode):
        """Create a primitive and add it to the specified mesh. Return the primitive <dict>."""
        assert mesh_ind or mesh_name

        new_primitive = Converter.build_primitive(attributes, indices, material, mode)

        self.add_mesh_primitive(name, new_primitive, mesh_ind, mesh_name)

        self.primitives_map["name"] = len(self.primitives) - 1

        return len(self.primitives) - 1

    @staticmethod
    def build_primitive(attributes, indices, material, mode):
        """Create a primitive and return the primitive <dict>."""

        new_primitive = {}

        if attributes:
            new_primitive["attributes"] = attributes
        if indices:
            new_primitive["indices"] = indices
        if material:
            new_primitive["material"] = material
        if mode:
            new_primitive["mode"] = mode

        return new_primitive

    def add_mesh_primitive(self, name, primitive, mesh_ind, mesh_name):
        """Add a given primitive to a mesh."""

        if mesh_name:
            mesh_ind = self.meshes_map[mesh_name]

        if mesh_ind < len(self.meshes):
            if primitive:
                self.meshes[mesh_ind]["primitives"].append(primitive)
                if primitive not in self.primitives:
                    self.primitives.append(primitive)
                    if name and not self.primitives_map:
                        self.primitives_map[name] = len(self.primitives) - 1
            else:
                primitive_index = self.primitives_map[name]
                self.meshes[mesh_ind]["primitives"].append(self.primitives[primitive_index])

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
    def _fetch_ind(names, ind_map, singleton=False):
        """Finds all indices given by a index map with the specified names and return a list of their indices"""
        ind_out = map(lambda name: ind_map[name], names)
        ind_out = filter(None, ind_out)

        return list(ind_out)[0] if singleton else ind_out
