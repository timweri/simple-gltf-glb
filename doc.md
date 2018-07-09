# Cấu Trúc glTF/glB Căn Bản
*Version 2.0*

Doc này dựa hoàn toàn trên thông tin tại doc thông số glTF chính thức tại [đây](https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md). Doc này không phải là bản dịch hoàn chỉnh của doc gốc. Chỉ có thông tin cần thiết cho dự án 3D mới được dịch và demo trong doc. Song ngữ sẽ được dùng để tránh làm mất nghĩa của doc gốc.

GL Transmission Format (glTF) là một cấu trúc trung lập về API dùng để truyền asset lúc chạy. glTF là cầu nối giữa phần mềm thiết kế 3D và ứng dụng 3D bằng cách cung cấp một cấu trúc chuẩn, hiệu quả, dễ phát triển và tính tương thích cao để truyền và tải dữ liệu 3D.

Editors

* Saurabh Bhatia, Microsoft
* Patrick Cozzi, Cesium
* Alexey Knyazev, Individual Contributor
* Tony Parisi, Unity

Khronos 3D Formats Working Group and Alumni

* Remi Arnaud, Starbreeze Studios
* Emiliano Gambaretto, Adobe
* Gary Hsu, Microsoft
* Max Limper, Fraunhofer IGD
* Scott Nagy, Microsoft
* Marco Hutter, Individual Contributor
* Uli Klumpp, Individual Contributor
* Ed Mackey, Individual Contributor
* Don McCurdy, Google
* Norbert Nopper, UX3D
* Fabrice Robinet, Individual Contributor (Previous Editor and Incubator)
* Neil Trevett, NVIDIA
* Jan Paul Van Waveren, Oculus
* Amanda Watson, Oculus

Copyright (C) 2013-2017 The Khronos Group Inc. All Rights Reserved. glTF is a trademark of The Khronos Group Inc.

Author and translator: TimWeri

Original documentation - Last Updated: June 9, 2017
This documentation - Last Updated: June 29, 2018

# Nội Dung

* [Giới thiệu](#introduction)
  * [Motivation](#motivation)
  * [glTF Cơ Bản](#gltf-basics)
  * [Design Goals](#design-goals)
  * [Versioning](#versioning)
  * [Đuôi File và MIME Types](#file-extensions-and-mime-types)
  * [Mã Hoá JSON](#json-encoding)
  * [URIs](#uris)
* [Concepts](#concepts)
  * [Asset](#asset)
  * [Indices và Names](#indices-and-names)
  * [Hệ Toạ Độ và Đơn vị](#coordinate-system-and-units)
  * [Scenes](#scenes)
    * [Hệ Thống Thứ Bậc Node](#nodes-and-hierarchy)
    * [Transformations](#transformations)
  * [Lưu Trũ Dữ Liệu](#binary-data-storage)
    * [Buffers và Buffer Views](#buffers-and-buffer-views)
      * [GLB-stored Buffer](#glb-stored-buffer)
    * [Accessors](#accessors)
        * [Dữ Liệu Floating-Point](#floating-point-data)
        * [Kích Cỡ Phần Tử Của Accessor](#accessor-element-size)
        * [Giới Hạn Accessor](#accessors-bounds)
        * ~~Sparse Accessors~~
    * [Canh Chỉnh Dữ Liệu](#data-alignment)   
  * [Geometry](#geometry)
    * [Meshes](#meshes)
      * [Tangent-space definition](#tangent-space-definition)
      * ~~Morph Targets~~
    * ~~Skins~~
    * [Instantiation](#instantiation)
  * ~~Texture Data~~
  * [Materials](#materials)
    * [Metallic-Roughness Material](#metallic-roughness-material)
    * [Additional Maps](#additional-maps)
    * [Alpha Coverage](#alpha-coverage)
    * [Double Sided](#double-sided)
    * [Default Material](#default-material)
    * [Point and Line Materials](#point-and-line-materials)
  * [Cameras](#cameras)
    * [Projection Matrices](#projection-matrices)
  * ~~Animations~~
  * [Specifying Extensions](#specifying-extensions)
* [GLB File Format Specification](#glb-file-format-specification)
  * [File Extension](#file-extension)
  * [MIME Type](#mime-type)
  * [Binary glTF Layout](#binary-gltf-layout)
    * [Header](#header)
    * [Chunks](#chunks)
      * [Structured JSON Content](#structured-json-content)
      * [Binary Buffer](#binary-buffer)
* [Properties Reference](#properties-reference)
* [Acknowledgments](#acknowledgments)
* [Appendix A: Tangent Space Recalculation](#appendix-a-tangent-space-recalculation)
* [Appendix B: BRDF Implementation](#appendix-b-brdf-implementation)
* [Appendix C: Spline Interpolation](#appendix-c-spline-interpolation)
* [Appendix D: Full Khronos Copyright Statement](#appendix-d-full-khronos-copyright-statement)

# Introduction

The GL Transmission Format (glTF) is an API-neutral runtime asset delivery format.  glTF bridges the gap between 3D content creation tools and modern graphics applications by providing an efficient, extensible, interoperable format for the transmission and loading of 3D content.

## Motivation

*This section is non-normative.*

Traditional 3D modeling formats have been designed to store data for offline use, primarily to support authoring workflows on desktop systems. Industry-standard 3D interchange formats allow for sharing assets between different modeling tools, and within the content pipeline in general. However, neither of these types of formats is optimized for download speed or fast loading at runtime. Files tend to grow very large, and applications need to do a significant amount of processing to load such assets into GPU-accelerated applications.

Applications seeking high performance rarely load modeling formats directly; instead, they process models offline as part of a custom content pipeline, converting the assets into a proprietary format optimized for their runtime application.  This has led to a fragmented market of incompatible proprietary runtime formats and duplicated efforts in the content creation pipeline. 3D assets exported for one application cannot be reused in another application without going back to the original modeling, tool-specific source and performing another proprietary export step.

With the advent of mobile- and web-based 3D computing, new classes of applications have emerged that require fast, dynamic loading of standardized 3D assets. Digital marketing solutions, e-commerce product visualizations, and online model-sharing sites are just a few of the connected 3D applications being built today using WebGL or OpenGL ES. Beyond the need for efficient delivery, many of these online applications can benefit from a standard, interoperable format to enable sharing and reuse of assets between users, between applications, and within heterogeneous, distributed content pipelines.

glTF solves these problems by providing a vendor- and runtime-neutral format that can be loaded and rendered with minimal processing. The format combines an easily parseable JSON scene description with one or more binary files representing geometry, animations, and other rich data. Binary data is stored in such a way that it can be loaded directly into GPU buffers without additional parsing or other manipulation. Using this approach, glTF is able to faithfully preserve full hierarchical scenes with nodes, meshes, cameras, materials, and animations, while enabling efficient delivery and fast loading.

## glTF Basics

*Phần này cung cấp thông tin phụ.*

glTF assets là file JSON có hỗ trợ dữ liệu ngoài. Cụ thể là một glTF asset được tạo nên bởi:

* Một file cấu trúc JSON (`.gltf`) miêu tả một đầy đủ thông tin về scene: node hierarchy, materials, cameras, cùng với dữ liệu về meshes, animations, và những phần khác
* Binary files (`.bin`) dùng để chứa dữ liệu hình học, animation hay những dữ liệu buffer khác
* Hình ảnh (`.jpg`, `.png`) làm texture

Asset dưới dạng khác như hình ảnh có thể được chứa ở file riêng và dùng thông qua URI, chưa sát nhau trong GLB, hoặc gắn thẳng trong JSON bằng [data URIs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs).

glTF asset hợp lệ bắt buộc phải khai báo version.

<p align="center">
<img src="figures/files.png" width="50%" />
</p>

## Design Goals

*This section is non-normative.*

glTF has been designed to meet the following goals:

* *Compact file sizes.* While web developers like to work with clear text as much as possible, clear text encoding is simply not practical for transmitting 3D data due to sheer size. The glTF JSON file itself is clear text, but it is compact and rapid to parse. All large data such as geometry and animations are stored in binary files that are much smaller than equivalent text representations.
* *Fast loading.* glTF data structures have been designed to mirror the GPU API data as closely as possible, both in the JSON and binary files, to reduce load times. For example, binary data for meshes could be viewed as JavaScript Typed Arrays and be loaded directly into GPU buffers with a simple data copy; no parsing or further processing is required.
* *Runtime-independence.* glTF makes no assumptions about the target application or 3D engine. glTF specifies no runtime behaviors other than rendering and animation.
* *Complete 3D scene representation.* Exporting single objects from a modeling package is not sufficient for many applications. Often, authors want to load entire scenes, including nodes, transformations, transform hierarchy, meshes, materials, cameras, and animations into their applications. glTF strives to preserve all of this information for use in the downstream application.
* *Extensibility.* While the initial base specification supports a rich feature set, there will be many opportunities for growth and improvement. glTF defines a mechanism that allows the addition of both general-purpose and vendor-specific extensions.

The design of glTF takes a pragmatic approach. The format is meant to mirror the GPU APIs as closely as possible, but if it did only that, there would be no cameras, animations, or other features typically found in both modeling tools and runtime systems, and much semantic information would be lost in the translation. By supporting these common constructs, glTF content can not only load and render, but it can be immediately usable in a wider range of applications and require less duplication of effort in the content pipeline.

The following are outside the scope of the initial design of glTF:

* *glTF is not a streaming format.* The binary data in glTF is inherently streamable, and the buffer design allows for fetching data incrementally. But there are no other streaming constructs in the format, and no conformance requirements for an implementation to stream data versus downloading it in its entirety before rendering.
* *glTF is not intended to be human-readable,* though by virtue of being represented in JSON, it is developer-friendly.

Version 2.0 of glTF does not define compression for geometry and other rich data. However, the design team believes that compression is a very important part of a transmission standard, and there is already work underway to define compression extensions.

> The 3D Formats Working Group is developing partnerships to define the codec options for geometry compression.  glTF defines the node hierarchy, materials, animations, and geometry, and will reference the external compression specs.

## Versioning

Any updates made to glTF in a minor version will be backwards and forwards compatible. Backwards compatibility will ensure that any client implementation that supports loading a glTF 2.x asset will also be able to load a glTF 2.0 asset. Forwards compatibility will allow a client implementation that only supports glTF 2.0 to load glTF 2.x assets while gracefully ignoring any new features it does not understand.

A minor version update can introduce new features but will not change any previously existing behavior. Existing functionality can be deprecated in a minor version update, but it will not be removed. 

Major version updates are not expected to be compatible with previous versions.

## File Extensions and MIME Types

* `*.gltf` files use `model/gltf+json`
* `*.bin` files use `application/octet-stream`
* Texture files use the official `image/*` type based on the specific image format. For compatibility with modern web browsers, the following image formats are supported: `image/jpeg`, `image/png`.

## JSON Encoding

Để đơn giản hoá việc ứng dụng, glTF áp dụng thêm một số quy tắc cho cấu trúc JSON và mã hoá.

1. JSON phải dùng UTF-8 và không có BOM.
   > **Implementation Note:** glTF exporter không được thêm 1 byte order mark ở đầu chuỗi text JSON. Để tăng sự tương thích, ứng dụng nên làm lơ BOM thay vì báo lỗi. Xem thêm tại [RFC8259, section 8](https://tools.ietf.org/html/rfc8259#section-8).

2. Mọi chuỗi chỉ được dùng ký tự ASCII (trong thuộc tính như names, enums) và phải được viết bằng plain text, e.g., `"buffer"` thay vì `"\u0062\u0075\u0066\u0066\u0065\u0072"`.

   > **Implementation Note:** Làm vậy thì sẽ cho phép ứng dụng không hỗ trợ Unicode hoàn chỉnh dùng glTF. Chuỗi riêng của ứng dụng (như là giá trị của thuộc tính `"name"` hay nội dung của `extras`) có thể dùng bất kỳ ký tự nào. 

3. Key trong JSON phải là duy nhất. Không được dùng key giống nhau trong một đối tượng. Ví dụ, `primitives` không được có hai `"POSITION"`.

## URIs

glTF dùng URIS để trỏ tới buffers và hình ảnh. URIs có thể trỏ đến dữ liệu bên ngoài hoặc có thể chính nó chứa dữ liệu (data URI). Data URI dùng chuẩn dữ liệu([RFC2397](https://tools.ietf.org/html/rfc2397)).
 
 > **Implementation Note:** Data URIs could be [decoded with JavaScript](https://developer.mozilla.org/en-US/docs/Web/API/WindowBase64/Base64_encoding_and_decoding) or consumed directly by web browsers in HTML tags.

Ứng dụng phải hỗ trợ ít nhất tài nguyên đính dạng base64 và tài nguyên ngoài có đường dẫn tương đối (như trong [RFC3986](https://tools.ietf.org/html/rfc3986#section-4.2)). Việc hỗ trợ những loại tài nguyên khác là tuỳ vào ứng dụng. (như là  `http://`).

 > **Implementation Note:** Làm vậy sẽ cho phép ứng dụng quyết định cách tốt nhất để truyền dữ liệu: nếu nhiều asset dùng chung tài nguyên thì chia ra nhiều file tài nguyên sẽ giảm lượng dữ liệu request. Với nhiều file riêng biệt thì ứng dụng có thể load dữ liệu theo thứ tự tối ưu và tránh load dữ liệu  cho phần mà không nhìn thấy được. Nếu ứng dụng ưu tiên việc ít file hơn thì nên đính dữ liệu vào JSON mặc dù làm vậy sẽ tăng kích cỡ file và không hỗ trợ việc kiểm soát thứ tự load. Ngoài ra, có thể dùng GLB container để chứa chung JSON và dữ liệu binary mà không cần base64. Xem [Cấu Trúc File GLB](#glb-file-format-specification) để biết thêm.

# Concepts

<p align="center">
<img src="figures/dictionary-objects.png" /><br/>
The top-level arrays in a glTF asset.  See the <a href="#properties-reference">Properties Reference</a>.
</p>

## Asset

Mỗi glTF asset phải có thuộc tính `asset`. Đây là thuộc tính cấp trên bắt buộc duy nhất để một cấu trúc JSON được cho là một cấu trúc glTF hợp lệ. `asset` phải khai báo version của glTF. `minVersion` cũng có thể được dùng để khai báo phiên bản glTF tương thích thấp nhất. Nhưng thông tin thêm `asset` có thể chứa là `generator` hoặc `copyright`. Ví dụ,

```json
{
    "asset": {
        "version": "2.0",
        "generator": "collada2gltf@f356b99aef8868f74877c7ca545f2cd206b9d3b7",
        "copyright": "2017 (c) Khronos Group"
    }
}
```

> **Implementation Note:** Đầu tiên, ứng dụng nên kiểm tra thuộc tính `minVersion` để đảm bảo tính tương thích. Nếu không có `minVersion` thì sẽ kiểm tra `version` để đảm bảo version quan trọng được hỗ trợ. Ứng dụng load [cấu trúc GLB](#glb-file-format-specification) cũng nên kiểm tra `minVersion` và `version` cả trong chunk JSON và chunk GLB header vì version trong GLB header chỉ là version của container.


## Indices and Names

glTF trỏ tới asset bằng cách dùng index của asset trong array chứa asset đó, e.g., `bufferView` sẽ trỏ tới `buffer` bằng cách dùng index của buffer trong array `buffers`. Ví dụ:

```json
{
    "buffers": [
        {
            "byteLength": 1024,
            "uri": "path-to.bin"
        }
    ],
    "bufferViews": [
        {
            "buffer": 0,
            "byteLength": 512,
            "byteOffset": 0
        }
    ]
}
```

Ở đây, `buffers` và `bufferViews` chỉ có một phần tử. Cái bufferView trỏ tới buffer dùng index của buffer: `"buffer": 0`. Cách này giống với ví dụ sau trong C, Python hay 1 tỷ ngôn ngữ khác: nếu `buffers` là một array và `buffer` là phần tử đầu tiên trong `buffers` thì `bufferViews` sẽ trỏ tới `buffer` bằng `buffers[0]`.

Trong nội tạng của glTF thì indices sẽ được dùng để trỏ qua lại. Nhưng các ứng dụng bên ngoài sẽ dùng _names_ để trỏ/gọi. Bất kỳ glTF object cấp trên nào cũng có thể có một thuộc tính string tên là `name` (hay lắm). Thuộc tính `name` này không nhất thiết là duy nhất vì tuỳ vào cái ứng dụng bên ngoài.

glTF dùng [camel case](http://en.wikipedia.org/wiki/CamelCase) `likeThis` để đặt tên thuộc tính. Camel case là cách đặt tên phổ biến trong JSON và WebGL.

## Coordinate System and Units

glTF dùng hệ thống toạ độ bên phải. Tức là cross product của +X và +Y sẽ trả về +Z. +Y là hướng lên. Mặt trước của glTF asset faces là +Z.

![](figures/coordinate-system.png)

Đơn vị của khoáng cách tuyến tính là mét.

Mọi góc sẽ được viết bằng radians.

Hướng xoay dương là ngược chiều kim đông hồ.


[Node transformations](#transformations) và [animation channel paths](#animations) sẽ dưới dạng 3D vectors hoặc quaternions với quy ước sau:

* translation: 3D vector chứa translation dọc theo 3 trục x, y và z.
* rotation: quaternion (x, y, z, w), trong đó w là vô hướng.
* scale: 3D vector chứa scaling factors dọc theo 3 trục x, y và z.



## Scenes

glTF asset chứa từ 0 *scenes* trở lên. Một scene là một tập hợp các object thấy được để render. Scenes được định nghĩa trong một cái `scenes` array. Một thuốc tính thêm , `scene` (không có 's'), dùng để khai báo scene nào sẽ được hiển thị trước lúc load.

Tất cả mọi nodes trong `scene.nodes` array phải là node gốc (xem phần tiếp theo để biết thêm).

Khi mà `scene` bị bỏ trống thì sẽ không hiển thị gì cả lúc load.

> **Lưu ý:** Làm như vậy sẽ cho phép ứng dụng dùng glTF assets làm thư viện chứa nhiều thứ độc lập như là material hoặc mesh.

Đây là một glTF asset ví dụ chưa một scene. Một scene này chỉ chứa một node.

```json
{
    "nodes": [
        {
            "name": "singleNode"
        }
    ],
    "scenes": [
        {
            "name": "singleScene",
            "nodes": [
                0
            ]
        }
    ],
    "scene": 0
}
```

### Hệ Thóng Thứ Bậc Node

glTF asset có thể khai báo *nodes*. Nodes là những objects tạo nên một scene để render.

Nodes có thể chứa thuộc tính `name` không bắt buộc.

Nodes cũng có thể chứ những thuộc tính transform, được nói trong phần sau.

Nodes được tổ chức dưới cha-con hierarchy, còn được gọi là *node hierarchy*. *root node* là node không có cha (mồ côi).

Node hierarchy được khai dùng thuộc tính `children` như sau:

```json
{
    "nodes": [
        {
            "name": "Car",
            "children": [1, 2, 3, 4]
        },
        {
            "name": "wheel_1"
        },
        {
            "name": "wheel_2"
        },
        {
            "name": "wheel_3"
        },
        {
            "name": "wheel_4"
        }        
    ]
}
```

Node `Car` có bốn node con. Mỗi node con này có thể có node con của riêng chúng.

> For Version 2.0 conformance, the glTF node hierarchy is not a directed acyclic graph (DAG) or *scene graph*, but a disjoint union of strict trees. That is, no node may be a direct descendant of more than one node. This restriction is meant to simplify implementation and facilitate conformance.

### Transformations

Bất kỳ node nào cũng có thể khai báo transformation cục bộ bằng một trong hai cách: thêm thuộc tính `matrix` hoặc bất kỳ thuộc tính nào trong các thuộc tính `translation`, `rotation`, và `scale` (*TRS properties*). `translation` và `scale` là giá trị `FLOAT_VEC3` trong trục toạ độ cục bộ. `rotation` là giá trị `FLOAT_VEC4` unit quaternion, `(x, y, z, w)` trong trục toạ độ cục bộ.

`matrix` phải rã ra thành TRS được. Tức là ma trận transformation không được skew hoặc shear.

Thuộc tính TRS sẽ đuợc dùng để tính ma trận biến dạng theo công thức `T * R * S`; scale, rotate rồi translate.

Khi mà dùng target để transform node (trỏ từ `animation.channel.target`) thì chỉ được dùng TRS; không được dùng `matrix`.

> **Implementation Note:** Nếu mà transform có giá trị âm thì winding order của mesh triangle sẽ đổi hướng. Làm vậy sẽ hỗ trợ scale âm dùng trong mirroring geometry.

> **Implementation Note:** Non-invertible transformations (transformation mà không làm ngược lại được) (e.g., scale một trục toạ độ thành 0) có thể dẫn đến  artifacts trong lighting và visibility.

Trong ví dụ dưới, node tên `Box` định nghĩa rotation với translation không mặc định.

```json
{
    "nodes": [
        {
            "name": "Box",
            "rotation": [
                0,
                0,
                0,
                1
            ],
            "scale": [
                1,
                1,
                1
            ],
            "translation": [
                -17.7082,
                -11.4156,
                2.0922
            ]
        }
    ]
}
```

Ví dụ tiếp theo định nghĩa transformation cho một node được gắn camera dùng thuộc tính `matrix` thay vì TRS.

```json
{
    "nodes": [
        {
            "name": "node-camera",
            "camera": 1,
            "matrix": [
                -0.99975,
                -0.00679829,
                0.0213218,
                0,
                0.00167596,
                0.927325,
                0.374254,
                0,
                -0.0223165,
                0.374196,
                -0.927081,
                0,
                -0.0115543,
                0.194711,
                -0.478297,
                1
            ]
        }
    ]
}
```

## Binary Data Storage

### Buffers and Buffer Views

*buffer* là dữ liệu chứa dưới dạng một cục binary blob. Buffer có thể chứa chung dữ liệu về hình học, animation với skins.

Binary blob cho phép tối ưu hoá việc tạo GPU buffer và texture vì không cần parse gì thêm, ngoại trừ việc xả nén. Asset cỏ thể chứa bao nhiêu file buffer cũng được để dễ ứng dụng trong nhiều trường hợp khác nhau.

Dữ liệu buffer theo thứ tự little endian.

Mọi buffer được chứa trong `buffers` array.

Ví dụ sau định nghĩa một buffer. Thuộc tính `byteLength` miêu tả kích cỡ của file buffer. Thuộc tính `uri` là URI trỏ đến dữ liệu buffer. Dữ liệu buffer cũng có thể được chứa thẳng trong data URI trong file glTF dùng mã hoá base64.

```json
{
   "buffers": [
       {
           "byteLength": 102040,
           "uri": "duck.bin"
       }
   ]
}
```

Một *bufferView* là một tập hợp dữ liệu con trong một buffer, định nghĩa dùng một thuộc tính offset integer `byteOffset` tương đối với buffer, và thuộc tính `byteLength` miêu tả kích cỡ của cái buffer view.

Khi buffer view chứa dữ liệu indices hoặc attributes của vertex, dữ liệu đó phải là thứ duy nhất trong buffer view. Có nghĩa là không được chứa nhiều hơn 1 loại dữ liệu trong buffer view.

> **Implementation Note:** Làm vậy cho phép việc tải thẳng dữ liệu vô GPU mà không cần xử lý thêm. Khi `bufferView.target` được khai, lúc chạy phải dùng nó để biết data dùng như thế nào, không thì phải xem accessor của mesh để biết.

Ví dụ sau định nghĩa 2 buffer views: Cái đầu tiên là một ELEMENT_ARRAY_BUFFER, chứa indices của một set tam giác có đánh số, và cái thứ hai là là một ARRAY_BUFFER chứa dữ liệu vertex cho set tam giác.

```json
{
    "bufferViews": [
        {
            "buffer": 0,
            "byteLength": 25272,
            "byteOffset": 0,
            "target": 34963
        },
        {
            "buffer": 0,
            "byteLength": 76768,
            "byteOffset": 25272,
            "byteStride": 32,
            "target": 34962
        }
    ]
}
```

Buffer view có thể có thuộc tính `byteStride`. Nó dùng để khai báo khoảng cách (tính bằng byte) giữa hai phần tử cạnh nhau. Cái này chỉ cần khi buffer view chứa vertex attributes.

Buffer với buffer view không chứa thông tin về type. Nó chỉ khai báo dữ liệu nguyên từ file. Những đối tượng trong glTF (mesh, skin, animation) đọc dữ liệu này thông qua *accessor*.

#### GLB-stored Buffer

glTF asset có thể dùng file container GLB để đóng gói tất cả mọi thứ vô một file. glTF buffer trỏ tới `BIN` chunk chứa bằng GLB không được khai báo `buffer.uri`, và buffer đó phải là phần tử đầu tiên của `buffers` array; kích cỡ byte của `BIN` chunk được phép lớn hơn `buffer.byteLength` trong khai trong JSON là 3 bytes để hỗ trợ việc pad GLB.

> **Implementation Note:**  Không bắt kích cỡ của `BIN` chunk và kích cỡ khai trong buffer bằng nhau thì đơn giản hoá việc chuyển từ glTF sang GLB một tí: không cần cập nhật `buffer.byteLength` sau khi pad GLB.

Trong ví dụ sau, cái buffer đầu tiên trỏ đến dữ liệu chứa bằng GLB. Cái buffer thứ hai trỏ đến dữ liệu bên ngoài.

```json
{
    "buffers": [
        {
            "byteLength": 35884
        },
        {
            "byteLength": 504,
            "uri": "external.bin"
        }
  ]
}
```

Xem [Cấu Trúc File GLB](#glb-file-format-specification) để biết thêm.

### Accessors

Mọi dữ liệu lớn dùng trong mesh, skin, và animation được lưu trong buffer và đọc bằng accessor.

Một *accessor* định nghĩa phương thức đọc dữ liệu trong `bufferView` dưới dạng typed arrays. Accessor khai báo type của đơn vị trong dữ liệu (như là `5126 (FLOAT)`) và type của dữ liệu (như là `VEC3`). Hai thông tin này gộp lại sẽ định nghĩa toàn diện type của dữ liệu cho mỗi phần tử trong mảng. Accessor cũng khai báo vị trí của dữ liệu trong `bufferView` và kích cỡ của dự liệu trong thuộc tính `byteOffset` và `count`. `count` miêu tả số lượng phần tử chứa trong `bufferView`, *chứ không phải* là kích cỡ byte. Một số ví dụ của phần tử là vertex indices, vertex attributes, animation keyframes,...

Mọi accessors đều được chứa trong `accessors` array.

Ví dụ sau dùng 2 accessor, cái đầu là accessor đọc indices của primitive, cái thứ hai là access đọc vector chứa 3 giá trị float để đọc dữ liệu toạ độ của primitive.

```json
{
    "accessors": [
        {
            "bufferView": 0,
            "byteOffset": 0,
            "componentType": 5123,
            "count": 12636,
            "max": [
                4212
            ],
            "min": [
                0
            ],
            "type": "SCALAR"
        },
        {
            "bufferView": 1,
            "byteOffset": 0,
            "componentType": 5126,
            "count": 2399,
            "max": [
                0.961799,
                1.6397,
                0.539252
            ],
            "min": [
                -0.692985,
                0.0992937,
                -0.613282
            ],
            "type": "VEC3"
        }
    ]
}
```

#### Floating-Point Data

Dữ liệu dạng `5126 (FLOAT)` componentType phải dùng quy ước IEEE-754. 

Giá trị như `NaN`, `+Infinity`, và `-Infinity` là không hợp lệ.

#### Accessor Element Size

Bảng sau có thể được dùng để tính kích cỡ mỗi phần tử được đọc bởi accessor.

| `componentType` | Kích cỡ theo byte |
|:---------------:|:-------------:|
| `5120` (BYTE) | 1 |
| `5121`(UNSIGNED_BYTE) | 1 |
| `5122` (SHORT) | 2 |
| `5123` (UNSIGNED_SHORT) | 2 |
| `5125` (UNSIGNED_INT) | 4 |
| `5126` (FLOAT) | 4 |

| `type` | Số lượng component |
|:------:|:--------------------:|
| `"SCALAR"` | 1 |
| `"VEC2"` | 2 |
| `"VEC3"` | 3 |
| `"VEC4"` | 4 |
| `"MAT2"` | 4 |
| `"MAT3"` | 9 |
| `"MAT4"` | 16 |

Kích cỡ một phần tử, theo byte, được tính như sau:
`(kích cỡ theo bytes của 'componentType') * (số component được đĩnh nghĩa với 'type')`.

Ví dụ:

```json
{
    "accessors": [
        {
            "bufferView": 1,
            "byteOffset": 7032,
            "componentType": 5126,
            "count": 586,
            "type": "VEC3"
        }
    ]
}
```

Trong accessor này, `componentType` là `5126` (FLOAT) nên mỗi component là 4 byte. `type` là `"VEC3"`, nên có 3 component.  Kích cỡ của một phần tử là 12 byte (`4 * 3`).

#### Giới Hạn Accessor

Thuộc tính `accessor.min` và `accessor.max` là array chứa giá trị min và max của mỗi component theo thứ tự. Type của các giá trị min max này sẽ theo `componentType` của accessor. Tức là nếu `componentType` là integer thì min max cũng là integer.

> **Implementation Note:** Nếu dùng JavaScript, nên dùng `Math.fround` để đổi số dạng floating-point doubles đọc từ JSON thành dạng single precision khi `componentType` là `5126` (FLOAT).

Mặc dù không bắt buộc phải có min max trong accessor trong nhiều trường hợp, có những trường hợp đặc biệt phải cần min max. Xem những phần khác để hiểu thêm.

#### Canh Chỉnh Data

Offset của một `accessor` tương đối với một `bufferView` (`accessor.byteOffset`) và offset của một `accessor` tương đối với một `buffer` (`accessor.byteOffset + bufferView.byteOffset`) phải là bội số của kích cỡ của component type trong accessor.

Khi `byteStride` không được khai báo trong `bufferView` thì có nghĩa là phần tử trong accessor được đóng gần kề nhau. Tức là `byteStride` bằng với kích cỡ của mỗi phần từ. Khi `byteStride` được khai báo, nó phải là bội số của kích cỡ của component type trong accessor. Bắt buộc phải có `byteStride` nếu nhiều hơn một accessor dùng chung một `bufferView`.

Mỗi `accessor` phải nhét vừa trong `bufferView` của nó. Tức là `accessor.byteOffset + STRIDE * (accessor.count - 1) + SIZE_OF_ELEMENT` nhỏ hơn hoặc bằng `bufferView.length`.

Vì mục tiêu tối ưu, mỗi phần tử của vertex attribute phải được cân chỉnh theo khoảng cách 4-byte trong `bufferView`. Tức là `accessor.byteOffset` và `bufferView.byteStride` phải là bội số của 4 để đảm bảo đầu và đuôi của `accessor` và của mỗi phần từ bắt đầu và kết thúc ở byte có thứ tự là bội số của 4.

Accessor đọc dữ liệu dạng ma trận thì sẽ đọc dọc theo cột (column-major order); Đầu của mỗi cột phải được canh theo byte bội số của 4. Để được vậy, có ba tổ hợp `type`/`componentType` cần canh chỉnh đặc biệt:

**MAT2, 1-byte components**
```
| 00| 01| 02| 03| 04| 05| 06| 07| 
|===|===|===|===|===|===|===|===|
|m00|m10|---|---|m01|m11|---|---|
```

**MAT3, 1-byte components**
```
| 00| 01| 02| 03| 04| 05| 06| 07| 08| 09| 0A| 0B|
|===|===|===|===|===|===|===|===|===|===|===|===|
|m00|m10|m20|---|m01|m11|m21|---|m02|m12|m22|---|
```

**MAT3, 2-byte components**
```
| 00| 01| 02| 03| 04| 05| 06| 07| 08| 09| 0A| 0B| 0C| 0D| 0E| 0F| 10| 11| 12| 13| 14| 15| 16| 17|
|===|===|===|===|===|===|===|===|===|===|===|===|===|===|===|===|===|===|===|===|===|===|===|===|
|m00|m00|m10|m10|m20|m20|---|---|m01|m01|m11|m11|m21|m21|---|---|m02|m02|m12|m12|m22|m22|---|---|
```

Chỉ cần canh cho đầu mỗi cột thôi. Đuôi không cần quan tâm nếu hết dữ liệu.

> **Implementation Note:** Trong JavaScript, làm vậy thì lúc chạy sẽ tối ưu hoá việc tạo một ArrayBuffer từ `buffer` của glTF hoặc tạo từng ArrayBuffer cho mỗi `bufferView`, rồi dùng một `accessor` để biến một typed array view (như là `Float32Array`) thành một ArrayBuffer mà không cần copy vì byte offset của typed array view đã là bội số của kích cỡ của type sẵn rồi (ví dụ như là bội số của `4` nếu dùng `Float32Array`)

Hãy xem ví dụ sau:

```json
{
    "bufferViews": [
        {
            "buffer": 0,
            "byteLength": 17136,
            "byteOffset": 620,
            "target": 34963
        }
    ],
    "accessors": [
        {
            "bufferView": 0,
            "byteOffset": 4608,
            "componentType": 5123,
            "count": 5232,
            "type": "SCALAR"
        }
    ]
}
```
Một cách đọc dữ liệu binary ở trên là như sau:

```js
var typedView = new Uint16Array(buffer, accessor.byteOffset + accessor.bufferView.byteOffset, accessor.count);
```

Kích cỡ của component type của accessor là 2 byte (`componentType` là unsigned short). `byteOffset` của accessor chia hết cho 2. Tương tự, offset của accessor tương đối với buffer `0` là `5228` (`620 + 4608`), cũng chia hết cho 2.


## Geometry

Bất kỳ node nào cũng chứa được một mesh, khai báo dùng thuộc tính `mesh`. Mesh có thể gắn skin dùng thông tin từ đối tượng `skin`. Mesh cũng có thể dùng morth target. Nhưng vì dự án chưa cần nên tạm thời bỏ qua hai phần này.

### Meshes

Trong glTF, mesh được định nghĩa là một array chứa *primitives*. Primitives là dữ liệu mà GPU dùng để vẽ (GPU draw call). Primitives có thể bao gồm một hoặc nhiều `attributes`, tương đương với vertex attributes dùng trong draw call. Primitives có dùng index thì sẽ khai báo thuộc tính `indices`. Attributes với indices chứa con trỏ đến accessor chứa dữ liệu cần thiết. Mỗi primitive chứa thông tin về một material và một primitive type tương đương với GPU primitive type (ví dụ như set tam giác).

> **Implementation note:** Chẻ một mesh thành nhiều *primitives*cho phép việc kiểm soát số lượng indices được vẽ cho mỗi draw call.

Nếu `material` bỏ trống thì sẽ dùng [material mặc định](#default-material).

Ví dụ sau định nghĩa một mesh chứa một set primitive tam giác.

```json
{
    "meshes": [
        {
            "primitives": [
                {
                    "attributes": {
                        "NORMAL": 23,
                        "POSITION": 22,
                        "TANGENT": 24,
                        "TEXCOORD_0": 25
                    },
                    "indices": 21,
                    "material": 3,
                    "mode": 4
                }
            ]
        }
    ]
}
```

Mỗi attribute được định nghĩa là thuộc tính của đối tượng `attributes`. Tên của mỗi thuộc tính attribute sẽ là tương với những giá trị định sẵn để đánh dấu các vertex attribute khác nhau, như là `POSITION`. Giá trị của thuộc tính attribute sẽ là index của một accessor chứa dữ liệu cần thiết.

Những tên hợp lệ của một thuộc tính attribute bao gồm `POSITION`, `NORMAL`, `TANGENT`, `TEXCOORD_0`, `TEXCOORD_1`, `COLOR_0`, `JOINTS_0`, và `WEIGHTS_0`. Những thuộc tính riêng của ứng dụng phải bắt đầu bằng `_` như là `_TEMPERATURE`.

Những type, component type hợp, và mỗi thuộc tính attribute hợp lệ được liệt kê bên dưới.

|Tên|Accessor Type(s)|Component Type(s)|Miêu tả|
|----|----------------|-----------------|-----------|
|`POSITION`|`"VEC3"`|`5126`&nbsp;(FLOAT)|Vị trí XYZ của vertex|
|`NORMAL`|`"VEC3"`|`5126`&nbsp;(FLOAT)|XYZ Normal của vertex đã được normalized|
|`TANGENT`|`"VEC4"`|`5126`&nbsp;(FLOAT)|XYZW vertex tangents where the *w* component is a sign value (-1 or +1) indicating handedness of the tangent basis|
|`TEXCOORD_0`|`"VEC2"`|`5126`&nbsp;(FLOAT)<br>`5121`&nbsp;(UNSIGNED_BYTE)&nbsp;normalized<br>`5123`&nbsp;(UNSIGNED_SHORT)&nbsp;normalized|UV texture coordinates for the first set|
|`TEXCOORD_1`|`"VEC2"`|`5126`&nbsp;(FLOAT)<br>`5121`&nbsp;(UNSIGNED_BYTE)&nbsp;normalized<br>`5123`&nbsp;(UNSIGNED_SHORT)&nbsp;normalized|UV texture coordinates for the second set|
|`COLOR_0`|`"VEC3"`<br>`"VEC4"`|`5126`&nbsp;(FLOAT)<br>`5121`&nbsp;(UNSIGNED_BYTE)&nbsp;normalized<br>`5123`&nbsp;(UNSIGNED_SHORT)&nbsp;normalized|RGB or RGBA vertex color|
|`JOINTS_0`|`"VEC4"`|`5121`&nbsp;(UNSIGNED_BYTE)<br>`5123`&nbsp;(UNSIGNED_SHORT)|See [Skinned Mesh Attributes](#skinned-mesh-attributes)|
|`WEIGHTS_0`|`"VEC4`|`5126`&nbsp;(FLOAT)<br>`5121`&nbsp;(UNSIGNED_BYTE)&nbsp;normalized<br>`5123`&nbsp;(UNSIGNED_SHORT)&nbsp;normalized|See [Skinned Mesh Attributes](#skinned-mesh-attributes)|

`POSITION` accessor **phải** khai báo thuộc tính `min` và `max`.

Tên của attribute `TEXCOORD`, `COLOR`, `JOINTS`, và `WEIGHTS` phải dưới dạng `[semantic]_[set_index]`, ví dụ như `TEXCOORD_0`, `TEXCOORD_1`, `COLOR_0`. Ứng dụng phải hỗ trợ ít nhất 2 bộ toạ độ UV texture, 1 vertex color, và 1 bộ joints/weights. Extension có thể thêm tên thuộc tính, accessor types, và/hoặc accessor component types.

Mọi index trong index attribute phải bắt đầu bằng 0 và liền kề nhau: `TEXCOORD_0`, `TEXCOORD_1`, ...

> **Implementation note:** Mỗi primitive là tương ứng với 1 WebGL draw call (engine tất nhiên sẽ có quyền chẻ draw call ra nhiều mảnh) corresponds to one WebGL draw call (engines are, of course, free to batch draw calls). When a primitive's `indices` property is defined, it references the accessor to use for index data, and GL's `drawElements` function should be used. When the `indices` property is not defined, GL's `drawArrays` function should be used with a count equal to the count property of any of the accessors referenced by the `attributes` property (they are all equal for a given primitive).

> **Implementation note:** When normals are not specified, client implementations should calculate flat normals.

> **Implementation note:** When tangents are not specified, client implementations should calculate tangents using default MikkTSpace algorithms.  For best results, the mesh triangles should also be processed using default MikkTSpace algorithms.

> **Implementation note:** Vertices of the same triangle should have the same `tangent.w` value. When vertices of the same triangle have different `tangent.w` values, tangent space is considered undefined.

> **Implementation note:** When normals and tangents are specified, client implementations should compute the bitangent by taking the cross product of the normal and tangent xyz vectors and multiplying against the w component of the tangent: `bitangent = cross(normal, tangent.xyz) * tangent.w`

### Instantiation

A mesh is instantiated by `node.mesh` property. The same mesh could be used by many nodes, which could have different transformations. For example:

```json
{
    "nodes": [
        {
            "mesh": 11
        },
        {
            "mesh": 11,
            "translation": [
                -20,
                -1,
                0
            ]            
        }
    ]
}

```

A Morph Target is instanced within a node using:
- The Morph Target referenced in the `mesh` property.
- The Morph Target `weights` overriding the `weights` of the Morph Target referenced in the `mesh` property.
The example below instatiates a Morph Target with non-default weights.

```json
{
    "nodes": [
        {
            "mesh": 11,
            "weights": [0, 0.5]
        }
    ]
}
```

A skin is instanced within a node using a combination of the node's `mesh` and `skin` properties. The mesh for a skin instance is defined in the `mesh` property. The `skin` property contains the index of the skin to instance.

```json
{
    "skins": [
        {
            "inverseBindMatrices": 29,
            "joints": [1, 2] 
        }
    ],
    "nodes": [
        {
            "name":"Skinned mesh node",
            "mesh": 0,
            "skin": 0
        },
        {
            "name":"Skeleton root joint",
            "children": [2],
            "rotation": [
                0,
                0,
                0.7071067811865475,
                0.7071067811865476
            ],
            "translation": [
                4.61599,
                -2.032e-06,
                -5.08e-08
            ]
        },
        {
            "name":"Head",
            "translation": [
                8.76635,
                0,
                0
            ]
        }
    ]
}
```

## Texture Data

glTF separates texture access into three distinct types of objects: Textures, Images, and Samplers.

### Textures

All textures are stored in the asset's `textures` array. A texture is defined by an image resource, denoted by the `source` property and a sampler index (`sampler`).

```json
{
    "textures": [
        {
            "sampler": 0,
            "source": 2
        }
    ]
}
```

> **Implementation Note** glTF 2.0 supports only 2D textures.

### Images

Images referred to by textures are stored in the `images` array of the asset. 

Each image contains one of
- a URI to an external file in one of the supported images formats, or
- a URI with embedded base64-encoded data, or
- a reference to a `bufferView`; in that case `mimeType` must be defined.

The following example shows an image pointing to an external PNG image file and another image referencing a `bufferView` with JPEG data.

```json
{
    "images": [
        {
            "uri": "duckCM.png"
        },
        {
            "bufferView": 14,
            "mimeType": "image/jpeg" 
        }
    ]
}
```
> **Implementation Note:** When image data is provided by `uri` and `mimeType` is defined, client implementations should prefer JSON-defined MIME Type over one provided by transport layer.

The origin of the UV coordinates (0, 0) corresponds to the upper left corner of a texture image.
This is illustrated in the following figure, where the respective UV coordinates are shown for all four corners of a normalized UV space:
<p align="center">
<img src="figures/texcoords.jpg" /><br/>
</p>

Any colorspace information (such as ICC profiles, intents, etc) from PNG or JPEG containers must be ignored.

> **Implementation Note:** This increases portability of an asset, since not all image decoding libraries fully support custom color conversions. To achieve correct rendering, WebGL runtimes must disable such conversions by setting `UNPACK_COLORSPACE_CONVERSION_WEBGL` flag to `NONE`.

### Samplers

Samplers are stored in the `samplers` array of the asset. Each sampler specifies filter and wrapping options corresponding to the GL types. The following example defines a sampler with linear mag filtering, linear mipmap min filtering, and repeat wrapping in S (U) and T (V).


```json
{
    "samplers": [
        {
            "magFilter": 9729,
            "minFilter": 9987,
            "wrapS": 10497,
            "wrapT": 10497
        }
    ]
}
```

> **Default Filtering Implementation Note:** When filtering options are defined, runtime must use them. Otherwise, it is free to adapt filtering to performance or quality goals.

> **Mipmapping Implementation Note**: When a sampler's minification filter (`minFilter`) uses mipmapping (`NEAREST_MIPMAP_NEAREST`, `NEAREST_MIPMAP_LINEAR`, `LINEAR_MIPMAP_NEAREST`, or `LINEAR_MIPMAP_LINEAR`), any texture referencing the sampler needs to have mipmaps, e.g., by calling GL's `generateMipmap()` function.

> **Non-Power-Of-Two Texture Implementation Note**: glTF does not guarantee that a texture's dimensions are a power-of-two.  At runtime, if a texture's width or height is not a power-of-two, the texture needs to be resized so its dimensions are powers-of-two if the `sampler` the texture references
> * Has a wrapping mode (either `wrapS` or `wrapT`) equal to `REPEAT` or `MIRRORED_REPEAT`, or
> * Has a minification filter (`minFilter`) that uses mipmapping (`NEAREST_MIPMAP_NEAREST`, `NEAREST_MIPMAP_LINEAR`, `LINEAR_MIPMAP_NEAREST`, or `LINEAR_MIPMAP_LINEAR`).

## Materials

glTF định nghĩa materials bằng những bộ parameter thông dụng trong Physically-Based Rendering (PBR). Cụ thể là glTF dùng model metallic-roughness. Dùng chuẩn này sẽ đảm bảo là file glTF được render một cách đồng đều trên nhiều nền tảng.

<p><img src="figures/materials.png" /></p>

### Metallic-Roughness Material 

Mọi parameter liên quan đến model metallic-roughness material được định nghĩa dưới thuộc tính `pbrMetallicRoughness` của đối tượng `material`. Đây là ví dụ của cách vẽ material vàng (gold) bằng model này.

```json
{
    "materials": [
        {
            "name": "gold",
            "pbrMetallicRoughness": {
                "baseColorFactor": [ 1.000, 0.766, 0.336, 1.0 ],
                "metallicFactor": 1.0,
                "roughnessFactor": 0.0
            }
        }
    ]
}
```

Model metallic-roughness material được định nghĩa bởi những thuộc tính sau:
* `baseColor` - Màu gốc của material
* `metallic` - Độ giống kim loại của material
* `roughness` - Độ nhám của material

Màu gốc có hai cách đọc tuỳ vào giá trị của độ kim loại. Khi mà material là kim loại, màu gốc là giá trị phản quang vuông góc với bề mặt (F0). Khi mà material là phi kim, màu gốc là reflected diffuse color của material. Model này không cho phép khai bảo giá trị F0 cho phi kim, và giá trị tuyến tính là 4% (0.04) sẽ được dùng.

Giá trị của mỗi thuộc tính (`baseColor`, `metallic`, `roughness`) có thể được định nghĩa dùng factor hoặc texture. Thuộc tính `metallic` và `roughness` được đóng chung trong một texture gọi là `metallicRoughnessTexture`. Nếu không có texture thì mọi component của texture trong material model này sẽ có giá trị là `1.0`. Nếu cả factor và texture đều được khai báo thì cái factor sẽ được dùng làm muliplier tuyến tính cho những gía trị texture tương ứng. `baseColorTexture` nằm trong không gian sRGB và phải được chuyển đổi sang không gian tuyến tính trước khi tính toán.

Ví dụ, giả sử giá trị `[0.9, 0.5, 0.3, 1.0]` thuộc không gian tuyến tính được lấy từ một RGBA `baseColorTexture`, và giả sử `baseColorFactor` là `[0.2, 1.0, 0.7, 1.0]`.
Kết quả sẽ là 
```
[0.9 * 0.2, 0.5 * 1.0, 0.3 * 0.7, 1.0 * 1.0] = [0.18, 0.5, 0.21, 1.0]
```

Những phương trình sau ví dụ cho cách tính input của hàm bidirectional reflectance distribution (BRDF) (*c<sub>diff</sub>*, *F<sub>0</sub>*, *&alpha;*) từ from the metallic-roughness material properties. In addition to the material properties, if a primitive specifies a vertex color using the attribute semantic property `COLOR_0`, then this value acts as an additional linear multiplier to `baseColor`.

`const dielectricSpecular = rgb(0.04, 0.04, 0.04)`
<br>
`const black = rgb(0, 0, 0)`

*c<sub>diff</sub>* = `lerp(baseColor.rgb * (1 - dielectricSpecular.r), black, metallic)`
<br>
*F<sub>0</sub>* = `lerp(dieletricSpecular, baseColor.rgb, metallic)`
<br>
*&alpha;* = `roughness ^ 2`

All implementations should use the same calculations for the BRDF inputs. Implementations of the BRDF itself can vary based on device performance and resource constraints. See [Appendix B](#appendix-b-brdf-implementation) for more details on the BRDF calculations.

### Additional Maps

The material definition also provides for additional maps that can also be used with the metallic-roughness material model as well as other material models which could be provided via glTF extensions.

Materials define the following additional maps:
- **normal** : A tangent space normal map.
- **occlusion** : The occlusion map indicating areas of indirect lighting.
- **emissive** : The emissive map controls the color and intensity of the light being emitted by the material.

The following examples shows a material that is defined using `pbrMetallicRoughness` parameters as well as additional texture maps:

```json
{
    "materials": [
        {
            "name": "Material0",
            "pbrMetallicRoughness": {
                "baseColorFactor": [ 0.5, 0.5, 0.5, 1.0 ],
                "baseColorTexture": {
                    "index": 1,
                    "texCoord": 1
                },
                "metallicFactor": 1,
                "roughnessFactor": 1,
                "metallicRoughnessTexture": {
                    "index": 2,
                    "texCoord": 1
                }
            },
            "normalTexture": {
                "scale": 2,
                "index": 3,
                "texCoord": 1
            },
            "emissiveFactor": [ 0.2, 0.1, 0.0 ]
        }
    ]
}
```

>**Implementation Note:** If an implementation is resource-bound and cannot support all the maps defined it should support these additional maps in the following priority order.  Resource-bound implementations should drop maps from the bottom to the top.
>
>| Map       | Rendering impact when map is not supported |
>|-----------|--------------------------------------------|
>| Normal    | Geometry will appear less detailed than authored. |
>| Occlusion | Model will appear brighter in areas that should be darker. |
>| Emissive  | Model with lights will not be lit. For example, the headlights of a car model will be off instead of on. |

### Alpha Coverage

The `alphaMode` property defines how the alpha value of the main factor and texture should be interpreted. The alpha value is defined in the `baseColor` for metallic-roughness material model. 

`alphaMode` can be one of the following values:
* `OPAQUE` - The rendered output is fully opaque and any alpha value is ignored.
* `MASK` - The rendered output is either fully opaque or fully transparent depending on the alpha value and the specified alpha cutoff value. This mode is used to simulate geometry such as tree leaves or wire fences.
* `BLEND` - The rendered output is combined with the background using the normal painting operation (i.e. the Porter and Duff over operator). This mode is used to simulate geometry such as guaze cloth or animal fur. 

 When `alphaMode` is set to `MASK` the `alphaCutoff` property specifies the cutoff threshold. If the alpha value is greater than or equal to the `alphaCutoff` value then it is rendered as fully opaque, otherwise, it is rendered as fully transparent. `alphaCutoff` value is ignored for other modes.

>**Implementation Note for Real-Time Rasterizers:** Real-time rasterizers typically use depth buffers and mesh sorting to support alpha modes. The following describe the expected behavior for these types of renderers.
>* `OPAQUE` - A depth value is written for every pixel and mesh sorting is not required for correct output.
>* `MASK` - A depth value is not written for a pixel that is discarded after the alpha test. A depth value is written for all other pixels. Mesh sorting is not required for correct output.
>* `BLEND` - Support for this mode varies. There is no perfect and fast solution that works for all cases. Implementations should try to achieve the correct blending output for as many situations as possible. Whether depth value is written or whether to sort is up to the implementation. For example, implementations can discard pixels which have zero or close to zero alpha value to avoid sorting issues.

### Double Sided

The `doubleSided` property specifies whether the material is double sided. When this value is false, back-face culling is enabled. When this value is true, back-face culling is disabled and double sided lighting is enabled. The back-face must have its normals reversed before the lighting equation is evaluated.

### Default Material

The default material, used when a mesh does not specify a material, is defined to be a material with no properties specified. All the default values of [`material`](#reference-material) apply. Note that this material does not emit light and will be black unless some lighting is present in the scene.

### Point and Line Materials

*This section is non-normative.*

This specification does not define size and style of non-triangular primitives (such as POINTS or LINES) at this time, and applications may use various techniques to render these primitives as appropriate. However, the following recommendations are provided for consistency:

* POINTS and LINES should have widths of 1px in viewport space.
* For LINES with `NORMAL` and `TANGENT` properties, render with standard lighting including normal maps.
* For POINTS or LINES with no `TANGENT` property, render with standard lighting but ignore any normal maps on the material.
* For POINTS or LINES with no `NORMAL` property, don't calculate lighting and instead output the `COLOR` value for each pixel drawn.

## Cameras

A camera defines the projection matrix that transforms from view to clip coordinates. The projection can be perspective or orthographic. Cameras are contained in nodes and thus can be transformed. Their world-space transformation matrix is used for calculating view-space transformation. The camera is defined such that the local +X axis is to the right, the lens looks towards the local -Z axis, and the top of the camera is aligned with the local +Y axis. If no transformation is specified, the location of the camera is at the origin.

Cameras are stored in the asset's `cameras` array. Each camera defines a `type` property that designates the type of projection (perspective or orthographic), and either a `perspective` or `orthographic` property that defines the details.

Depending on the presence of `zfar` property, perspective cameras could use finite or infinite projection.

The following example defines two perspective cameras with supplied values for Y field of view, aspect ratio, and clipping information.

```json
{
    "cameras": [
        {
            "name": "Finite perspective camera",
            "type": "perspective",
            "perspective": {
                "aspectRatio": 1.5,
                "yfov": 0.660593,
                "zfar": 100,
                "znear": 0.01
            }      
        },
        {
            "name": "Infinite perspective camera",
            "type": "perspective",
            "perspective": {
                "aspectRatio": 1.5,
                "yfov": 0.660593,
                "znear": 0.01
            }
        }
    ]
}
```

## Specifying Extensions

Thiết kế của glTF cho phép việc mở rộng cấu trúc và thêm tính năng bằng extensions. Bất kỳ đối tượng glTF nào cũng có thể gắn thêm thuộc tính `extensions` để mở rộng. Ví dụ như là có thể thêm tính năng cho scene bằng `scene.extensions`.

Để biết thêm về glTF extensions, hãy xem [thông số của extension](../../extensions/README.md).

# Cấu Trúc File GLB

glTF cung cấp hai cách để vận chuyển dữ liệu, có thể dùng cả hai cùng lúc:

* glTF JSON trỏ tới dữ liệu binary ngoài (geometry, key frames, skins), and images.
* glTF JSON chứa dữ liệu binary mã hoá theo base64, và hình ảnh lưu trong data URI.


Đối với những tài nguyên này, glTF đòi phải một là bắn nhiều request hoặc hi sinh space vì dùng base64. Base64 cần phải xử lý thêm và tăng kích cỡ tài nguyên lên khoảng 33%. Mặc dù có thể dùng file nén để khắc phục, nhưng giải nén và giải mã cũng tốn nhiều thời gian.

Để giải quyết vấn đề này, một cấu trúc container, _Binary glTF_ được ra đời. Trong Binary glTF, một glTF asset (JSON, .bin và hình ảnh) có thể được lưu chung trong một cục binary blob.

Cục binary blob (cỏ thể là một file), có cấu trúc sau:
* 12 byte lưu thông tin về toàn container, gọi là `header`.
* Một hoặc nhiều `chunks` chứa JSON và dữ liệu binary.

`chunk` chửa JSON có thể dùng tài nguyên bên ngoài như bình thường, và cũng có thể dùng tài nguyên chứa trong các binary `chunks` khác.

Ví dụ, một ứng dùng cho phép người dùng chọn texture có thể bỏ tất cả mọi thứ trừ texture image trong Binary glTF. Tài nguyên base64 vẫn dùng được, nhưng sẽ dùng nó là không tối ưu.

### Đuôi File

Đuôi của Binary glTF là `.glb`.

### MIME Type

Dùng `model/gltf-binary`.

## Binary glTF Layout

Binary glTF là little endian. Hình 1 là một ví dụ của một Binary glTF asset.

**Hình 1**: Binary glTF layout.

![](figures/glb2.png)

Những phần sau sẽ miêu tả cấu trúc này chi tiết hơn.

### Header

Cái header 12 byte này chứa 3 thành phần 4 byte:

```
uint32 magic
uint32 version
uint32 length
```

* `magic` có giá trị `0x46546C67`. Dịch theo mã ASCII thì nó là chuỗi  `glTF`, dùng để đánh dấu đây là dữ liệu có dạng Binary glTF.

* `version` là version của Binary glTF container (không phải của glTF JSON). Phiên bản hiện tại của doc này là version 2.

* `length` là tổng kích cỡ của the Binary glTF, cộng hết kích cỡ của Header và tất cả Chunks, tính bằng byte.

> **Implementation Note:** Ứng dụng load GLB nên kiểm tra [thuộc tính asset version](#asset) trong chunk JSON vì version trong chunk Header có thể khác version trong chunk JSON. Version trong chunk Header chỉ là version của cái GLB container.

### Chunks

Mỗi chunk có cấu trúc sau:
```
uint32 chunkLength
uint32 chunkType
ubyte[] chunkData
```

* `chunkLength` là kích cỡ của `chunkData`, theo byte, không tính `chunkLength` và `chunkType`.

* `chunkType` đánh dấu type của chunk. Xem Bảng 1 để biết thêm.

* `chunkData` là nơi chứa dữ liệu của chunk.

Đầu và đuôi của mỗi chunk phải được canh theo những khoảng cách bội số của 4. Xem định nghĩa của chunk để biết pad như thế nào. Thứ tự của chunk phải theo chính xác Bảng 1.

**Table 1**: Chunk types

|  | Chunk Type | ASCII | Miêu Tả | Số Lượng |
|----|------------|-------|-------------------------|-------------|
| 1. | 0x4E4F534A | JSON | Nội dung JSON | 1 |
| 2. | 0x004E4942 | BIN | Binary buffer | 0 or 1 |

Ứng dụng phải lơ chunk có type lạ để cho phép glTF extension dùng type chunk mới đặt say hai chunk JSON với BIN.

#### Structured JSON Content

Chunk này chứa dữ liệu glTF, y như trong một file .gltf bình thường.

> **Implementation Note:** Khi dùng JavaScript, cái API `TextDecoder` có thể được dùng để lấy nội dung glTF từ ArrayBuffer, và sau đó parse nội dung JSON với `JSON.parse` như bình thường. 

Chunk này phải là chunk đầu tiêu trong Binary glTF ngay sau chunk Header. Chunk này cần được đọc trước để ứng dụng biết được cần đọc gì từ những chunk tiếp theo. Như vậy thì chỉ cần đọc những phần tài nguyên cần thiết trong Binary glTF.

Chunk này phải được pad dùng ký tự trắng (`Space == 0x20`) để đúng quy ước.

#### Binary buffer

Chunk này chứa dữ liệu binary như là geometry, animation, key frams, skins và hình ảnh. Đọc thông số của glTF để hiểu cách đọc chunk này trong JSON.

Đây phải là chunk thứ hai trong Binary glTF asset sau chunk Header.

Chunk này phải được pad bằng số 0 (`0x00`) để đúng quy ước.

# Properties Reference

## Objects
* [`accessor`](#reference-accessor)
   * [`sparse`](#reference-sparse)
      * [`indices`](#reference-indices)
      * [`values`](#reference-values)
* [`animation`](#reference-animation)
   * [`animation sampler`](#reference-animation-sampler)
   * [`channel`](#reference-channel)
      * [`target`](#reference-target)
* [`asset`](#reference-asset)
* [`buffer`](#reference-buffer)
* [`bufferView`](#reference-bufferview)
* [`camera`](#reference-camera)
   * [`orthographic`](#reference-orthographic)
   * [`perspective`](#reference-perspective)
* [`extension`](#reference-extension)
* [`extras`](#reference-extras)
* [`glTF`](#reference-gltf) (root object)
* [`image`](#reference-image)
* [`material`](#reference-material)
   * [`normalTextureInfo`](#reference-normaltextureinfo)
   * [`occlusionTextureInfo`](#reference-occlusiontextureinfo)
   * [`pbrMetallicRoughness`](#reference-pbrmetallicroughness)
* [`mesh`](#reference-mesh)
   * [`primitive`](#reference-primitive)
* [`node`](#reference-node)
* [`sampler`](#reference-sampler)
* [`scene`](#reference-scene)
* [`skin`](#reference-skin)
* [`texture`](#reference-texture)
* [`textureInfo`](#reference-textureinfo)


---------------------------------------
<a name="reference-accessor"></a>
### accessor

A typed view into a bufferView.  A bufferView contains raw binary data.  An accessor provides a typed view into a bufferView or a subset of a bufferView similar to how WebGL's `vertexAttribPointer()` defines an attribute in a buffer.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**bufferView**|`integer`|The index of the bufferView.|No|
|**byteOffset**|`integer`|The offset relative to the start of the bufferView in bytes.|No, default: `0`|
|**componentType**|`integer`|The datatype of components in the attribute.| :white_check_mark: Yes|
|**normalized**|`boolean`|Specifies whether integer data values should be normalized.|No, default: `false`|
|**count**|`integer`|The number of attributes referenced by this accessor.| :white_check_mark: Yes|
|**type**|`string`|Specifies if the attribute is a scalar, vector, or matrix.| :white_check_mark: Yes|
|**max**|`number` `[1-16]`|Maximum value of each component in this attribute.|No|
|**min**|`number` `[1-16]`|Minimum value of each component in this attribute.|No|
|**sparse**|`object`|Sparse storage of attributes that deviate from their initialization value.|No|
|**name**|`string`|The user-defined name of this object.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [accessor.schema.json](schema/accessor.schema.json)

#### accessor.bufferView

The index of the bufferView. When not defined, accessor must be initialized with zeros; [`sparse`](#reference-sparse) property or extensions could override zeros with actual values.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### accessor.byteOffset

The offset relative to the start of the bufferView in bytes.  This must be a multiple of the size of the component datatype.

* **Type**: `integer`
* **Required**: No, default: `0`
* **Minimum**: ` >= 0`
* **Related WebGL functions**: `vertexAttribPointer()` offset parameter

#### accessor.componentType :white_check_mark: 

The datatype of components in the attribute.  All valid values correspond to WebGL enums.  The corresponding typed arrays are `Int8Array`, `Uint8Array`, `Int16Array`, `Uint16Array`, `Uint32Array`, and `Float32Array`, respectively.  5125 (UNSIGNED_INT) is only allowed when the accessor contains indices, i.e., the accessor is only referenced by `primitive.indices`.

* **Type**: `integer`
* **Required**: Yes
* **Allowed values**:
   * `5120` BYTE
   * `5121` UNSIGNED_BYTE
   * `5122` SHORT
   * `5123` UNSIGNED_SHORT
   * `5125` UNSIGNED_INT
   * `5126` FLOAT
* **Related WebGL functions**: `vertexAttribPointer()` type parameter

#### accessor.normalized

Specifies whether integer data values should be normalized (`true`) to [0, 1] (for unsigned types) or [-1, 1] (for signed types), or converted directly (`false`) when they are accessed. This property is defined only for accessors that contain vertex attributes or animation output data.

* **Type**: `boolean`
* **Required**: No, default: `false`
* **Related WebGL functions**: `vertexAttribPointer()` normalized parameter

#### accessor.count :white_check_mark: 

The number of attributes referenced by this accessor, not to be confused with the number of bytes or number of components.

* **Type**: `integer`
* **Required**: Yes
* **Minimum**: ` >= 1`

#### accessor.type :white_check_mark: 

Specifies if the attribute is a scalar, vector, or matrix.

* **Type**: `string`
* **Required**: Yes
* **Allowed values**:
   * `"SCALAR"`
   * `"VEC2"`
   * `"VEC3"`
   * `"VEC4"`
   * `"MAT2"`
   * `"MAT3"`
   * `"MAT4"`

#### accessor.max

Maximum value of each component in this attribute.  Array elements must be treated as having the same data type as accessor's `componentType`. Both min and max arrays have the same length.  The length is determined by the value of the type property; it can be 1, 2, 3, 4, 9, or 16.

`normalized` property has no effect on array values: they always correspond to the actual values stored in the buffer. When accessor is sparse, this property must contain max values of accessor data with sparse substitution applied.

* **Type**: `number` `[1-16]`
* **Required**: No

#### accessor.min

Minimum value of each component in this attribute.  Array elements must be treated as having the same data type as accessor's `componentType`. Both min and max arrays have the same length.  The length is determined by the value of the type property; it can be 1, 2, 3, 4, 9, or 16.

`normalized` property has no effect on array values: they always correspond to the actual values stored in the buffer. When accessor is sparse, this property must contain min values of accessor data with sparse substitution applied.

* **Type**: `number` `[1-16]`
* **Required**: No

#### accessor.sparse

Sparse storage of attributes that deviate from their initialization value.

* **Type**: `object`
* **Required**: No

#### accessor.name

The user-defined name of this object.  This is not necessarily unique, e.g., an accessor and a buffer could have the same name, or two accessors could even have the same name.

* **Type**: `string`
* **Required**: No

#### accessor.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### accessor.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-animation"></a>
### animation

A keyframe animation.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**channels**|channel `[1-*]`|An array of channels, each of which targets an animation's sampler at a node's property. Different channels of the same animation can't have equal targets.| :white_check_mark: Yes|
|**samplers**|animation sampler `[1-*]`|An array of samplers that combines input and output accessors with an interpolation algorithm to define a keyframe graph (but not its target).| :white_check_mark: Yes|
|**name**|`string`|The user-defined name of this object.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [animation.schema.json](schema/animation.schema.json)

#### animation.channels :white_check_mark: 

An array of channels, each of which targets an animation's sampler at a node's property. Different channels of the same animation can't have equal targets.

* **Type**: channel `[1-*]`
* **Required**: Yes

#### animation.samplers :white_check_mark: 

An array of samplers that combines input and output accessors with an interpolation algorithm to define a keyframe graph (but not its target).

* **Type**: animation sampler `[1-*]`
* **Required**: Yes

#### animation.name

The user-defined name of this object.  This is not necessarily unique, e.g., an accessor and a buffer could have the same name, or two accessors could even have the same name.

* **Type**: `string`
* **Required**: No

#### animation.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### animation.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-animation-sampler"></a>
### animation sampler

Combines input and output accessors with an interpolation algorithm to define a keyframe graph (but not its target).

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**input**|`integer`|The index of an accessor containing keyframe input values, e.g., time.| :white_check_mark: Yes|
|**interpolation**|`string`|Interpolation algorithm.|No, default: `"LINEAR"`|
|**output**|`integer`|The index of an accessor, containing keyframe output values.| :white_check_mark: Yes|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [animation.sampler.schema.json](schema/animation.sampler.schema.json)

#### animation sampler.input :white_check_mark: 

The index of an accessor containing keyframe input values, e.g., time. That accessor must have componentType `FLOAT`. The values represent time in seconds with `time[0] >= 0.0`, and strictly increasing values, i.e., `time[n + 1] > time[n]`.

* **Type**: `integer`
* **Required**: Yes
* **Minimum**: ` >= 0`

#### animation sampler.interpolation

Interpolation algorithm.

* **Type**: `string`
* **Required**: No, default: `"LINEAR"`
* **Allowed values**:
   * `"LINEAR"` The animated values are linearly interpolated between keyframes. When targeting a rotation, spherical linear interpolation (slerp) should be used to interpolate quaternions. The number output of elements must equal the number of input elements.
   * `"STEP"` The animated values remain constant to the output of the first keyframe, until the next keyframe. The number of output elements must equal the number of input elements.
   * `"CUBICSPLINE"` The animation's interpolation is computed using a cubic spline with specified tangents. The number of output elements must equal three times the number of input elements. For each input element, the output stores three elements, an in-tangent, a spline vertex, and an out-tangent. There must be at least two keyframes when using this interpolation.

#### animation sampler.output :white_check_mark: 

The index of an accessor containing keyframe output values. When targeting TRS target, the `accessor.componentType` of the output values must be `FLOAT`. When targeting morph weights, the `accessor.componentType` of the output values must be `FLOAT` or normalized integer where each output element stores values with a count equal to the number of morph targets.

* **Type**: `integer`
* **Required**: Yes
* **Minimum**: ` >= 0`

#### animation sampler.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### animation sampler.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-asset"></a>
### asset

Metadata about the glTF asset.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**copyright**|`string`|A copyright message suitable for display to credit the content creator.|No|
|**generator**|`string`|Tool that generated this glTF model.  Useful for debugging.|No|
|**version**|`string`|The glTF version that this asset targets.| :white_check_mark: Yes|
|**minVersion**|`string`|The minimum glTF version that this asset targets.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [asset.schema.json](schema/asset.schema.json)

#### asset.copyright

A copyright message suitable for display to credit the content creator.

* **Type**: `string`
* **Required**: No

#### asset.generator

Tool that generated this glTF model.  Useful for debugging.

* **Type**: `string`
* **Required**: No

#### asset.version :white_check_mark: 

The glTF version that this asset targets.

* **Type**: `string`
* **Required**: Yes

#### asset.minVersion

The minimum glTF version that this asset targets.

* **Type**: `string`
* **Required**: No

#### asset.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### asset.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-buffer"></a>
### buffer

A buffer points to binary geometry, animation, or skins.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**uri**|`string`|The uri of the buffer.|No|
|**byteLength**|`integer`|The length of the buffer in bytes.| :white_check_mark: Yes|
|**name**|`string`|The user-defined name of this object.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [buffer.schema.json](schema/buffer.schema.json)

#### buffer.uri

The uri of the buffer.  Relative paths are relative to the .gltf file.  Instead of referencing an external file, the uri can also be a data-uri.

* **Type**: `string`
* **Required**: No
* **Format**: uriref

#### buffer.byteLength :white_check_mark: 

The length of the buffer in bytes.

* **Type**: `integer`
* **Required**: Yes
* **Minimum**: ` >= 1`

#### buffer.name

The user-defined name of this object.  This is not necessarily unique, e.g., an accessor and a buffer could have the same name, or two accessors could even have the same name.

* **Type**: `string`
* **Required**: No

#### buffer.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### buffer.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-bufferview"></a>
### bufferView

A view into a buffer generally representing a subset of the buffer.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**buffer**|`integer`|The index of the buffer.| :white_check_mark: Yes|
|**byteOffset**|`integer`|The offset into the buffer in bytes.|No, default: `0`|
|**byteLength**|`integer`|The length of the bufferView in bytes.| :white_check_mark: Yes|
|**byteStride**|`integer`|The stride, in bytes.|No|
|**target**|`integer`|The target that the GPU buffer should be bound to.|No|
|**name**|`string`|The user-defined name of this object.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [bufferView.schema.json](schema/bufferView.schema.json)

#### bufferView.buffer :white_check_mark: 

The index of the buffer.

* **Type**: `integer`
* **Required**: Yes
* **Minimum**: ` >= 0`

#### bufferView.byteOffset

The offset into the buffer in bytes.

* **Type**: `integer`
* **Required**: No, default: `0`
* **Minimum**: ` >= 0`

#### bufferView.byteLength :white_check_mark: 

The length of the bufferView in bytes.

* **Type**: `integer`
* **Required**: Yes
* **Minimum**: ` >= 1`

#### bufferView.byteStride

The stride, in bytes, between vertex attributes.  When this is not defined, data is tightly packed. When two or more accessors use the same bufferView, this field must be defined.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 4`
* **Maximum**: ` <= 252`
* **Related WebGL functions**: `vertexAttribPointer()` stride parameter

#### bufferView.target

The target that the GPU buffer should be bound to.

* **Type**: `integer`
* **Required**: No
* **Allowed values**:
   * `34962` ARRAY_BUFFER
   * `34963` ELEMENT_ARRAY_BUFFER
* **Related WebGL functions**: `bindBuffer()`

#### bufferView.name

The user-defined name of this object.  This is not necessarily unique, e.g., an accessor and a buffer could have the same name, or two accessors could even have the same name.

* **Type**: `string`
* **Required**: No

#### bufferView.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### bufferView.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-camera"></a>
### camera

A camera's projection.  A node can reference a camera to apply a transform to place the camera in the scene.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**orthographic**|`object`|An orthographic camera containing properties to create an orthographic projection matrix.|No|
|**perspective**|`object`|A perspective camera containing properties to create a perspective projection matrix.|No|
|**type**|`string`|Specifies if the camera uses a perspective or orthographic projection.| :white_check_mark: Yes|
|**name**|`string`|The user-defined name of this object.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [camera.schema.json](schema/camera.schema.json)

#### camera.orthographic

An orthographic camera containing properties to create an orthographic projection matrix.

* **Type**: `object`
* **Required**: No

#### camera.perspective

A perspective camera containing properties to create a perspective projection matrix.

* **Type**: `object`
* **Required**: No

#### camera.type :white_check_mark: 

Specifies if the camera uses a perspective or orthographic projection.  Based on this, either the camera's [`perspective`](#reference-perspective) or [`orthographic`](#reference-orthographic) property will be defined.

* **Type**: `string`
* **Required**: Yes
* **Allowed values**:
   * `"perspective"`
   * `"orthographic"`

#### camera.name

The user-defined name of this object.  This is not necessarily unique, e.g., an accessor and a buffer could have the same name, or two accessors could even have the same name.

* **Type**: `string`
* **Required**: No

#### camera.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### camera.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-channel"></a>
### channel

Targets an animation's sampler at a node's property.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**sampler**|`integer`|The index of a sampler in this animation used to compute the value for the target.| :white_check_mark: Yes|
|**target**|`object`|The index of the node and TRS property to target.| :white_check_mark: Yes|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [animation.channel.schema.json](schema/animation.channel.schema.json)

#### channel.sampler :white_check_mark: 

The index of a sampler in this animation used to compute the value for the target, e.g., a node's translation, rotation, or scale (TRS).

* **Type**: `integer`
* **Required**: Yes
* **Minimum**: ` >= 0`

#### channel.target :white_check_mark: 

The index of the node and TRS property to target.

* **Type**: `object`
* **Required**: Yes

#### channel.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### channel.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-extension"></a>
### extension

Dictionary object with extension-specific objects.

Additional properties are allowed.

* **JSON schema**: [extension.schema.json](schema/extension.schema.json)




---------------------------------------
<a name="reference-extras"></a>
### extras

Application-specific data.



---------------------------------------
<a name="reference-gltf"></a>
### glTF

The root object for a glTF asset.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**extensionsUsed**|`string` `[1-*]`|Names of glTF extensions used somewhere in this asset.|No|
|**extensionsRequired**|`string` `[1-*]`|Names of glTF extensions required to properly load this asset.|No|
|**accessors**|accessor `[1-*]`|An array of accessors.|No|
|**animations**|animation `[1-*]`|An array of keyframe animations.|No|
|**asset**|`object`|Metadata about the glTF asset.|Yes|
|**buffers**|buffer `[1-*]`|An array of buffers.|No|
|**bufferViews**|bufferView `[1-*]`|An array of bufferViews.|No|
|**cameras**|camera `[1-*]`|An array of cameras.|No|
|**images**|image `[1-*]`|An array of images.|No|
|**materials**|material `[1-*]`|An array of materials.|No|
|**meshes**|mesh `[1-*]`|An array of meshes.|No|
|**nodes**|node `[1-*]`|An array of nodes.|No|
|**samplers**|sampler `[1-*]`|An array of samplers.|No|
|**scene**|`integer`|The index of the default scene.|No|
|**scenes**|scene `[1-*]`|An array of scenes.|No|
|**skins**|skin `[1-*]`|An array of skins.|No|
|**textures**|texture `[1-*]`|An array of textures.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [glTF.schema.json](schema/glTF.schema.json)

#### glTF.extensionsUsed

Names of glTF extensions used somewhere in this asset.

* **Type**: `string` `[1-*]`
   * Each element in the array must be unique.
* **Required**: No

#### glTF.extensionsRequired

Names of glTF extensions required to properly load this asset.

* **Type**: `string` `[1-*]`
   * Each element in the array must be unique.
* **Required**: No

#### glTF.accessors

An array of accessors.  An accessor is a typed view into a bufferView.

* **Type**: accessor `[1-*]`
* **Required**: No

#### glTF.animations

An array of keyframe animations.

* **Type**: animation `[1-*]`
* **Required**: No

#### glTF.asset :white_check_mark: 

Metadata about the glTF asset.

* **Type**: `object`
* **Required**: Yes

#### glTF.buffers

An array of buffers.  A buffer points to binary geometry, animation, or skins.

* **Type**: buffer `[1-*]`
* **Required**: No

#### glTF.bufferViews

An array of bufferViews.  A bufferView is a view into a buffer generally representing a subset of the buffer.

* **Type**: bufferView `[1-*]`
* **Required**: No

#### glTF.cameras

An array of cameras.  A camera defines a projection matrix.

* **Type**: camera `[1-*]`
* **Required**: No

#### glTF.images

An array of images.  An image defines data used to create a texture.

* **Type**: image `[1-*]`
* **Required**: No

#### glTF.materials

An array of materials.  A material defines the appearance of a primitive.

* **Type**: material `[1-*]`
* **Required**: No

#### glTF.meshes

An array of meshes.  A mesh is a set of primitives to be rendered.

* **Type**: mesh `[1-*]`
* **Required**: No

#### glTF.nodes

An array of nodes.

* **Type**: node `[1-*]`
* **Required**: No

#### glTF.samplers

An array of samplers.  A sampler contains properties for texture filtering and wrapping modes.

* **Type**: sampler `[1-*]`
* **Required**: No

#### glTF.scene

The index of the default scene.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### glTF.scenes

An array of scenes.

* **Type**: scene `[1-*]`
* **Required**: No

#### glTF.skins

An array of skins.  A skin is defined by joints and matrices.

* **Type**: skin `[1-*]`
* **Required**: No

#### glTF.textures

An array of textures.

* **Type**: texture `[1-*]`
* **Required**: No

#### glTF.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### glTF.extras

Application-specific data.

* **Type**: `any`
* **Required**: No






---------------------------------------
<a name="reference-image"></a>
### image

Image data used to create a texture. Image can be referenced by URI or [`bufferView`](#reference-bufferview) index. `mimeType` is required in the latter case.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**uri**|`string`|The uri of the image.|No|
|**mimeType**|`string`|The image's MIME type.|No|
|**bufferView**|`integer`|The index of the bufferView that contains the image. Use this instead of the image's uri property.|No|
|**name**|`string`|The user-defined name of this object.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [image.schema.json](schema/image.schema.json)

#### image.uri

The uri of the image.  Relative paths are relative to the .gltf file.  Instead of referencing an external file, the uri can also be a data-uri.  The image format must be jpg or png.

* **Type**: `string`
* **Required**: No
* **Format**: uriref

#### image.mimeType

The image's MIME type.

* **Type**: `string`
* **Required**: No
* **Allowed values**:
   * `"image/jpeg"`
   * `"image/png"`

#### image.bufferView

The index of the bufferView that contains the image. Use this instead of the image's uri property.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### image.name

The user-defined name of this object.  This is not necessarily unique, e.g., an accessor and a buffer could have the same name, or two accessors could even have the same name.

* **Type**: `string`
* **Required**: No

#### image.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### image.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-indices"></a>
### indices

Indices of those attributes that deviate from their initialization value.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**bufferView**|`integer`|The index of the bufferView with sparse indices. Referenced bufferView can't have ARRAY_BUFFER or ELEMENT_ARRAY_BUFFER target.| :white_check_mark: Yes|
|**byteOffset**|`integer`|The offset relative to the start of the bufferView in bytes. Must be aligned.|No, default: `0`|
|**componentType**|`integer`|The indices data type.| :white_check_mark: Yes|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [accessor.sparse.indices.schema.json](schema/accessor.sparse.indices.schema.json)

#### indices.bufferView :white_check_mark: 

The index of the bufferView with sparse indices. Referenced bufferView can't have ARRAY_BUFFER or ELEMENT_ARRAY_BUFFER target.

* **Type**: `integer`
* **Required**: Yes
* **Minimum**: ` >= 0`

#### indices.byteOffset

The offset relative to the start of the bufferView in bytes. Must be aligned.

* **Type**: `integer`
* **Required**: No, default: `0`
* **Minimum**: ` >= 0`

#### indices.componentType :white_check_mark: 

The indices data type.  Valid values correspond to WebGL enums: `5121` (UNSIGNED_BYTE), `5123` (UNSIGNED_SHORT), `5125` (UNSIGNED_INT).

* **Type**: `integer`
* **Required**: Yes
* **Allowed values**:
   * `5121` UNSIGNED_BYTE
   * `5123` UNSIGNED_SHORT
   * `5125` UNSIGNED_INT

#### indices.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### indices.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-material"></a>
### material

The material appearance of a primitive.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**name**|`string`|The user-defined name of this object.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|
|**pbrMetallicRoughness**|`object`|A set of parameter values that are used to define the metallic-roughness material model from Physically-Based Rendering (PBR) methodology. When not specified, all the default values of [`pbrMetallicRoughness`](#reference-pbrmetallicroughness) apply.|No|
|**normalTexture**|`object`|The normal map texture.|No|
|**occlusionTexture**|`object`|The occlusion map texture.|No|
|**emissiveTexture**|`object`|The emissive map texture.|No|
|**emissiveFactor**|`number` `[3]`|The emissive color of the material.|No, default: `[0,0,0]`|
|**alphaMode**|`string`|The alpha rendering mode of the material.|No, default: `"OPAQUE"`|
|**alphaCutoff**|`number`|The alpha cutoff value of the material.|No, default: `0.5`|
|**doubleSided**|`boolean`|Specifies whether the material is double sided.|No, default: `false`|

Additional properties are allowed.

* **JSON schema**: [material.schema.json](schema/material.schema.json)

#### material.name

The user-defined name of this object.  This is not necessarily unique, e.g., an accessor and a buffer could have the same name, or two accessors could even have the same name.

* **Type**: `string`
* **Required**: No

#### material.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### material.extras

Application-specific data.

* **Type**: `any`
* **Required**: No

#### material.pbrMetallicRoughness

A set of parameter values that are used to define the metallic-roughness material model from Physically-Based Rendering (PBR) methodology. When not specified, all the default values of [`pbrMetallicRoughness`](#reference-pbrmetallicroughness) apply.

* **Type**: `object`
* **Required**: No

#### material.normalTexture

A tangent space normal map. The texture contains RGB components in linear space. Each texel represents the XYZ components of a normal vector in tangent space. Red [0 to 255] maps to X [-1 to 1]. Green [0 to 255] maps to Y [-1 to 1]. Blue [128 to 255] maps to Z [1/255 to 1]. The normal vectors use OpenGL conventions where +X is right and +Y is up. +Z points toward the viewer. In GLSL, this vector would be unpacked like so: `vec3 normalVector = tex2D(normalMap, texCoord) * 2 - 1`. Client implementations should normalize the normal vectors before using them in lighting equations.

* **Type**: `object`
* **Required**: No

#### material.occlusionTexture

The occlusion map texture. The occlusion values are sampled from the R channel. Higher values indicate areas that should receive full indirect lighting and lower values indicate no indirect lighting. These values are linear. If other channels are present (GBA), they are ignored for occlusion calculations.

* **Type**: `object`
* **Required**: No

#### material.emissiveTexture

The emissive map controls the color and intensity of the light being emitted by the material. This texture contains RGB components in sRGB color space. If a fourth component (A) is present, it is ignored.

* **Type**: `object`
* **Required**: No

#### material.emissiveFactor

The RGB components of the emissive color of the material. These values are linear. If an emissiveTexture is specified, this value is multiplied with the texel values.

* **Type**: `number` `[3]`
   * Each element in the array must be greater than or equal to `0` and less than or equal to `1`.
* **Required**: No, default: `[0,0,0]`

#### material.alphaMode

The material's alpha rendering mode enumeration specifying the interpretation of the alpha value of the main factor and texture.

* **Type**: `string`
* **Required**: No, default: `"OPAQUE"`
* **Allowed values**:
   * `"OPAQUE"` The alpha value is ignored and the rendered output is fully opaque.
   * `"MASK"` The rendered output is either fully opaque or fully transparent depending on the alpha value and the specified alpha cutoff value.
   * `"BLEND"` The alpha value is used to composite the source and destination areas. The rendered output is combined with the background using the normal painting operation (i.e. the Porter and Duff over operator).

#### material.alphaCutoff

Specifies the cutoff threshold when in `MASK` mode. If the alpha value is greater than or equal to this value then it is rendered as fully opaque, otherwise, it is rendered as fully transparent. A value greater than 1.0 will render the entire material as fully transparent. This value is ignored for other modes.

* **Type**: `number`
* **Required**: No, default: `0.5`
* **Minimum**: ` >= 0`

#### material.doubleSided

Specifies whether the material is double sided. When this value is false, back-face culling is enabled. When this value is true, back-face culling is disabled and double sided lighting is enabled. The back-face must have its normals reversed before the lighting equation is evaluated.

* **Type**: `boolean`
* **Required**: No, default: `false`




---------------------------------------
<a name="reference-mesh"></a>
### mesh

A set of primitives to be rendered.  A node can contain one mesh.  A node's transform places the mesh in the scene.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**primitives**|primitive `[1-*]`|An array of primitives, each defining geometry to be rendered with a material.| :white_check_mark: Yes|
|**weights**|`number` `[1-*]`|Array of weights to be applied to the Morph Targets.|No|
|**name**|`string`|The user-defined name of this object.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [mesh.schema.json](schema/mesh.schema.json)

#### mesh.primitives :white_check_mark: 

An array of primitives, each defining geometry to be rendered with a material.

* **Type**: primitive `[1-*]`
* **Required**: Yes

#### mesh.weights

Array of weights to be applied to the Morph Targets.

* **Type**: `number` `[1-*]`
* **Required**: No

#### mesh.name

The user-defined name of this object.  This is not necessarily unique, e.g., an accessor and a buffer could have the same name, or two accessors could even have the same name.

* **Type**: `string`
* **Required**: No

#### mesh.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### mesh.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-node"></a>
### node

A node in the node hierarchy.  When the node contains [`skin`](#reference-skin), all `mesh.primitives` must contain `JOINTS_0` and `WEIGHTS_0` attributes.  A node can have either a `matrix` or any combination of `translation`/`rotation`/`scale` (TRS) properties. TRS properties are converted to matrices and postmultiplied in the `T * R * S` order to compose the transformation matrix; first the scale is applied to the vertices, then the rotation, and then the translation. If none are provided, the transform is the identity. When a node is targeted for animation (referenced by an animation.channel.target), only TRS properties may be present; `matrix` will not be present.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**camera**|`integer`|The index of the camera referenced by this node.|No|
|**children**|`integer` `[1-*]`|The indices of this node's children.|No|
|**skin**|`integer`|The index of the skin referenced by this node.|No|
|**matrix**|`number` `[16]`|A floating-point 4x4 transformation matrix stored in column-major order.|No, default: `[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]`|
|**mesh**|`integer`|The index of the mesh in this node.|No|
|**rotation**|`number` `[4]`|The node's unit quaternion rotation in the order (x, y, z, w), where w is the scalar.|No, default: `[0,0,0,1]`|
|**scale**|`number` `[3]`|The node's non-uniform scale, given as the scaling factors along the x, y, and z axes.|No, default: `[1,1,1]`|
|**translation**|`number` `[3]`|The node's translation along the x, y, and z axes.|No, default: `[0,0,0]`|
|**weights**|`number` `[1-*]`|The weights of the instantiated Morph Target. Number of elements must match number of Morph Targets of used mesh.|No|
|**name**|`string`|The user-defined name of this object.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [node.schema.json](schema/node.schema.json)

#### node.camera

The index of the camera referenced by this node.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### node.children

The indices of this node's children.

* **Type**: `integer` `[1-*]`
   * Each element in the array must be unique.
   * Each element in the array must be greater than or equal to `0`.
* **Required**: No

#### node.skin

The index of the skin referenced by this node.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### node.matrix

A floating-point 4x4 transformation matrix stored in column-major order.

* **Type**: `number` `[16]`
* **Required**: No, default: `[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]`
* **Related WebGL functions**: `uniformMatrix4fv()` with the transpose parameter equal to false

#### node.mesh

The index of the mesh in this node.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### node.rotation

The node's unit quaternion rotation in the order (x, y, z, w), where w is the scalar.

* **Type**: `number` `[4]`
   * Each element in the array must be greater than or equal to `-1` and less than or equal to `1`.
* **Required**: No, default: `[0,0,0,1]`

#### node.scale

The node's non-uniform scale, given as the scaling factors along the x, y, and z axes.

* **Type**: `number` `[3]`
* **Required**: No, default: `[1,1,1]`

#### node.translation

The node's translation along the x, y, and z axes.

* **Type**: `number` `[3]`
* **Required**: No, default: `[0,0,0]`

#### node.weights

The weights of the instantiated Morph Target. Number of elements must match number of Morph Targets of used mesh.

* **Type**: `number` `[1-*]`
* **Required**: No

#### node.name

The user-defined name of this object.  This is not necessarily unique, e.g., an accessor and a buffer could have the same name, or two accessors could even have the same name.

* **Type**: `string`
* **Required**: No

#### node.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### node.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-normaltextureinfo"></a>
### normalTextureInfo

Reference to a texture.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**index**|`integer`|The index of the texture.| :white_check_mark: Yes|
|**texCoord**|`integer`|The set index of texture's TEXCOORD attribute used for texture coordinate mapping.|No, default: `0`|
|**scale**|`number`|The scalar multiplier applied to each normal vector of the normal texture.|No, default: `1`|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [material.normalTextureInfo.schema.json](schema/material.normalTextureInfo.schema.json)

#### normalTextureInfo.index :white_check_mark: 

The index of the texture.

* **Type**: `integer`
* **Required**: Yes
* **Minimum**: ` >= 0`

#### normalTextureInfo.texCoord

This integer value is used to construct a string in the format TEXCOORD_<set index> which is a reference to a key in mesh.primitives.attributes (e.g. A value of 0 corresponds to TEXCOORD_0).

* **Type**: `integer`
* **Required**: No, default: `0`
* **Minimum**: ` >= 0`

#### normalTextureInfo.scale

The scalar multiplier applied to each normal vector of the texture. This value scales the normal vector using the formula: `scaledNormal =  normalize((normalize(<sampled normal texture value>) * 2.0 - 1.0) * vec3(<normal scale>, <normal scale>, 1.0))`. This value is ignored if normalTexture is not specified. This value is linear.

* **Type**: `number`
* **Required**: No, default: `1`

#### normalTextureInfo.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### normalTextureInfo.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-occlusiontextureinfo"></a>
### occlusionTextureInfo

Reference to a texture.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**index**|`integer`|The index of the texture.| :white_check_mark: Yes|
|**texCoord**|`integer`|The set index of texture's TEXCOORD attribute used for texture coordinate mapping.|No, default: `0`|
|**strength**|`number`|A scalar multiplier controlling the amount of occlusion applied.|No, default: `1`|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [material.occlusionTextureInfo.schema.json](schema/material.occlusionTextureInfo.schema.json)

#### occlusionTextureInfo.index :white_check_mark: 

The index of the texture.

* **Type**: `integer`
* **Required**: Yes
* **Minimum**: ` >= 0`

#### occlusionTextureInfo.texCoord

This integer value is used to construct a string in the format TEXCOORD_<set index> which is a reference to a key in mesh.primitives.attributes (e.g. A value of 0 corresponds to TEXCOORD_0).

* **Type**: `integer`
* **Required**: No, default: `0`
* **Minimum**: ` >= 0`

#### occlusionTextureInfo.strength

A scalar multiplier controlling the amount of occlusion applied. A value of 0.0 means no occlusion. A value of 1.0 means full occlusion. This value affects the resulting color using the formula: `occludedColor = lerp(color, color * <sampled occlusion texture value>, <occlusion strength>)`. This value is ignored if the corresponding texture is not specified. This value is linear.

* **Type**: `number`
* **Required**: No, default: `1`
* **Minimum**: ` >= 0`
* **Maximum**: ` <= 1`

#### occlusionTextureInfo.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### occlusionTextureInfo.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-orthographic"></a>
### orthographic

An orthographic camera containing properties to create an orthographic projection matrix.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**xmag**|`number`|The floating-point horizontal magnification of the view.| :white_check_mark: Yes|
|**ymag**|`number`|The floating-point vertical magnification of the view.| :white_check_mark: Yes|
|**zfar**|`number`|The floating-point distance to the far clipping plane. `zfar` must be greater than `znear`.| :white_check_mark: Yes|
|**znear**|`number`|The floating-point distance to the near clipping plane.| :white_check_mark: Yes|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [camera.orthographic.schema.json](schema/camera.orthographic.schema.json)

#### orthographic.xmag :white_check_mark: 

The floating-point horizontal magnification of the view.

* **Type**: `number`
* **Required**: Yes

#### orthographic.ymag :white_check_mark: 

The floating-point vertical magnification of the view.

* **Type**: `number`
* **Required**: Yes

#### orthographic.zfar :white_check_mark: 

The floating-point distance to the far clipping plane. `zfar` must be greater than `znear`.

* **Type**: `number`
* **Required**: Yes
* **Minimum**: ` > 0`

#### orthographic.znear :white_check_mark: 

The floating-point distance to the near clipping plane.

* **Type**: `number`
* **Required**: Yes
* **Minimum**: ` >= 0`

#### orthographic.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### orthographic.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-pbrmetallicroughness"></a>
### pbrMetallicRoughness

A set of parameter values that are used to define the metallic-roughness material model from Physically-Based Rendering (PBR) methodology.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**baseColorFactor**|`number` `[4]`|The material's base color factor.|No, default: `[1,1,1,1]`|
|**baseColorTexture**|`object`|The base color texture.|No|
|**metallicFactor**|`number`|The metalness of the material.|No, default: `1`|
|**roughnessFactor**|`number`|The roughness of the material.|No, default: `1`|
|**metallicRoughnessTexture**|`object`|The metallic-roughness texture.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [material.pbrMetallicRoughness.schema.json](schema/material.pbrMetallicRoughness.schema.json)

#### pbrMetallicRoughness.baseColorFactor

The RGBA components of the base color of the material. The fourth component (A) is the alpha coverage of the material. The `alphaMode` property specifies how alpha is interpreted. These values are linear. If a baseColorTexture is specified, this value is multiplied with the texel values.

* **Type**: `number` `[4]`
   * Each element in the array must be greater than or equal to `0` and less than or equal to `1`.
* **Required**: No, default: `[1,1,1,1]`

#### pbrMetallicRoughness.baseColorTexture

The base color texture. This texture contains RGB(A) components in sRGB color space. The first three components (RGB) specify the base color of the material. If the fourth component (A) is present, it represents the alpha coverage of the material. Otherwise, an alpha of 1.0 is assumed. The `alphaMode` property specifies how alpha is interpreted. The stored texels must not be premultiplied.

* **Type**: `object`
* **Required**: No

#### pbrMetallicRoughness.metallicFactor

The metalness of the material. A value of 1.0 means the material is a metal. A value of 0.0 means the material is a dielectric. Values in between are for blending between metals and dielectrics such as dirty metallic surfaces. This value is linear. If a metallicRoughnessTexture is specified, this value is multiplied with the metallic texel values.

* **Type**: `number`
* **Required**: No, default: `1`
* **Minimum**: ` >= 0`
* **Maximum**: ` <= 1`

#### pbrMetallicRoughness.roughnessFactor

The roughness of the material. A value of 1.0 means the material is completely rough. A value of 0.0 means the material is completely smooth. This value is linear. If a metallicRoughnessTexture is specified, this value is multiplied with the roughness texel values.

* **Type**: `number`
* **Required**: No, default: `1`
* **Minimum**: ` >= 0`
* **Maximum**: ` <= 1`

#### pbrMetallicRoughness.metallicRoughnessTexture

The metallic-roughness texture. The metalness values are sampled from the B channel. The roughness values are sampled from the G channel. These values are linear. If other channels are present (R or A), they are ignored for metallic-roughness calculations.

* **Type**: `object`
* **Required**: No

#### pbrMetallicRoughness.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### pbrMetallicRoughness.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-perspective"></a>
### perspective

A perspective camera containing properties to create a perspective projection matrix.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**aspectRatio**|`number`|The floating-point aspect ratio of the field of view.|No|
|**yfov**|`number`|The floating-point vertical field of view in radians.| :white_check_mark: Yes|
|**zfar**|`number`|The floating-point distance to the far clipping plane.|No|
|**znear**|`number`|The floating-point distance to the near clipping plane.| :white_check_mark: Yes|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [camera.perspective.schema.json](schema/camera.perspective.schema.json)

#### perspective.aspectRatio

The floating-point aspect ratio of the field of view. When this is undefined, the aspect ratio of the canvas is used.

* **Type**: `number`
* **Required**: No
* **Minimum**: ` > 0`

#### perspective.yfov :white_check_mark: 

The floating-point vertical field of view in radians.

* **Type**: `number`
* **Required**: Yes
* **Minimum**: ` > 0`

#### perspective.zfar

The floating-point distance to the far clipping plane. When defined, `zfar` must be greater than `znear`. If `zfar` is undefined, runtime must use infinite projection matrix.

* **Type**: `number`
* **Required**: No
* **Minimum**: ` > 0`

#### perspective.znear :white_check_mark: 

The floating-point distance to the near clipping plane.

* **Type**: `number`
* **Required**: Yes
* **Minimum**: ` > 0`

#### perspective.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### perspective.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-primitive"></a>
### primitive

Geometry to be rendered with the given material.

**Related WebGL functions**: `drawElements()` and `drawArrays()`

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**attributes**|`object`|A dictionary object, where each key corresponds to mesh attribute semantic and each value is the index of the accessor containing attribute's data.| :white_check_mark: Yes|
|**indices**|`integer`|The index of the accessor that contains the indices.|No|
|**material**|`integer`|The index of the material to apply to this primitive when rendering.|No|
|**mode**|`integer`|The type of primitives to render.|No, default: `4`|
|**targets**|`object` `[1-*]`|An array of Morph Targets, each  Morph Target is a dictionary mapping attributes (only `POSITION`, `NORMAL`, and `TANGENT` supported) to their deviations in the Morph Target.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [mesh.primitive.schema.json](schema/mesh.primitive.schema.json)

#### primitive.attributes :white_check_mark: 

A dictionary object, where each key corresponds to mesh attribute semantic and each value is the index of the accessor containing attribute's data.

* **Type**: `object`
* **Required**: Yes
* **Type of each property**: `integer`

#### primitive.indices

The index of the accessor that contains mesh indices.  When this is not defined, the primitives should be rendered without indices using `drawArrays()`.  When defined, the accessor must contain indices: the [`bufferView`](#reference-bufferview) referenced by the accessor should have a [`target`](#reference-target) equal to 34963 (ELEMENT_ARRAY_BUFFER); `componentType` must be 5121 (UNSIGNED_BYTE), 5123 (UNSIGNED_SHORT) or 5125 (UNSIGNED_INT), the latter may require enabling additional hardware support; `type` must be `"SCALAR"`. For triangle primitives, the front face has a counter-clockwise (CCW) winding order.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### primitive.material

The index of the material to apply to this primitive when rendering.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### primitive.mode

The type of primitives to render. All valid values correspond to WebGL enums.

* **Type**: `integer`
* **Required**: No, default: `4`
* **Allowed values**:
   * `0` POINTS
   * `1` LINES
   * `2` LINE_LOOP
   * `3` LINE_STRIP
   * `4` TRIANGLES
   * `5` TRIANGLE_STRIP
   * `6` TRIANGLE_FAN

#### primitive.targets

An array of Morph Targets, each  Morph Target is a dictionary mapping attributes (only `POSITION`, `NORMAL`, and `TANGENT` supported) to their deviations in the Morph Target.

* **Type**: `object` `[1-*]`
* **Required**: No

#### primitive.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### primitive.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-sampler"></a>
### sampler

Texture sampler properties for filtering and wrapping modes.

**Related WebGL functions**: `texParameterf()`

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**magFilter**|`integer`|Magnification filter.|No|
|**minFilter**|`integer`|Minification filter.|No|
|**wrapS**|`integer`|s wrapping mode.|No, default: `10497`|
|**wrapT**|`integer`|t wrapping mode.|No, default: `10497`|
|**name**|`string`|The user-defined name of this object.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [sampler.schema.json](schema/sampler.schema.json)

#### sampler.magFilter

Magnification filter.  Valid values correspond to WebGL enums: `9728` (NEAREST) and `9729` (LINEAR).

* **Type**: `integer`
* **Required**: No
* **Allowed values**:
   * `9728` NEAREST
   * `9729` LINEAR
* **Related WebGL functions**: `texParameterf()` with pname equal to TEXTURE_MAG_FILTER

#### sampler.minFilter

Minification filter.  All valid values correspond to WebGL enums.

* **Type**: `integer`
* **Required**: No
* **Allowed values**:
   * `9728` NEAREST
   * `9729` LINEAR
   * `9984` NEAREST_MIPMAP_NEAREST
   * `9985` LINEAR_MIPMAP_NEAREST
   * `9986` NEAREST_MIPMAP_LINEAR
   * `9987` LINEAR_MIPMAP_LINEAR
* **Related WebGL functions**: `texParameterf()` with pname equal to TEXTURE_MIN_FILTER

#### sampler.wrapS

S (U) wrapping mode.  All valid values correspond to WebGL enums.

* **Type**: `integer`
* **Required**: No, default: `10497`
* **Allowed values**:
   * `33071` CLAMP_TO_EDGE
   * `33648` MIRRORED_REPEAT
   * `10497` REPEAT
* **Related WebGL functions**: `texParameterf()` with pname equal to TEXTURE_WRAP_S

#### sampler.wrapT

T (V) wrapping mode.  All valid values correspond to WebGL enums.

* **Type**: `integer`
* **Required**: No, default: `10497`
* **Allowed values**:
   * `33071` CLAMP_TO_EDGE
   * `33648` MIRRORED_REPEAT
   * `10497` REPEAT
* **Related WebGL functions**: `texParameterf()` with pname equal to TEXTURE_WRAP_T

#### sampler.name

The user-defined name of this object.  This is not necessarily unique, e.g., an accessor and a buffer could have the same name, or two accessors could even have the same name.

* **Type**: `string`
* **Required**: No

#### sampler.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### sampler.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-scene"></a>
### scene

The root nodes of a scene.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**nodes**|`integer` `[1-*]`|The indices of each root node.|No|
|**name**|`string`|The user-defined name of this object.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [scene.schema.json](schema/scene.schema.json)

#### scene.nodes

The indices of each root node.

* **Type**: `integer` `[1-*]`
   * Each element in the array must be unique.
   * Each element in the array must be greater than or equal to `0`.
* **Required**: No

#### scene.name

The user-defined name of this object.  This is not necessarily unique, e.g., an accessor and a buffer could have the same name, or two accessors could even have the same name.

* **Type**: `string`
* **Required**: No

#### scene.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### scene.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-skin"></a>
### skin

Joints and matrices defining a skin.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**inverseBindMatrices**|`integer`|The index of the accessor containing the floating-point 4x4 inverse-bind matrices.  The default is that each matrix is a 4x4 identity matrix, which implies that inverse-bind matrices were pre-applied.|No|
|**skeleton**|`integer`|The index of the node used as a skeleton root. When undefined, joints transforms resolve to scene root.|No|
|**joints**|`integer` `[1-*]`|Indices of skeleton nodes, used as joints in this skin.| :white_check_mark: Yes|
|**name**|`string`|The user-defined name of this object.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [skin.schema.json](schema/skin.schema.json)

#### skin.inverseBindMatrices

The index of the accessor containing the floating-point 4x4 inverse-bind matrices.  The default is that each matrix is a 4x4 identity matrix, which implies that inverse-bind matrices were pre-applied.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### skin.skeleton

The index of the node used as a skeleton root. When undefined, joints transforms resolve to scene root.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### skin.joints :white_check_mark: 

Indices of skeleton nodes, used as joints in this skin.  The array length must be the same as the `count` property of the `inverseBindMatrices` accessor (when defined).

* **Type**: `integer` `[1-*]`
   * Each element in the array must be unique.
   * Each element in the array must be greater than or equal to `0`.
* **Required**: Yes

#### skin.name

The user-defined name of this object.  This is not necessarily unique, e.g., an accessor and a buffer could have the same name, or two accessors could even have the same name.

* **Type**: `string`
* **Required**: No

#### skin.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### skin.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-sparse"></a>
### sparse

Sparse storage of attributes that deviate from their initialization value.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**count**|`integer`|Number of entries stored in the sparse array.| :white_check_mark: Yes|
|**indices**|`object`|Index array of size `count` that points to those accessor attributes that deviate from their initialization value. Indices must strictly increase.| :white_check_mark: Yes|
|**values**|`object`|Array of size `count` times number of components, storing the displaced accessor attributes pointed by [`indices`](#reference-indices). Substituted values must have the same `componentType` and number of components as the base accessor.| :white_check_mark: Yes|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [accessor.sparse.schema.json](schema/accessor.sparse.schema.json)

#### sparse.count :white_check_mark: 

The number of attributes encoded in this sparse accessor.

* **Type**: `integer`
* **Required**: Yes
* **Minimum**: ` >= 1`

#### sparse.indices :white_check_mark: 

Index array of size `count` that points to those accessor attributes that deviate from their initialization value. Indices must strictly increase.

* **Type**: `object`
* **Required**: Yes

#### sparse.values :white_check_mark: 

Array of size `count` times number of components, storing the displaced accessor attributes pointed by [`indices`](#reference-indices). Substituted values must have the same `componentType` and number of components as the base accessor.

* **Type**: `object`
* **Required**: Yes

#### sparse.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### sparse.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-target"></a>
### target

The index of the node and TRS property that an animation channel targets.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**node**|`integer`|The index of the node to target.|No|
|**path**|`string`|The name of the node's TRS property to modify, or the "weights" of the Morph Targets it instantiates. For the "translation" property, the values that are provided by the sampler are the translation along the x, y, and z axes. For the "rotation" property, the values are a quaternion in the order (x, y, z, w), where w is the scalar. For the "scale" property, the values are the scaling factors along the x, y, and z axes.| :white_check_mark: Yes|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [animation.channel.target.schema.json](schema/animation.channel.target.schema.json)

#### target.node

The index of the node to target.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### target.path :white_check_mark: 

The name of the node's TRS property to modify, or the "weights" of the Morph Targets it instantiates. For the "translation" property, the values that are provided by the sampler are the translation along the x, y, and z axes. For the "rotation" property, the values are a quaternion in the order (x, y, z, w), where w is the scalar. For the "scale" property, the values are the scaling factors along the x, y, and z axes.

* **Type**: `string`
* **Required**: Yes
* **Allowed values**:
   * `"translation"`
   * `"rotation"`
   * `"scale"`
   * `"weights"`

#### target.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### target.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-texture"></a>
### texture

A texture and its sampler.

**Related WebGL functions**: `createTexture()`, `deleteTexture()`, `bindTexture()`, `texImage2D()`, and `texParameterf()`

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**sampler**|`integer`|The index of the sampler used by this texture. When undefined, a sampler with repeat wrapping and auto filtering should be used.|No|
|**source**|`integer`|The index of the image used by this texture.|No|
|**name**|`string`|The user-defined name of this object.|No|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [texture.schema.json](schema/texture.schema.json)

#### texture.sampler

The index of the sampler used by this texture. When undefined, a sampler with repeat wrapping and auto filtering should be used.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### texture.source

The index of the image used by this texture.

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### texture.name

The user-defined name of this object.  This is not necessarily unique, e.g., an accessor and a buffer could have the same name, or two accessors could even have the same name.

* **Type**: `string`
* **Required**: No

#### texture.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### texture.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-textureinfo"></a>
### textureInfo

Reference to a texture.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**index**|`integer`|The index of the texture.| :white_check_mark: Yes|
|**texCoord**|`integer`|The set index of texture's TEXCOORD attribute used for texture coordinate mapping.|No, default: `0`|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [textureInfo.schema.json](schema/textureInfo.schema.json)

#### textureInfo.index :white_check_mark: 

The index of the texture.

* **Type**: `integer`
* **Required**: Yes
* **Minimum**: ` >= 0`

#### textureInfo.texCoord

This integer value is used to construct a string in the format `TEXCOORD_<set index>` which is a reference to a key in mesh.primitives.attributes (e.g. A value of `0` corresponds to `TEXCOORD_0`). Mesh must have corresponding texture coordinate attributes for the material to be applicable to it.

* **Type**: `integer`
* **Required**: No, default: `0`
* **Minimum**: ` >= 0`

#### textureInfo.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### textureInfo.extras

Application-specific data.

* **Type**: `any`
* **Required**: No




---------------------------------------
<a name="reference-values"></a>
### values

Array of size `accessor.sparse.count` times number of components storing the displaced accessor attributes pointed by `accessor.sparse.indices`.

**Properties**

|   |Type|Description|Required|
|---|----|-----------|--------|
|**bufferView**|`integer`|The index of the bufferView with sparse values. Referenced bufferView can't have ARRAY_BUFFER or ELEMENT_ARRAY_BUFFER target.| :white_check_mark: Yes|
|**byteOffset**|`integer`|The offset relative to the start of the bufferView in bytes. Must be aligned.|No, default: `0`|
|**extensions**|`object`|Dictionary object with extension-specific objects.|No|
|**extras**|`any`|Application-specific data.|No|

Additional properties are allowed.

* **JSON schema**: [accessor.sparse.values.schema.json](schema/accessor.sparse.values.schema.json)

#### values.bufferView :white_check_mark: 

The index of the bufferView with sparse values. Referenced bufferView can't have ARRAY_BUFFER or ELEMENT_ARRAY_BUFFER target.

* **Type**: `integer`
* **Required**: Yes
* **Minimum**: ` >= 0`

#### values.byteOffset

The offset relative to the start of the bufferView in bytes. Must be aligned.

* **Type**: `integer`
* **Required**: No, default: `0`
* **Minimum**: ` >= 0`

#### values.extensions

Dictionary object with extension-specific objects.

* **Type**: `object`
* **Required**: No
* **Type of each property**: extension

#### values.extras

Application-specific data.

* **Type**: `any`
* **Required**: No


# Acknowledgments
* Sarah Chow, Cesium
* Tom Fili, Cesium
* Darryl Gough
* Eric Haines, Autodesk
* Yu Chen Hou
* Scott Hunter, Analytical Graphics, Inc.
* Brandon Jones, Google
* Sean Lilley, Cesium
* Juan Linietsky, Godot Engine
* Matthew McMullan
* Mohamad Moneimne, University of Pennsylvania
* Kai Ninomiya, formerly Cesium
* Cedric Pinson, Sketchfab
* Jeff Russell, Marmoset
* Miguel Sousa, Fraunhofer IGD
* Timo Sturm, Fraunhofer IGD
* Rob Taglang, Cesium
* Maik Thöner, Fraunhofer IGD
* Steven Vergenz, AltspaceVR
* Corentin Wallez, Google
* Alex Wood, Analytical Graphics, Inc


# Appendix A: Tangent Space Recalculation

**TODO**

# Appendix B: BRDF Implementation

*This section is non-normative.*

The glTF spec is designed to allow applications to choose different lighting implementations based on their requirements.

An implementation sample is available at https://github.com/KhronosGroup/glTF-WebGL-PBR/ and provides an example of a WebGL implementation of a standard BRDF based on the glTF material parameters.

As previously defined

`const dielectricSpecular = rgb(0.04, 0.04, 0.04)`
<br>
`const black = rgb(0, 0, 0)`

*c<sub>diff</sub>* = `lerp(baseColor.rgb * (1 - dielectricSpecular.r), black, metallic)`
<br>
*F<sub>0</sub>* = `lerp(dieletricSpecular, baseColor.rgb, metallic)`
<br>
*&alpha;* = `roughness ^ 2`

Additionally,  
*V* is the eye vector to the shading location  
*L* is the vector from the light to the shading location  
*N* is the surface normal in the same space as the above values  
*H* is the half vector, where *H* = normalize(*L*+*V*)  

The core lighting equation the sample uses is the Schlick BRDF model from [An Inexpensive BRDF Model for Physically-based Rendering](https://www.cs.virginia.edu/~jdl/bib/appearance/analytic%20models/schlick94b.pdf)

![](figures/lightingSum.PNG)

Below are common implementations for the various terms found in the lighting equation.

### Surface Reflection Ratio (F)

**Fresnel Schlick**

Simplified implementation of Fresnel from [An Inexpensive BRDF Model for Physically based Rendering](https://www.cs.virginia.edu/~jdl/bib/appearance/analytic%20models/schlick94b.pdf) by Christophe Schlick.

![](figures/lightingF.PNG)

### Geometric Occlusion (G)

**Schlick**

Implementation of microfacet occlusion from [An Inexpensive BRDF Model for Physically based Rendering](https://www.cs.virginia.edu/~jdl/bib/appearance/analytic%20models/schlick94b.pdf) by Christophe Schlick.

![](figures/lightingG.PNG)

### Microfaced Distribution (D)

**Trowbridge-Reitz**

Implementation of microfaced distrubtion from [Average Irregularity Representation of a Roughened Surface for Ray Reflection](https://www.osapublishing.org/josa/abstract.cfm?uri=josa-65-5-531) by T. S. Trowbridge, and K. P. Reitz

![](figures/lightingD.PNG)

### Diffuse Term (diffuse)

**Lambert**

Implementation of diffuse from [Lambert's Photometria](https://archive.org/details/lambertsphotome00lambgoog) by Johann Heinrich Lambert

![](figures/lightingDiff.PNG)

# Appendix C: Spline Interpolation

Animations in glTF support spline interpolation with a cubic spline.

The keyframes of a cubic spline in glTF have input and output values where each input value corresponds to three output values: in-tangent, spline vertex, and out-tangent.

Given a set of keyframes

&nbsp;&nbsp;&nbsp;&nbsp;Input *t*<sub>*k*</sub> and output in-tangent ***a***<sub>k</sub>, vertex ***v***<sub>*k*</sub>, and out-tangent ***b***<sub>k</sub> for *k* = 1,...,*n*

A spline segment between two keyframes is represented in a cubic Hermite spline form

&nbsp;&nbsp;&nbsp;&nbsp;***p***(*t*) = (2*t*<sup>3</sup> - 3*t*<sup>2</sup> + 1)***p***<sub>0</sub> + (*t<sup>3</sup>* - 2*t*<sup>2</sup> + *t*)***m***<sub>0</sub> + (-2*t*<sup>3</sup> + 3*t*<sup>2</sup>)***p***<sub>1</sub> + (*t*<sup>3</sup> - *t*<sup>2</sup>)***m***<sub>1</sub>

Where

&nbsp;&nbsp;&nbsp;&nbsp;*t* is a value between 0 and 1  
&nbsp;&nbsp;&nbsp;&nbsp;***p***<sub>0</sub> is the starting vertex at *t* = 0  
&nbsp;&nbsp;&nbsp;&nbsp;***m***<sub>0</sub> is the starting tangent at *t* = 0  
&nbsp;&nbsp;&nbsp;&nbsp;***p***<sub>1</sub> is the ending vertex at *t* = 1  
&nbsp;&nbsp;&nbsp;&nbsp;***m***<sub>1</sub> is the ending tangent at *t* = 1  
&nbsp;&nbsp;&nbsp;&nbsp;***p***(*t*) is the resulting value  

Where at input offset *t*<sub>*current*</sub> with keyframe index *k*

&nbsp;&nbsp;&nbsp;&nbsp;*t* = (*t*<sub>*current*</sub> - *t*<sub>*k*</sub>) / (*t*<sub>*k*+1</sub> - *t*<sub>*k*</sub>)  
&nbsp;&nbsp;&nbsp;&nbsp;***p***<sub>0</sub> = ***v***<sub>*k*</sub>  
&nbsp;&nbsp;&nbsp;&nbsp;***m***<sub>0</sub> = (*t*<sub>*k*+1</sub> - *t*<sub>*k*</sub>)***b***<sub>k</sub>  
&nbsp;&nbsp;&nbsp;&nbsp;***p***<sub>1</sub> = ***v***<sub>*k*+1</sub>  
&nbsp;&nbsp;&nbsp;&nbsp;***m***<sub>1</sub> = (*t*<sub>*k*+1</sub> - *t*<sub>*k*</sub>)***a***<sub>k+1</sub>  

When the sampler targets a node's rotation property, the resulting ***p***(*t*) quaternion must be normalized before applying the result to the node's rotation.

> **Implementation Note:** When writing out rotation output values, exporters should take care to not write out values which can result in an invalid quaternion with all zero values. This can be achieved by ensuring the output values never have both -***q*** and ***q*** in the same spline.

> **Implementation Note:** The first in-tangent ***a***<sub>1</sub> and last out-tangent ***b***<sub>*n*</sub> should be zeros as they are not used in the spline calculations.

# Appendix D: Full Khronos Copyright Statement

Copyright 2013-2017 The Khronos Group Inc. 

Some parts of this Specification are purely informative and do not define requirements
necessary for compliance and so are outside the Scope of this Specification. These
parts of the Specification are marked as being non-normative, or identified as 
**Implementation Notes**.
 
Where this Specification includes normative references to external documents, only the
specifically identified sections and functionality of those external documents are in
Scope. Requirements defined by external documents not created by Khronos may contain
contributions from non-members of Khronos not covered by the Khronos Intellectual
Property Rights Policy.

This specification is protected by copyright laws and contains material proprietary 
to Khronos. Except as described by these terms, it or any components 
may not be reproduced, republished, distributed, transmitted, displayed, broadcast 
or otherwise exploited in any manner without the express prior written permission 
of Khronos. 

This specification has been created under the Khronos Intellectual Property Rights 
Policy, which is Attachment A of the Khronos Group Membership Agreement available at
www.khronos.org/files/member_agreement.pdf. Khronos grants a conditional 
copyright license to use and reproduce the unmodified specification for any purpose, 
without fee or royalty, EXCEPT no licenses to any patent, trademark or other 
intellectual property rights are granted under these terms. Parties desiring to 
implement the specification and make use of Khronos trademarks in relation to that 
implementation, and receive reciprocal patent license protection under the Khronos 
IP Policy must become Adopters and confirm the implementation as conformant under 
the process defined by Khronos for this specification; 
see https://www.khronos.org/adopters.

Khronos makes no, and expressly disclaims any, representations or warranties, 
express or implied, regarding this specification, including, without limitation: 
merchantability, fitness for a particular purpose, non-infringement of any 
intellectual property, correctness, accuracy, completeness, timeliness, and 
reliability. Under no circumstances will Khronos, or any of its Promoters, 
Contributors or Members, or their respective partners, officers, directors, 
employees, agents or representatives be liable for any damages, whether direct, 
indirect, special or consequential damages for lost revenues, lost profits, or 
otherwise, arising from or in connection with these materials.

Vulkan is a registered trademark and Khronos, OpenXR, SPIR, SPIR-V, SYCL, WebGL, 
WebCL, OpenVX, OpenVG, EGL, COLLADA, glTF, NNEF, OpenKODE, OpenKCAM, StreamInput, 
OpenWF, OpenSL ES, OpenMAX, OpenMAX AL, OpenMAX IL, OpenMAX DL, OpenML and DevU are 
trademarks of The Khronos Group Inc. ASTC is a trademark of ARM Holdings PLC, 
OpenCL is a trademark of Apple Inc. and OpenGL and OpenML are registered trademarks 
and the OpenGL ES and OpenGL SC logos are trademarks of Silicon Graphics 
International used under license by Khronos. All other product names, trademarks, 
and/or company names are used solely for identification and belong to their 
respective owners.