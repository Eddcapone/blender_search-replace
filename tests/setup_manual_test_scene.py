# SPDX-License-Identifier: GPL-2.0-or-later
"""
Baut eine Demo-/Testszene fuer die MANUELLE Bedienung der "Search & Replace"-
Extension auf (Bedienung im N-Panel > Tools > "Search&Replace").

Ausfuehren: im Blender Text-Editor oeffnen und mit Alt+P starten.
Erneutes Ausfuehren ist sicher - vorhandene Demo-Objekte (Praefix "SNR_DEMO_")
werden vorher entfernt und frisch neu angelegt.

Nur aufraeumen ohne Neuaufbau: CLEANUP_ONLY unten auf True setzen und erneut
ausfuehren.

Siehe README_Test.md im selben Ordner fuer die Schritt-fuer-Schritt-Anleitung.
"""

import bpy
import math

PREFIX = "SNR_DEMO_"
CLEANUP_ONLY = False

_CUBE_VERTS = [
    (-0.4, -0.4, -0.4), (0.4, -0.4, -0.4), (0.4, 0.4, -0.4), (-0.4, 0.4, -0.4),
    (-0.4, -0.4, 0.4), (0.4, -0.4, 0.4), (0.4, 0.4, 0.4), (-0.4, 0.4, 0.4),
]
_CUBE_FACES = [
    (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
    (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
]


def cleanup():
    for obj in list(bpy.data.objects):
        if obj.name.startswith(PREFIX):
            mesh = obj.data
            bpy.data.objects.remove(obj, do_unlink=True)
            if mesh is not None and getattr(mesh, "users", 0) == 0:
                bpy.data.meshes.remove(mesh)
    for mat in list(bpy.data.materials):
        if mat.name.startswith(PREFIX):
            bpy.data.materials.remove(mat)
    for img in list(bpy.data.images):
        if img.name.startswith(PREFIX):
            bpy.data.images.remove(img)
    for mesh in list(bpy.data.meshes):
        if mesh.name.startswith(PREFIX) and mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    coll = bpy.data.collections.get(PREFIX + "Testszene")
    if coll:
        bpy.data.collections.remove(coll)


def deselect_all():
    for obj in bpy.context.scene.objects:
        obj.select_set(False)


def add_cube(name, location, rotation, scale, collection):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(_CUBE_VERTS, [], _CUBE_FACES)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    obj.rotation_euler = rotation
    obj.scale = scale
    collection.objects.link(obj)
    return obj


def make_flat_image(name, color):
    img = bpy.data.images.new(name, width=8, height=8)
    pixels = list(color) * (8 * 8)
    img.pixels = pixels
    return img


def make_colored_material(name, color):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    if mat.use_nodes:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
    return mat


def make_tex_material(name, image):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    tex_node = nt.nodes.new("ShaderNodeTexImage")
    tex_node.image = image
    tex_node.location = (-300, 300)
    nt.nodes.active = tex_node
    bsdf = nt.nodes.get("Principled BSDF")
    if bsdf:
        nt.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def build():
    cleanup()

    coll = bpy.data.collections.new(PREFIX + "Testszene")
    bpy.context.scene.collection.children.link(coll)

    # ------------------------------------------------------------------
    # Bereich 1: Objekte  (y = 0)
    # ------------------------------------------------------------------
    src_a = add_cube(PREFIX + "Obj_Source_A", (0, 0, 0), (0, 0, math.radians(45)), (1, 1, 1), coll)
    src_b = add_cube(PREFIX + "Obj_Source_B", (2, 0, 0), (math.radians(30), 0, 0), (2, 2, 2), coll)
    add_cube(PREFIX + "Obj_Source_C_nicht_ausgewaehlt", (4, 0, 0), (0, 0, 0), (0.5, 0.5, 0.5), coll)

    bpy.ops.mesh.primitive_uv_sphere_add(location=(8, 0, 0))
    obj_sphere = bpy.context.active_object
    obj_sphere.name = PREFIX + "Obj_ReplaceWithSphere"
    for c in list(obj_sphere.users_collection):
        c.objects.unlink(obj_sphere)
    coll.objects.link(obj_sphere)

    # ------------------------------------------------------------------
    # Bereich 2: Materialien  (y = 3)
    # ------------------------------------------------------------------
    mat_x = make_colored_material(PREFIX + "Mat_Rot_X", (0.8, 0.05, 0.05, 1.0))
    mat_y = make_colored_material(PREFIX + "Mat_Gruen_Y", (0.05, 0.7, 0.1, 1.0))
    mat_z = make_colored_material(PREFIX + "Mat_Blau_Z_unbenutzt", (0.05, 0.2, 0.8, 1.0))

    mat_cube1 = add_cube(PREFIX + "Mat_Cube1_nurX", (0, 3, 0), (0, 0, 0), (1, 1, 1), coll)
    mat_cube1.data.materials.append(mat_x)

    mat_cube2 = add_cube(PREFIX + "Mat_Cube2_X_dann_Y", (2, 3, 0), (0, 0, 0), (1, 1, 1), coll)
    mat_cube2.data.materials.append(mat_x)
    mat_cube2.data.materials.append(mat_y)

    mat_cube3 = add_cube(PREFIX + "Mat_Cube3_Y_dann_X", (4, 3, 0), (0, 0, 0), (1, 1, 1), coll)
    mat_cube3.data.materials.append(mat_y)
    mat_cube3.data.materials.append(mat_x)

    add_cube(PREFIX + "Mat_Cube4_nurY", (6, 3, 0), (0, 0, 0), (1, 1, 1), coll)
    bpy.data.objects[PREFIX + "Mat_Cube4_nurY"].data.materials.append(mat_y)

    # ------------------------------------------------------------------
    # Bereich 3: Texturen  (y = 6)
    # ------------------------------------------------------------------
    img_a = make_flat_image(PREFIX + "Bild_Rot_A", (0.8, 0.05, 0.05, 1.0))
    img_b = make_flat_image(PREFIX + "Bild_Gruen_B", (0.05, 0.7, 0.1, 1.0))
    make_flat_image(PREFIX + "Bild_Blau_C_unbenutzt", (0.05, 0.2, 0.8, 1.0))

    tex_mat1 = make_tex_material(PREFIX + "TexMat1_BildA", img_a)
    tex_mat2 = make_tex_material(PREFIX + "TexMat2_BildA", img_a)
    tex_mat3 = make_tex_material(PREFIX + "TexMat3_BildB", img_b)

    tex_cube1 = add_cube(PREFIX + "Tex_Cube1", (0, 6, 0), (0, 0, 0), (1, 1, 1), coll)
    tex_cube1.data.materials.append(tex_mat1)

    tex_cube2 = add_cube(PREFIX + "Tex_Cube2", (2, 6, 0), (0, 0, 0), (1, 1, 1), coll)
    tex_cube2.data.materials.append(tex_mat2)

    tex_cube3 = add_cube(PREFIX + "Tex_Cube3", (4, 6, 0), (0, 0, 0), (1, 1, 1), coll)
    tex_cube3.data.materials.append(tex_mat3)

    # ------------------------------------------------------------------
    # Vorauswahl: Object-Source_A/B ausgewaehlt, damit man sofort testen kann
    # ------------------------------------------------------------------
    deselect_all()
    src_a.select_set(True)
    src_b.select_set(True)
    bpy.context.view_layer.objects.active = src_a

    print("Demo-Szene angelegt (Praefix 'SNR_DEMO_').")
    print(f"Objekte: {src_a.name}, {src_b.name} vorausgewaehlt. Ziel zur Auswahl: {obj_sphere.name}.")
    print(f"Materialien: {mat_x.name} (rot), {mat_y.name} (gruen), {mat_z.name} (blau, unbenutzt = Replace-Ziel).")
    print(f"Texturen: {img_a.name} (rot), {img_b.name} (gruen), "
          f"{PREFIX}Bild_Blau_C_unbenutzt (blau, unbenutzt = Replace-Ziel).")
    print("N-Panel > Tools-Tab > 'Search&Replace' oeffnen und README_Test.md folgen.")


if CLEANUP_ONLY:
    cleanup()
    print("Demo-Objekte entfernt.")
else:
    build()
