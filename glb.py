from gltf import GLTF
import struct
import json
from rfc2397 import RFC2397


class GLB(GLTF):
    MAGIC = int.from_bytes(b"glTF", byteorder='little')
    VERSION = 2
    JSON_CHUNK_TYPE = b"JSON"
    BIN_CHUNK_TYPE = b"BIN\x00"

    def __init__(self):
        super(GLB, self).__init__()
        self.length = 12
        self.glb_buffer = bytearray()

        glb_buffer = {
            "byteLength": 0
        }
        self.buffers.append(glb_buffer)

    def import_data(self, accessor_data):
        """Add data to the binary chunk. Each set of data generates a pair of accessor and bufferView, which will be
        added to the glb object.

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
        :return: accessor indices, bufferView indices
        """
        accessor_indices = []
        buffer_view_indices = []

        cur_byte_offset = len(self.glb_buffer)

        buffer_bin, buffer_bin_length, buffer_view_data = RFC2397.get_binary_buffer(accessor_data, cur_byte_offset)

        bv_required_keys = ["name", "target"]
        ac_required_keys = ["name", "bufferview", "byte_offset", "ele_type", "comptype_id", "count", "max_vals",
                            "min_vals", "normalized"]
        for bv, ac in zip(buffer_view_data, accessor_data):
            bv_required_args = {key: ac[key] for key in bv_required_keys if key in ac}
            bv_index = self._create_bufferview(buffer=0,
                                               byte_offset=bv["byteOffset"],
                                               byte_length=bv["byteLength"],
                                               byte_stride=bv["byteStride"],
                                               **bv_required_args)
            buffer_view_indices.append(bv_index)

            ac_required_args = {key: ac[key] for key in ac_required_keys if key in ac}
            ac_index = self._create_accessor(bufferview=bv_index,
                                             **ac_required_args)
            accessor_indices.append(ac_index)

        self.glb_buffer.extend(buffer_bin)
        self.buffers[0]["byteLength"] = len(self.glb_buffer)

        return accessor_indices, buffer_view_indices

    def export_glb(self, path):
        """Write the glb file to path
        """
        with open(path, 'wb') as glb_f:
            json_chunk = self._build_json_chunk()
            bin_chunk = self._build_bin_chunk()
            # Build header last since it needs the total byte length
            header_chunk = self._build_header(12 + len(bin_chunk) + len(json_chunk))
            glb_f.write(header_chunk)
            glb_f.write(json_chunk)
            glb_f.write(bin_chunk)

    def _build_header(self, total_length):
        """Build the 12-byte header chunk
        :return: a 12-byte binary object
        """
        header = struct.pack("<III", self.MAGIC, self.VERSION, total_length)

        return header

    def _build_json_chunk(self):
        """Build the padded JSON chunk
        :return: the chunk <bytearray>
        """
        # No GLB-stored buffer if BIN chunk is empty
        if len(self.glb_buffer) == 0:
            self.buffers = self.buffers[1:]
            for view in self.bufferViews:
                view["buffer"] -= 1

        gltf_asset_dict = self.to_dict()
        json_chunk_data = json.dumps(gltf_asset_dict, separators=(',', ':'))
        json_chunk_data_length = len(json_chunk_data)

        json_chunk = bytearray()
        json_chunk.extend(struct.pack("<I", json_chunk_data_length))  # u32int
        json_chunk.extend(struct.pack("<4s", self.JSON_CHUNK_TYPE))  # u32int
        json_chunk.extend(bytes(json_chunk_data, "utf-8"))

        # Pad with trailing spaces (0x20) to satisfy alignment requirements
        if json_chunk_data_length % 4:
            for i in range(4 - json_chunk_data_length % 4):
                json_chunk.extend(b'\x20')

        # Readd the empty GLB-stored buffer
        if len(self.glb_buffer) == 0:
            self.buffers = [{"byteLength":0}] + self.buffers
            for view in self.bufferViews:
                view["buffer"] += 1

        return json_chunk

    def _build_bin_chunk(self):
        """Build the padded Binary chunk
        :return: the chunk <bytearray>
        """
        bin_chunk = bytearray()
        bin_chunk_data_length = len(self.glb_buffer)

        if bin_chunk_data_length != 0:
            bin_chunk.extend(struct.pack("<I", bin_chunk_data_length))  # u32int
            bin_chunk.extend(struct.pack("<4s", self.BIN_CHUNK_TYPE))  # u32int
            bin_chunk.extend(self.glb_buffer)

            # No need to pad with trailing spaces to conform to byte alignment
            # Data is already padded with RFC2397 module

        return bin_chunk
