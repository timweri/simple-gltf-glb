# Simple GLTF/GLB Builder Demo
This is a simple demo toolkit written in Python 3 to build GLTF/GLB files according to Khronos Group's glTF 2.0 specifications. It was put together to show how to export simple 3D models in glTF/GLB format. It does not support every feature of glTF 2.0. Also, it is not fully comformant nor fully tested.

## Features
- Support basic construction of important glTF asset properties: scenes, nodes, meshes, materials, buffers, bufferViews, accessors
- Support custom naming of objects: implementation can use any string to refer to any created object.
- Generate RFC 2397 conformant Data URI for use as buffer
- Generate conformant GLB container, including GLB-stored buffer
- Export to .gltf/.glb files

## Usage
Documentation of API methods will be properly provided if this demo becomes more complete. For now, to understand how to use API methods, refer to [samples scripts](samples/) to see how to build basic 3D models using this API.
