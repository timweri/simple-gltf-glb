"""glTF/GLB buffer generator

This module provides utilities to generate buffer either for use as base64-encoded data URI or as GLB-stored buffer.
The output of embedded data URI will follow RFC 2397. Both embedded data URI and GLB-stored buffer will follow the
required data alignment stated in the glTF/GLB 2.0 specifications.
"""

import base64
import struct


class BufferUtility:
    def __init__(self):
        pass

    @staticmethod
    def _get_comptype_size(comptype_id):
        """:return: the size of each component
        """
        COMPONENTTYPE_SIZE_MAP = {
            5120: 1,
            5121: 1,
            5122: 2,
            5123: 2,
            5125: 4,
            5126: 4
        }
        return COMPONENTTYPE_SIZE_MAP[comptype_id]

    @staticmethod
    def _get_comptype_formatter(comptype_id):
        COMPONENTTYPE_MAP = {
            5120: 'b',  # char
            5121: 'B',  # unsigned char
            5122: 'h',  # short
            5123: 'H',  # unsigned short
            5125: 'I',  # unsigned int
            5126: 'f'  # float
        }
        return COMPONENTTYPE_MAP[comptype_id]

    @staticmethod
    def _get_compnumber(ele_type):
        """:return: number of components in an element
        """
        TYPE_MAP = {
            "SCALAR": 1,
            "VEC2": 2,
            "VEC3": 3,
            "VEC4": 4,
            "MAT2": 4,
            "MAT3": 9,
            "MAT4": 16
        }
        return TYPE_MAP[ele_type]

    @staticmethod
    def _generate_chunk(data, comptype_id, ele_type, offset, vertex_attr):
        """Generate a binary blob with the required data alignment:
            - byteStride = componentType * Type must be a multiple of 4 (if vertex_attr is True)
            - byteLength must be a multiple of 4
            - Pad data with trailing \x00

        :return: (binary data<bytearray>, byteLength<int>, byteStride<int>, byteOffset<int>)

        Note: The returned byteOffset is the offset the next chunk needs to have for the buffer to be valid
        """
        final_barray = bytearray()

        comp_number = BufferUtility._get_compnumber(ele_type)
        comp_size = BufferUtility._get_comptype_size(comptype_id)
        comp_formatter = BufferUtility._get_comptype_formatter(comptype_id)
        ele_size = comp_size * comp_number

        ele_padding_count = (4 - ele_size % 4) % 4 if vertex_attr else 0
        formatter = '<{}{}{}x'.format(comp_number, comp_formatter, ele_padding_count)

        # "SCA", "VEC" or "MAT"
        type_pref = ele_type[:3]

        if type_pref == "SCA":
            for ele in data:
                bobj = struct.pack(formatter, ele)
                final_barray.extend(bobj)
        elif type_pref == "VEC" or type_pref == "MAT":
            for ele in data:
                bobj = struct.pack(formatter, *ele)
                final_barray.extend(bobj)

        byte_stride = ele_size + ele_padding_count if ele_padding_count else None
        byte_length = len(final_barray)

        chunk_padding_count = (4 - byte_length % 4) % 4

        final_barray.extend(struct.pack('{}x'.format(chunk_padding_count)))

        byte_offset = offset + len(final_barray)

        return final_barray, byte_length, byte_stride, byte_offset

    @staticmethod
    def get_binary_buffer(data, byte_offset=0):
        """Encode data to a glTF compliant binary blob

        :param data: an array of dicts of raw data. Each dict corresponds to one bufferView and should include:
                    - data: the raw data to be encoded
                    - ele_type: the type of each element in data
                    - comptype_id: the type of each component of each element in data
                    - vertex_attr: a flag to signal True if the data describes vertex attributes
        :param byte_offset: the initial byteOffset
        :return: (binary buffer blob<bytearray>, byteLength<int>, bufferViews data<list of dicts>)
                  byteLength: the byte length of the data
                  bufferViews data: [{byteLength, byteStride, byteOffset}<dict>, ...] a list of dicts with three
                                    properties to define bufferViews
        """
        buffer_view_data = []
        final_barray = bytearray()
        current_byte_offset = byte_offset

        required_keys = ["data", "ele_type", "comptype_id", "vertex_attr"]
        for view in data:
            view_required_args = {key: view[key] for key in required_keys if key in view}
            view_byte_array, view_byte_length, \
                view_byte_stride, view_byte_offset = BufferUtility._generate_chunk(**view_required_args,
                                                                                   offset=current_byte_offset)

            final_barray.extend(view_byte_array)
            new_buffer_view_data = {
                "byteLength": view_byte_length,
                "byteOffset": current_byte_offset,
                "byteStride": view_byte_stride
            }

            buffer_view_data.append(new_buffer_view_data)

            current_byte_offset = view_byte_offset

        return final_barray, len(final_barray), buffer_view_data

    @staticmethod
    def get_embedded_uri(data):
        """Encode data to a glTF compliant base64-encoded string

        :param data: an array of dicts of raw data. Each dict corresponds to one bufferView and should include:
                    - data: the raw data to be encoded
                    - type: the type of each element in data
                    - componentType: the type of each component of each element in data
                    - vertex_attr: a flag to signal True if the data describes vertex attributes

        :return: (str<string>, byteLength<int>, bufferViews data<list of dicts>) where
                  str: glTF compliant base64-encoded string that represents the input list
                  byteLength: the byte length of the data
                  bufferViews data: [{byteLength, byteStride, byteOffset}<dict>, ...] a list of dicts with three
                                    properties to define bufferViews
        """
        final_barray, byte_length, buffer_view_data = BufferUtility.get_binary_buffer(data)

        uri = "data:{mediatype};base64,{data}".format(mediatype="application/octet-stream",
                                                      data=base64.b64encode(final_barray).decode("ascii"))

        return uri, byte_length, buffer_view_data
