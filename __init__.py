# SPDX-FileCopyrightText: Eduard Fekete, CoDEmanX
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Search & Replace - combined panel to search/replace objects, materials and
textures in one place, matching the original (2013) all-in-one addon layout.

"Texture" here means the image used by the active Image Texture node of an
object's active material (node_tree.nodes.active) - the closest modern
equivalent of the legacy Blender-Internal "active texture slot" concept,
which was removed from Blender in 2.80 along with bpy.data.textures-based
material texturing.
"""

import bpy
import random
from bpy.props import (
    BoolProperty,
    StringProperty,
    CollectionProperty,
    PointerProperty,
    IntProperty,
)

#
# globals
#
obj_list = []
mat_obj_list = []
tex_obj_list = []


#
# shared list item + UIList (used for all three lists)
#
class SNR_NameItem(bpy.types.PropertyGroup):
    name: StringProperty()


class SNR_UL_name_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(icon="OBJECT_DATA", text=item.name)


#
# panel
#
class VIEW3D_PT_search_and_replace(bpy.types.Panel):
    bl_label = "Search&Replace"
    bl_category = "Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def draw(self, context):
        layout = self.layout
        props = context.window_manager.snr_properties

        # --- Options -----------------------------------------------------
        layout.label(text="Options:")
        row = layout.row(align=True)
        row.prop(props, "select", text="Always deselect")
        row.prop(props, "copy_rotation", text="Copy Rot&Scale")

        # --- Object search/replace -----------------------------------------
        layout.separator()
        layout.label(text="All Objects from {}".format(context.scene.name))
        layout.operator(VIEW3D_OT_refresh.bl_idname, text="", icon="FILE_REFRESH")
        row = layout.row(align=True)
        row.operator("replace_selected.objects", text="Replace selection with :", icon="FILE_REFRESH")
        row.prop_search(props, "srch_replace", bpy.data, "objects", text="")
        layout.template_list("SNR_UL_name_list", "obj", props, "srch_objects", props, "srch_index")

        # --- Material search/replace -----------------------------------------
        layout.separator()
        row = layout.row(align=True)
        row.label(text="Search Material")
        row.label(text="New Material")

        row = layout.row(align=True)
        row.operator(VIEW3D_OT_refresh.bl_idname, text="", icon="FILE_REFRESH")
        row.prop_search(props, "material", props, "all_materials", text="")
        row.prop_search(props, "mat_replace", bpy.data, "materials", text="")

        row = layout.row(align=True)
        row.operator("replace_all.materials", text="Replace All", icon="SEQ_CHROMA_SCOPE")
        row.operator("random.materials", text="Random")

        layout.template_list("SNR_UL_name_list", "mat", props, "mat_objects", props, "mat_index")

        # --- Texture search/replace -----------------------------------------
        layout.separator()
        row = layout.row(align=True)
        row.label(text="Search Texture")
        row.label(text="New Texture")

        row = layout.row(align=True)
        row.operator(VIEW3D_OT_refresh.bl_idname, text="", icon="FILE_REFRESH")
        row.prop_search(props, "texture", props, "all_textures", text="")
        row.prop_search(props, "tex_replace", bpy.data, "images", text="")

        layout.operator("replace_all.textures", text="Replace All", icon="SEQ_CHROMA_SCOPE")

        layout.template_list("SNR_UL_name_list", "tex", props, "tex_objects", props, "tex_index")


#
# refresh
#
class VIEW3D_OT_refresh(bpy.types.Operator):
    """Refresh all lists"""
    bl_idname = "view3d.obj_search_refresh"
    bl_label = "Refresh"

    def execute(self, context):
        props = context.window_manager.snr_properties
        update_objects(props, context)
        update_material(props, context)
        update_textures(props, context)
        return {'FINISHED'}


#
# jump-to-object (shared by all three lists)
#
def jump_to_object(context, ob):
    try:
        props = context.window_manager.snr_properties
        view_layer = context.view_layer
        if props.select:
            for o in view_layer.objects:
                o.select_set(False)

        ob.select_set(True)
        view_layer.objects.active = ob

        window = context.window
        screen = window.screen if window else None
        area = next((a for a in screen.areas if a.type == 'VIEW_3D'), None) if screen else None
        if area is None:
            return False
        region = next((r for r in area.regions if r.type == 'WINDOW'), None)
        with context.temp_override(window=window, area=area, region=region):
            return bpy.ops.view3d.view_selected() == {'FINISHED'}
    except Exception:
        return False


#
# ---------------------------------------------------------------------------
# Objects
# ---------------------------------------------------------------------------
#
def update_objects(self, context):
    self.srch_index = -1
    self.srch_objects.clear()
    obj_list.clear()

    for ob in context.scene.objects:
        obj_list.append(ob.name)
        item = self.srch_objects.add()
        item.name = ob.name


def update_obj_search_index(self, context):
    if len(self.srch_objects) < 1 or self.srch_index < 0:
        return
    try:
        ob_name = self.srch_objects[self.srch_index].name
    except IndexError:
        print("Object Search: Bad objects list index")
        return

    ob = context.scene.objects.get(ob_name)
    if ob is not None:
        jump_to_object(context, ob)


class VIEW3D_OT_replace_selected_objects(bpy.types.Operator):
    """Replace all selected objects with the object chosen from the drop-down menu"""
    bl_idname = "replace_selected.objects"
    bl_label = "Replace"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = context.window_manager.snr_properties

        if props.srch_replace == "":
            return {'CANCELLED'}

        replace_obj = scene.objects.get(props.srch_replace)
        if replace_obj is None:
            return {'CANCELLED'}

        selected = [obj for obj in context.selected_objects if obj.name != replace_obj.name]
        if not selected:
            return {'CANCELLED'}

        # Build full independent copies via bpy.data directly (no bpy.ops.object.duplicate_move
        # / snap_selected_to_cursor / object.delete chain) so the whole replace happens as a
        # single undo step. Chaining several bpy.ops calls here used to push one undo step per
        # sub-operator, which could corrupt the depsgraph on Ctrl+Z and crash Blender.
        new_objects = []
        for obj in selected:
            new_obj = replace_obj.copy()
            if replace_obj.data is not None:
                new_obj.data = replace_obj.data.copy()
            new_obj.location = obj.location.copy()

            if props.copy_rotation:
                new_obj.rotation_mode = obj.rotation_mode
                if obj.rotation_mode == 'QUATERNION':
                    new_obj.rotation_quaternion = obj.rotation_quaternion.copy()
                elif obj.rotation_mode == 'AXIS_ANGLE':
                    new_obj.rotation_axis_angle = obj.rotation_axis_angle[:]
                else:
                    new_obj.rotation_euler = obj.rotation_euler.copy()
                new_obj.scale = obj.scale.copy()
            # else: keep replace_obj's own rotation/scale, already carried over by .copy()

            target_collections = obj.users_collection or (scene.collection,)
            for coll in target_collections:
                coll.objects.link(new_obj)

            new_objects.append(new_obj)

        for obj in selected:
            bpy.data.objects.remove(obj, do_unlink=True)

        for o in scene.objects:
            o.select_set(False)
        for new_obj in new_objects:
            new_obj.select_set(True)
        context.view_layer.objects.active = new_objects[-1]

        update_objects(props, context)
        return {'FINISHED'}


#
# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------
#
def get_assigned_materials(self, context):
    scn = context.scene
    allm = self.all_materials
    allm.clear()

    local_all_mat = []
    for obj in scn.objects:
        for slot in obj.material_slots:
            mat = slot.material
            if mat is None or mat.name in local_all_mat:
                continue
            item = allm.add()
            item.name = mat.name
            local_all_mat.append(mat.name)

    return local_all_mat


def update_material(self, context):
    scn = context.scene
    self.mat_index = -1
    self.mat_objects.clear()
    mat_obj_list.clear()

    get_assigned_materials(self, context)

    if not self.material:
        return

    for obj in scn.objects:
        for slot in obj.material_slots:
            if slot.material is not None and slot.material.name == self.material:
                item = self.mat_objects.add()
                item.name = obj.name
                mat_obj_list.append(obj.name)
                break


def update_mat_index(self, context):
    if len(self.mat_objects) < 1 or self.mat_index < 0:
        return
    try:
        ob_name = self.mat_objects[self.mat_index].name
    except IndexError:
        print("Material Object Search: Bad objects list index")
        return

    ob = context.scene.objects.get(ob_name)
    if ob is not None:
        jump_to_object(context, ob)


class VIEW3D_OT_replace_all_materials(bpy.types.Operator):
    """Replace the searched material with the chosen replacement on all matched objects"""
    bl_idname = "replace_all.materials"
    bl_label = "Replace"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        props = context.window_manager.snr_properties

        if not props.material or not props.mat_replace:
            return {'CANCELLED'}

        replace_mat = bpy.data.materials.get(props.mat_replace)
        if replace_mat is None:
            return {'CANCELLED'}

        for obj in scn.objects:
            if obj.name not in mat_obj_list:
                continue
            for slot in obj.material_slots:
                if slot.material is not None and slot.material.name == props.material:
                    slot.material = replace_mat

        return {'FINISHED'}


class VIEW3D_OT_random_materials(bpy.types.Operator):
    """Assign a random existing material to each material slot of the selected objects"""
    bl_idname = "random.materials"
    bl_label = "Random"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        materials = list(bpy.data.materials)
        if not materials:
            return {'CANCELLED'}

        for obj in context.selected_objects:
            for slot in obj.material_slots:
                slot.material = random.choice(materials)

        return {'FINISHED'}


#
# ---------------------------------------------------------------------------
# Textures
#
# "Texture" = the image on the active Image Texture node of an object's
# active material (node_tree.nodes.active). This is the closest modern
# equivalent of the legacy "active texture slot" - Blender removed
# bpy.data.textures-based material texturing in 2.80.
# ---------------------------------------------------------------------------
#
def get_active_texture_image_name(obj):
    mat = obj.active_material
    if mat is None or not mat.use_nodes or mat.node_tree is None:
        return ""
    node = mat.node_tree.nodes.active
    if node is None or node.type != 'TEX_IMAGE' or node.image is None:
        return ""
    return node.image.name


def get_assigned_textures(self, context):
    scn = context.scene
    all_tex = self.all_textures
    all_tex.clear()

    local_all_tex = []
    for obj in scn.objects:
        name = get_active_texture_image_name(obj)
        if name and name not in local_all_tex:
            item = all_tex.add()
            item.name = name
            local_all_tex.append(name)

    return local_all_tex


def update_textures(self, context):
    scn = context.scene
    self.tex_index = -1
    self.tex_objects.clear()
    tex_obj_list.clear()

    get_assigned_textures(self, context)

    if not self.texture:
        return

    for obj in scn.objects:
        if get_active_texture_image_name(obj) == self.texture:
            item = self.tex_objects.add()
            item.name = obj.name
            tex_obj_list.append(obj.name)


def update_tex_index(self, context):
    if len(self.tex_objects) < 1 or self.tex_index < 0:
        return
    try:
        ob_name = self.tex_objects[self.tex_index].name
    except IndexError:
        print("Texture Object Search: Bad objects list index")
        return

    ob = context.scene.objects.get(ob_name)
    if ob is not None:
        jump_to_object(context, ob)


class VIEW3D_OT_replace_all_textures(bpy.types.Operator):
    """Replace the searched texture image with the chosen replacement on all matched objects"""
    bl_idname = "replace_all.textures"
    bl_label = "Replace"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        props = context.window_manager.snr_properties

        if not props.texture or not props.tex_replace:
            return {'CANCELLED'}

        new_image = bpy.data.images.get(props.tex_replace)
        if new_image is None:
            return {'CANCELLED'}

        for obj in scn.objects:
            if obj.name not in tex_obj_list:
                continue
            mat = obj.active_material
            if mat is None or not mat.use_nodes or mat.node_tree is None:
                continue
            node = mat.node_tree.nodes.active
            if (node is not None and node.type == 'TEX_IMAGE'
                    and node.image is not None and node.image.name == props.texture):
                node.image = new_image

        return {'FINISHED'}


#
# ---------------------------------------------------------------------------
# Properties / registration
# ---------------------------------------------------------------------------
#
class SNR_Properties(bpy.types.PropertyGroup):
    select: BoolProperty(default=True, description="Deselect all other objects before jumping/replacing")
    copy_rotation: BoolProperty(default=True, description="Keep rotation and scale when replacing objects")

    srch_replace: StringProperty(description="Object that replaces the current selection")
    srch_objects: CollectionProperty(type=SNR_NameItem)
    srch_index: IntProperty(update=update_obj_search_index)

    material: StringProperty(update=update_material)
    mat_replace: StringProperty(description="Material that replaces the searched material")
    all_materials: CollectionProperty(type=SNR_NameItem)
    mat_objects: CollectionProperty(type=SNR_NameItem)
    mat_index: IntProperty(update=update_mat_index)

    texture: StringProperty(update=update_textures)
    tex_replace: StringProperty(description="Image that replaces the searched texture")
    all_textures: CollectionProperty(type=SNR_NameItem)
    tex_objects: CollectionProperty(type=SNR_NameItem)
    tex_index: IntProperty(update=update_tex_index)


classes = (
    SNR_NameItem,
    SNR_UL_name_list,
    SNR_Properties,
    VIEW3D_PT_search_and_replace,
    VIEW3D_OT_refresh,
    VIEW3D_OT_replace_selected_objects,
    VIEW3D_OT_replace_all_materials,
    VIEW3D_OT_random_materials,
    VIEW3D_OT_replace_all_textures,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.snr_properties = PointerProperty(type=SNR_Properties, options={'SKIP_SAVE'})


def unregister():
    del bpy.types.WindowManager.snr_properties
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
