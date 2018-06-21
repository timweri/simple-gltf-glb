"""Generate data to construct boxes
"""

BASE_BOX_COORS = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0],
                  [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]]
BASE_BOX_COORS_COMPONENTTYPE = 5120  # BYTE (1 byte)
BASE_BOX_COORS_TYPE = "VEC3"


def gen_box(size=[1,1,1], position=[0,0,0],color="red"):
    """Calculate and return a dict with the required configuration to turn a base box into the desired box"""
    translation = [];
