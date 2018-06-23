"""Converters to build glTF/glb files

This module contains converters that convert/encode raw geometric data into data that can be used to build a glTF or glb
file. Currently, for the purpose of simple demonstration, it only supports one scene, one node, one mesh, one buffer,...
Basically it does not do much.
"""

from .rfc2397 import RFC2397


class Converter:
    def __init__(self):
        # Initialize objects according to the glTF specs
        self.scenes_map = {}
        self.scenes = []
        self.nodes_map = {}
        self.nodes = []
        self.meshes_map = {}
        self.meshes = []
        self.buffers_map = {}
        self.buffers = []
        self.bufferViews_map = {}
        self.bufferViews = []
        self.accessors_map = {}
        self.accessors = []
        self.asset = {"version": "2.0"}

    def add_scene(self, name, nodes, nodes_name, mesh_name, mesh):
        """Add a scene with the specified configurations. Return the index of the scene."""
        new_scene = {"name":name}

        nodes_ind = Converter._fetch_ind(nodes_name, self.nodes_map)
        nodes_ind += nodes
        new_scene["nodes"] = nodes_ind;

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
        new_mesh = {"name":name, "primitives": primitives}

        self.meshes.append(new_mesh)

        # Update meshes map
        self.meshes_map[name] = len(self.meshes) - 1

        return len(self.meshes) - 1

    def build_add_primitive(self, mesh_ind, mesh_name, attributes, indices, material, mode):
        """Create a primitive and add it to the specified mesh. Return the primitive."""
        assert mesh_ind or mesh_name

        new_primitive = {}

        if attributes:
            new_primitive["attributes"] = attributes
        if indices:
            new_primitive["indices"] = indices
        if material:
            new_primitive["material"] = material
        if mode:
            new_primitive["mode"] = mode

        if mesh_name:
            mesh_ind = self.meshes_map[mesh_name]

        if mesh_ind < len(self.meshes):
            self.meshes[mesh_ind]["primitives"].append(new_primitive)

        return new_primitive

    def build_primitive(self):
        pass

    @staticmethod
    def _fetch_ind(names, ind_map, singleton = False):
        """Finds all indices given by a index map with the specified names and return a list of their indices"""
        ind_out = map(lambda name: ind_map[name], names)
        ind_out = filter(None, ind_out)

        return ind_out[0] if singleton else ind_out;

    def
