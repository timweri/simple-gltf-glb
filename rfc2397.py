'''Embedded URI encoder

This module includes tools to encode data for use as embedded URI. The output will follow RFC 2397.

Embedded URI used by glTF/glb buffer has to ensure that each component is stored with fixed amount of bytes, determined
by the componentType configuration.

To ensure our data comply with the required byte alignment, we will first convert Python value to bytes objects of the
correct size. Then

'''

import base64
import json
import struct


class RFC2397:
    COMPONENTTYPE_MAP: {
        5120: 'b',      # char
        5121: 'B',      # unsigned char
        5122: '<h',     # short
        5123: '<H',     # unsigned short
        5125: '<I',     # unsigned int
        5126: '<f'
    }

    def __init__(self):
        pass

    @staticmethod
    def converter_5126(inp):
        """Convert a float into a base32 4-byte bytes object and return the bytes object"""
        out = struct.pack('<f', inp)

        return out

    @staticmethod
    def _encode_list(lst, ele_converter):
        """Encode a list to a glTF compliant base64-encoded string

        :param lst: the list of elements to be converted to a glTF compliant bytearray.
        :param ele_converter: A function that returns a glTF compliant bytes object representation of list elements.
                              Each return will have the same byte size.
        :return: glTF compliant base64-encoded string that represents the input list
        """

        final_barray = 0

        for ele in lst:
            bobj = ele_converter(ele)
            if not final_barray:
                final_barray = bytearray(bobj)
            else:
                final_barray.extend(bobj)

        output = base64.b64encode(final_barray)

        return output


lst = [1,0.3,0.2,0,0.9,-0.2]

print(RFC2397.converter_5126(0.2))

print(RFC2397._encode_list(lst,RFC2397.converter_5126))
