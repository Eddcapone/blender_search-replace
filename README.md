# blender_search-replace

A Blender extension that provides one panel to search and replace **objects**,
**materials**, and **textures** in the current scene.

- **Objects** — list all scene objects, jump to one by clicking it, and
  replace the current selection with another object (optionally keeping each
  replaced object's rotation and scale).
- **Materials** — search which objects use a given material (across all of
  their material slots) and replace it everywhere it's found. Includes a
  "Random" operator to assign random existing materials to the selected
  objects.
- **Textures** — search which objects have a given image active on their
  active material's Image Texture node, and replace that image everywhere
  it's found.

<img width="3834" height="2083" alt="grafik" src="https://github.com/user-attachments/assets/9099dd5b-9a14-43b9-ab2f-931b9d863970" />

## Compatibility

Since version `5.2.0` this is packaged as a Blender **extension** (the
format Blender uses from 4.2 onward), targeting Blender 4.2+ and tested
against Blender 5.2 LTS. Earlier tagged versions (`1.0.0`, `2.0.0`) were
single-file legacy add-ons for older Blender releases and are no longer
maintained.

Note on "textures": Blender removed its old texture-slot system
(`bpy.data.textures`, `material.active_texture`) in 2.80 when materials
became fully node-based. The closest modern equivalent — and what this
extension searches/replaces — is the **active node** in a material's shader
node tree (`material.node_tree.nodes.active`), when that node is an Image
Texture node. Click the node in the Shader Editor to make it "active" before
searching for it here.

## Installation

1. Download this repository (or a release zip) as a folder.
2. In Blender: *Edit > Preferences > Get Extensions* (or *Add-ons*) > install
   from disk, pointing at this folder (or a zipped version of it).
3. Enable "Search & Replace".

The panel appears in the 3D Viewport's sidebar (`N`), under the **Tools**
tab, while in Object Mode.

## Testing

See [`tests/README_Test.md`](tests/README_Test.md) for an automated
regression test script and a script that builds a hands-on demo scene
covering all three panel sections.

## License

GPL-2.0-or-later, see [LICENSE](LICENSE).
