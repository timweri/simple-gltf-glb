"""Embedded URI encoder

This module includes tools to encode data for use as embedded URI. The output will follow RFC 2397.

Embedded URI used by glTF/glb buffer has to ensure that each component is stored with fixed amount of bytes, determined
by the componentType configuration.

We need to ensure accessor.byteOffset and bufferView.byteStride are multiples of 4. Start of each column of a
matrix accessor must also be aligned to 4-byte boundaries.
"""

import base64
import struct


# TODO: Implement byte alignment compliance
class RFC2397:
    def __init__(self):
        pass

    @staticmethod
    def _get_comptype_formatter(comptype_id):
        COMPONENTTYPE_MAP = {
            5120: 'b',  # char
            5121: 'B',  # unsigned char
            5122: '<h',  # short
            5123: '<H',  # unsigned short
            5125: '<I',  # unsigned int
            5126: '<f'
        }
        return COMPONENTTYPE_MAP[comptype_id]

    @staticmethod
    def _get_compnumber(ele_type):
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
    def _get_comp_bobj(inp, comptype_id):
        """Convert an input into a base32 byte object according to the component type and return the bytes object"""
        out = struct.pack(RFC2397._get_comptype_formatter(comptype_id), inp)

        return out

    @staticmethod
    def get_embedded_uri(data, comptype_id, ele_type):
        """Encode data to a glTF compliant base64-encoded string

        This now encodes a basic list or matrix to a base64 encoding compliant with RFC2397.
        2D matrix will be flattened for iteration.
        However, many features are still not implemented, such as byte striding and byte offsetting.

        :param data: matrix <list> to be converted to a glTF compliant bytearray.
        :param comptype_id: the id that defines the type of each component.
        :param ele_type: a string that specifies the type of each element.
        :return: (str <string>, byte_length <int>) where
                  str: glTF compliant base64-encoded string that represents the input list
                  byte_length: the byte length of the data
        """

        final_barray = 0
        comp_number = RFC2397._get_compnumber(ele_type)

        is_matrix = ele_type[:3] == "MAT"

        for ele in data:
            # If it is a matrix, flatten it
            if is_matrix:
                ele = [comp for row in ele for comp in row]
            for i in range(comp_number):
                bobj = RFC2397._get_comp_bobj(ele if comp_number == 1 else ele[i], comptype_id)
                if not final_barray:
                    final_barray = bytearray(bobj)
                else:
                    final_barray.extend(bobj)

        uri = "data:{mediatype};base64,{data}".format(mediatype="application/octet-stream",
                                                      data=base64.b64encode(final_barray).decode("ascii"))

        return uri, len(final_barray)
