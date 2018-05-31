# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Search&Replace",
    "author": "Eduard Fekete",
    "version": (1, 44),
    "blender": (2, 69, 0),
    "location": "View3D -> Tools -> Search&Replace",
    "description": "Allows the user to search objects by texture or material and also to replace textures/materials with others very quick. Visit my Wikipage for more informations",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Material_Search",
    "tracker_url": "http://developer.blender.org/T37651",
    "category": "3D View"
    }
    
import bpy
from bpy.props import *
import random

#
#   globals
#
obj_list = []
mat_obj_list = []
tex_obj_list = []

#
#   classes for the template lists
#
class ObjectSearchList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(icon="OBJECT_DATA", text=item.name)

class MaterialObjectSearchList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(icon="OBJECT_DATA", text=item.name)

class TextureObjectSearchList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(icon="OBJECT_DATA", text=item.name) 

class VIEW3D_PT_search_and_replace(bpy.types.Panel):
    bl_label = "Search&Replace"
    bl_category = "Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    @classmethod
    def poll(self, context):
        return context.mode == "OBJECT"
        
    def draw(self, context):
        layout = self.layout
        split = layout.split()
        col = split.column()
        
        #
        #   Options
        #
        wm = context.window_manager.MyProperties
        layout.label("Options:")
        row = layout.row(align=True)
        row.prop(wm, "select", text = "Always deselect")
        row.prop(wm, "copy_rotation", text = "Copy Rot&Scale")       
        
        #
        #   Object Search Menu
        #       
        layout.label(text='All Objects from {}'.format(context.scene.name))
        layout.operator(VIEW3D_OT_refresh.bl_idname, text="", icon="FILE_REFRESH")
        row = layout.row(align=True)
        row.operator('replace_selected.objects','Replace selection with :','Ersetzen',True)
        row.prop_search(wm, "srch_replace", bpy.data, "objects", text="")
        # Outputfield
        layout.template_list("ObjectSearchList", "",
                             wm, "srch_objects", 
                             wm, "srch_index")
        #
        #   Replace Material Menu
        #
        wm = context.window_manager.MyProperties
        row = layout.row(align=True)
        row.label(text="   Search Material")
        row.label(text="  New Material")
        
        row = layout.row(align=True)
        row.operator(VIEW3D_OT_refresh.bl_idname, text="", icon="FILE_REFRESH")
        row.prop_search(wm, "material", wm, "all_materials", text="")
        row.prop_search(wm, "mat_replace", bpy.data, "materials", text="")
        row.operator(VIEW3D_OT_refresh.bl_idname, text="", icon="FILE_REFRESH")
        
        row = layout.row(align=True)
        row.operator('replace_selected.materials','Replace selected','Alle Ersetzen',True)
        row.operator('replace_all.materials','Replace All','Ersetzen',True)
        row.operator('random.materials','Random','Set a Random Material',True)

        
        
        # Outputfield
        layout.template_list("MaterialObjectSearchList", "",
                             wm, "mat_objects", 
                             wm, "mat_index")   
                                
        #
        #   Replace Texture Menu
        #
        wm = context.window_manager.MyProperties
        
        row = layout.row(align=True)
        row.label(text="Search Texture:")
        row.label(text="New Texture:")
        
        row = layout.row(align=True)
        row.operator(VIEW3D_OT_refresh.bl_idname, text="", icon="FILE_REFRESH")
        row.prop_search(wm, "texture", wm, "all_textures", text="")
        row.prop_search(wm, "tex_replace", bpy.data, "textures", text="")
        row.operator(VIEW3D_OT_refresh.bl_idname, text="", icon="FILE_REFRESH")
        
        layout.operator('replace_all.textures','Replace All','Alle Ersetzen',True)

        # Outputfield
        layout.template_list("TextureObjectSearchList", "",
                             wm, "tex_objects", 
                             wm, "tex_index")

#
#   Refresh Button
#   
class VIEW3D_OT_refresh(bpy.types.Operator):
    """Refresh all"""
    bl_idname = "view3d.obj_search_refresh"
    bl_label = "Refresh objects list"
    
    def execute(self, context):
        update_objects(context.window_manager.MyProperties, context)
        update_material(context.window_manager.MyProperties, context)
        update_textures(context.window_manager.MyProperties, context)
        return {'FINISHED'}

#-----------------------------------------------------------------------------
#
#                               Replace Functions
#
#-----------------------------------------------------------------------------
#
#    Replace Selected Objects
#
class ReplaceSelectedObjects(bpy.types.Operator):
    """Replace all selected objects with the object"""\
    """which you choiced from the drop down menu at right"""
    
    bl_idname = "replace_selected.objects"
    bl_label = "Replace"

    def execute(self, context):
        
        scn = context.scene
        wm = context.window_manager.MyProperties
        
        selected_objects = []
        selected_objects = get_selected_objects(scn)
               
        i = 0
        replaced = 0
        
        try:
            for obj in scn.objects:
                              
                if wm.srch_replace != "" and wm.srch_replace != obj.name: #SC
                    
                    if obj.name in selected_objects:
                        
                                           
                    # set cursor to object
                        scn.cursor_location = obj.location.copy()
                            
                    #find and select the new object to make a copy of it
                        for ob in scn.objects:
                            
                            if ob.name == wm.srch_replace:

                                deselect_all_objects(scn)       
                                ob.select = True
                                scn.objects.active = ob
                                
                                #Save old values to restore them later
                                try:
                                    if ob.rotation_mode == "QUATERNION":
                                        old_rm = ob.rotation_mode
                                        old_rw = ob.rotation_quaternion.w
                                        old_rx = ob.rotation_quaternion.x
                                        old_ry = ob.rotation_quaternion.y
                                        old_rz = ob.rotation_quaternion.z
                                    elif ob.rotation_mode == "AXIS_ANGLE":
                                        old_rm = ob.rotation_mode
                                        old_rw = ob.rotation_axis_angle[0]
                                        old_rx = ob.rotation_axis_angle[1]
                                        old_ry = ob.rotation_axis_angle[2]
                                        old_rz = ob.rotation_axis_angle[3]
                                    else:
                                        old_rm = ob.rotation_mode
                                        old_rx = ob.rotation_euler.x
                                        old_ry = ob.rotation_euler.y
                                        old_rz = ob.rotation_euler.z
                                                        
                                    #Save current scale values
                                    old_sx = ob.scale.x
                                    old_sy = ob.scale.y
                                    old_sz = ob.scale.z
                                except:
                                    print("ERROR #3")
                                
                                if wm.copy_rotation:                              
                                    try:
                                    #extract datasets
                                        x = i*9
                                        name = selected_objects[0+x]
                                        rw = selected_objects[1+x]
                                        rx = selected_objects[2+x]
                                        ry = selected_objects[3+x]
                                        rz = selected_objects[4+x]
                                        sx = selected_objects[5+x]
                                        sy = selected_objects[6+x]
                                        sz = selected_objects[7+x]
                                        rmode = selected_objects[8+x]
                                    except:
                                        print("ERROR #2")
      
                                    try:    
                                    #set new rotation values. Take values from the object which will be replaced.
                                        if rmode == "QUATERNION":
                                            ob.rotation_mode = rmode
                                            ob.rotation_quaternion.w = rw
                                            ob.rotation_quaternion.x = rx
                                            ob.rotation_quaternion.y = ry
                                            ob.rotation_quaternion.z = rz
                                                
                                        elif rmode == "AXIS_ANGLE":
                                            ob.rotation_mode = rmode
                                            ob.rotation_axis_angle[0] = rw
                                            ob.rotation_axis_angle[1] = rx
                                            ob.rotation_axis_angle[2] = ry
                                            ob.rotation_axis_angle[3] = rz
                                        else:
                                            ob.rotation_mode = rmode
                                            ob.rotation_euler.x = rx
                                            ob.rotation_euler.y = ry
                                            ob.rotation_euler.z = rz
                                                
                                    #set new scale values. Take values from the object which will be replaced.
                                        ob.scale.x = sx
                                        ob.scale.y = sy
                                        ob.scale.z = sz
                                    except:
                                        print("ERROR #4")
                                    
                                    #create a copy from the new object        
                                    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
                                    replaced = 1
                                     
                                    try:   
                                        if wm.copy_rotation:     #If checkbox "Copy Rot&Scale" is selected
                                        
                                        #restore old rotation values
                                            if old_rm == "QUATERNION":
                                                ob.rotation_mode = old_rm
                                                ob.rotation_quaternion.w = old_rw
                                                ob.rotation_quaternion.x = old_rx
                                                ob.rotation_quaternion.y = old_ry
                                                ob.rotation_quaternion.z = old_rz
                                                    
                                            elif old_rm == "AXIS_ANGLE":
                                                ob.rotation_axis_angle[0] = old_rw
                                                ob.rotation_axis_angle[1] = old_rx
                                                ob.rotation_axis_angle[2] = old_ry
                                                ob.rotation_axis_angle[3] = old_rz
                                            else:
                                                #ob.rotation_mode = old_rm
                                                ob.rotation_euler.x = old_rx
                                                ob.rotation_euler.y = old_ry
                                                ob.rotation_euler.z = old_rz
                                                
                                        #restore old scale values    
                                            ob.scale.x = old_sx
                                            ob.scale.y = old_sy
                                            ob.scale.z = old_sz
                                    except:
                                        print("Error #5")
                                        
                                    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
                                    i = i+1                                              

                                else:
                                    ob.rotation_mode = "XYZ"
                                    ob.rotation_euler.x = 0
                                    ob.rotation_euler.y = 0
                                    ob.rotation_euler.z = 0

                                    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
                                    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
                                    replaced = 1
                                                                    
                                 #restore old rotation values
                                    if old_rm == "QUATERNION":
                                        ob.rotation_mode = old_rm
                                        ob.rotation_quaternion.w = old_rw
                                        ob.rotation_quaternion.x = old_rx
                                        ob.rotation_quaternion.y = old_ry
                                        ob.rotation_quaternion.z = old_rz
                                            
                                    elif old_rm == "AXIS_ANGLE":
                                        ob.rotation_axis_angle[0] = old_rw
                                        ob.rotation_axis_angle[1] = old_rx
                                        ob.rotation_axis_angle[2] = old_ry
                                        ob.rotation_axis_angle[3] = old_rz
                                    else:
                                        ob.rotation_mode = old_rm
                                        ob.rotation_euler.x = old_rx
                                        ob.rotation_euler.y = old_ry
                                        ob.rotation_euler.z = old_rz
        except:             
            print("ERROR #1")
            
    #delete replaced objects
        if replaced == 1:
            for obj in scn.objects:
                if wm.srch_replace != "" and wm.srch_replace != obj.name:
                    if obj.name in selected_objects:
                        deselect_all_objects(scn)
                        obj.select = True
                        scn.objects.active = obj
                        bpy.ops.object.delete(use_global=False)
                    
        return{'FINISHED'}
             
#
#   Replace All Textures
#
class ReplaceAll_Texture(bpy.types.Operator):
    """Replace all textures with the texture choiced"""\
    """ from the drop down menu on 'New Texture'"""
    
    bl_idname = "replace_all.textures"
    bl_label = "Replace"

    def execute(self, context):
    
        scn = context.scene
        
        wm = context.window_manager.MyProperties    # now i can access all my defined properties with the var "wm"
        max = len(bpy.data.materials)
        m = len(bpy.data.textures)
        
        for obj in scn.objects:
            if obj.name in tex_obj_list:
                    
                for i in range(max):
                    if obj.active_material is not None: 
                        obj.select = True
                        scn.objects.active = obj
                        obj.active_material_index = i
            
                    for x in range(m):
                        if obj.active_material is not None: 
                            
                            obj.active_material.active_texture_index = x                       
                            ActiveTexture = get_active_texture(obj)
                                
                            if ActiveTexture is not None:
                                if ActiveTexture == wm.texture:
                                    if ActiveTexture != wm.tex_replace:
                                        if wm.texture is not None:
                                            if wm.tex_replace is not None:
                                               obj.active_material.active_texture = bpy.data.textures[wm.tex_replace]
        
        # set active texture index of every material from all objects in scene to zero
        for i in range(max):
            for obj in scn.objects:
                obj.active_material_index = i
                if obj.active_material is not None:
                    obj.active_material.active_texture_index = 0
                    
        # set active material index of all objects to zero
        for obj in scn.objects:
            obj.active_material_index = 0

        return{'FINISHED'}
    
#
#    Replace All Materials
#
class ReplaceAllMaterials(bpy.types.Operator):
    """Refresh all materials with the material choiced"""\
    """ from the drop down menu 'New Material'"""
    
    bl_idname = "replace_all.materials"
    bl_label = "Replace"

    def execute(self, context):
    
        scn = context.scene
        wm = context.window_manager.MyProperties
        max = len(bpy.data.materials)
        
        for obj in scn.objects:
            if obj.name in mat_obj_list:
                    
                for i in range(max):                    
                    obj.select = True
                    scn.objects.active = obj
                    obj.active_material_index = i
                    
                    #get active material
                    ActiveMaterial = str(obj.material_slots.data.active_material)[23:-3]
                    
                    if ActiveMaterial != "":
                        if wm.material != "":
                            if wm.mat_replace != "":
                                if ActiveMaterial == wm.material:
                                    if ActiveMaterial != wm.mat_replace:
                                        obj.active_material = bpy.data.materials[wm.mat_replace]
                                        
        for obj in scn.objects:
            obj.active_material_index = 0

        return{'FINISHED'}
    
#
#    Replace Material from selected object/s
#
class ReplaceSelectedMaterial(bpy.types.Operator):
    """Replace materials from all selected objects with """\
    """the material choiced from the drop down menu 'New Material'"""
    
    bl_idname = "replace_selected.materials"
    bl_label = "Replace"

    def execute(self, context):
    
        scn = context.scene
        obj = scn.objects.active
        wm = context.window_manager.MyProperties
        max = len(bpy.data.materials)
        
        for obj in scn.objects:
            if obj.select == True:
                for i in range(max):                    
                    
                    if wm.material == "":
                        if wm.mat_replace != "":
                            if obj.active_material_index == 0:
                                obj.active_material = bpy.data.materials[wm.mat_replace]    
                                                    
                    obj.active_material_index = i
                    ActiveMaterial = str(obj.material_slots.data.active_material)[23:-3]
                            
                    if ActiveMaterial != "":
                        if wm.material != "":
                            if wm.mat_replace != "":
                                if ActiveMaterial == wm.material:
                                    if ActiveMaterial != wm.mat_replace:
                                        obj.active_material = bpy.data.materials[wm.mat_replace]
                                        obj.active_material_index = 0

        return{'FINISHED'}

#
#    Select Random Materials
#
class SelectRandomMaterials(bpy.types.Operator):
    """ Initialise objects with random materials """
    
    bl_idname = "random.materials"
    bl_label = "Replace"

    def execute(self, context):
           
        scn = context.scene
        obj = scn.objects.active
        wm = context.window_manager.MyProperties
        max = len(bpy.data.materials)
        
        for obj in scn.objects:
            if obj.select == True:
                for i in range(max):                    
                    
                    random_nr = zahl = random.randint(0,max-1)
                    
                    if len(obj.material_slots) > i:     # verhindert das Material Slots erstellt werden die nicht benötigt werden
                        obj.active_material_index = i
                    
                    if str(bpy.data.materials[random_nr])[23:-3] != "Material":
                        obj.active_material = bpy.data.materials[random_nr]
                    
                    ActiveMaterial = str(obj.material_slots.data.active_material)[23:-3]

        return{'FINISHED'}

#-----------------------------------------------------------------------------
#
#                               Jump To Object Functions
#
#-----------------------------------------------------------------------------
#
#   [Object-Menu] select the object and focus the view on it
#
def jump_to_object(scene, ob):
    
    try:
        wm = bpy.context.window_manager.MyProperties
        if wm.select == True:     
            deselect_all_objects(scene)
                
        ob.select = True
        scene.objects.active = ob
        return bpy.ops.view3d.view_selected('EXEC_REGION_WIN') == {'FINISHED'}
    except:
        return False 

#
#   [Material-Menu] select the object and focus the view on it
#  
def jump_to_mat_object(scene, ob):
    try:     
        wm = bpy.context.window_manager.MyProperties
        if wm.select == True:     
            deselect_all_objects(scene)
            
        ob.select = True
        scene.objects.active = ob
        return bpy.ops.view3d.view_selected('EXEC_REGION_WIN') == {'FINISHED'}
    except:
        return False      
    
#
#   [Texture-Menu] select the object and focus the view on it
#
def jump_to_tex_object(scene, ob):
    try:
        wm = bpy.context.window_manager.MyProperties
        if wm.select == True:     
            deselect_all_objects(scene)
            
        ob.select = True
        scene.objects.active = ob
        return bpy.ops.view3d.view_selected('EXEC_REGION_WIN') == {'FINISHED'}
    except:
        return False
    
#-----------------------------------------------------------------------------
#
#                               Update Functions
#
#-----------------------------------------------------------------------------
#
#   Update Objects - gets called when a refresh button or the list was clicked 
#
def update_objects(self, context):
    
    self.srch_index = -1
    self.srch_objects.clear()
        
    for ob in context.scene.objects:
        obj_list.append(ob.name)
        item = self.srch_objects.add()
        item.name = ob.name
        
#
#   Update Materials - gets called when a refresh button or the list was clicked 
#
def update_material(self, context):
    
    scn = bpy.context.scene
    self.mat_index = -1
    self.mat_objects.clear()
    mat_obj_list.clear()

    get_assigned_materials(self, context)
    
    max = len(bpy.data.materials)
    for i in range(max):
        for obj in scn.objects:
            
            obj.active_material_index = i
            active_material = get_active_material(obj)
            
            if self.material == active_material and self.material != "":
                if mat_obj_list:
                    for a in mat_obj_list:
                        if obj.name not in mat_obj_list:
                            item = self.mat_objects.add()
                            item.name = obj.name
                            mat_obj_list.append(obj.name)
                else:
                    item = self.mat_objects.add()
                    item.name = obj.name
                    mat_obj_list.append(obj.name)
                
    for obj in scn.objects:
        obj.active_material_index = 0

#
#   Update Textures - get called when a refresh button or the list was clicked 
#
def update_textures(self, context):
    
    scn = bpy.context.scene
    self.tex_index = -1
    self.tex_objects.clear()
    tex_obj_list.clear()
    
    get_assigned_textures(self, context)
    
    max = len(bpy.data.materials)
    m = len(bpy.data.textures)
    
    for i in range(max):
        #for each material slot and for each object in scene
        for obj in scn.objects:     
            obj.active_material_index = i
            
            for x in range(m):
                if obj.active_material is not None: 
                    obj.active_material.active_texture_index = x
                    if obj.active_material.active_texture != "None":
            
                        active_texture = get_active_texture(obj)
                                           
                        if self.texture == active_texture and active_texture != "":
                            if tex_obj_list:
                                for a in tex_obj_list:
                                    if obj.name not in tex_obj_list:
                                        item = self.tex_objects.add()
                                        item.name = obj.name
                                        tex_obj_list.append(obj.name)
                            else:
                                item = self.tex_objects.add()
                                item.name = obj.name
                                tex_obj_list.append(obj.name)
                            
    for i in range(max):
        for obj in scn.objects:
            obj.active_material_index = i
            if obj.active_material is not None:
                obj.active_material.active_texture_index  = 0
        
    for obj in scn.objects:
        obj.active_material_index = 0
        
#
#   index update function for the texture outputfield
#  
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
        jump_to_tex_object(context.scene, ob)    
        
#
#   index update function for the material outputfield
#      
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
        jump_to_mat_object(context.scene, ob)
        
#
#   index update function for the object search outputfield
#           
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
        jump_to_object(context.scene, ob)    

#-----------------------------------------------------------------------------
#
#                               Get-Methods
#
#-----------------------------------------------------------------------------

#get all materials with users
def get_assigned_materials(self, context):
    
    scn = context.scene
    allm = self.all_materials
    local_all_mat = []
    
    allm.clear()
    local_all_mat.clear()
    
    max = len(bpy.data.materials)
    for i in range(max):
        for obj in scn.objects:
            
            obj.active_material_index = i
            active_material = get_active_material(obj)

            if ((active_material != "") and (active_material not in local_all_mat) and (active_material in bpy.data.materials)):
                item = allm.add()
                item.name = active_material
                local_all_mat.append(active_material)
          
    for obj in scn.objects:
        obj.active_material_index = 0
                    
    return local_all_mat  

#       
#   Get all textures with users so that we can put them into the dropdown list
#
def get_assigned_textures(self, context):
    
    scn = context.scene
    
    wm_alltex = self.all_textures
    wm_alltex.clear()
    
    all_twu = []    #all_twu = all_textures_with_users
    all_twu.clear()
    
    max = len(bpy.data.materials)
    m = len(bpy.data.textures)
    
    for i in range(max):
        for obj in scn.objects:
            if obj.active_material is not None:
                obj.active_material_index = i
                
                for x in range(m):
                    if obj.active_material is not None:   
                        obj.active_material.active_texture_index = x
                        if obj.active_material.active_texture:
                            if obj.active_material.active_texture.type is not None:
                                
                                active_texture = get_active_texture(obj)

                                if ((active_texture != "") and (active_texture not in all_twu)):
                                    item = wm_alltex.add()
                                    item.name = active_texture
                                    all_twu.append(active_texture)
   
    for obj in scn.objects:
        if obj.active_material is not None: 
            obj.active_material_index = 0
            obj.active_material.active_texture_index = 0

    return all_twu

def get_active_material(obj):
    
    active = obj.active_material
    
    if active is not None:
        Material = active.name
    else:
         Material = ""
         
    return Material


def get_active_texture(obj):

    tex = obj.material_slots.data.active_material.active_texture
    
    if tex is not None:
        active_texture = tex.name
    else:
        active_texture = ""
        
    return active_texture


def get_selected_objects(scn):
    
    list=[]
    
    for obj in scn.objects:
        if obj.select == True:
            
            list.append(obj.name)          
            rmode = obj.rotation_mode

            if rmode == "QUATERNION":
                list.append(obj.rotation_quaternion.w)
                list.append(obj.rotation_quaternion.x)
                list.append(obj.rotation_quaternion.y)
                list.append(obj.rotation_quaternion.z)
            elif rmode == "AXIS_ANGLE":
                list.append(obj.rotation_axis_angle[0])
                list.append(obj.rotation_axis_angle[1])
                list.append(obj.rotation_axis_angle[2])
                list.append(obj.rotation_axis_angle[3])
            else:
                list.append(0.0)
                list.append(obj.rotation_euler.x)
                list.append(obj.rotation_euler.y)
                list.append(obj.rotation_euler.z)
                
            list.append(obj.scale.x)
            list.append(obj.scale.y)
            list.append(obj.scale.z)
            
            list.append(rmode)
                            
    return list

#-----------------------------------------------------------------------------
#
#                               Other Functions
#
#-----------------------------------------------------------------------------

def deselect_all_objects(scn):
    for obj in scn.objects:
        obj.select = False

#-----------------------------------------------------------------------------
#
#                               Properties
#
#-----------------------------------------------------------------------------

class MyProperties(bpy.types.PropertyGroup):
    select = BoolProperty(default=True)
    copy_rotation = BoolProperty(default=True)
    
    object = StringProperty(update=update_objects)
    srch_replace = StringProperty()
    srch_all_objects = CollectionProperty(type=bpy.types.PropertyGroup)
    srch_objects = CollectionProperty(type=bpy.types.PropertyGroup)
    srch_index = IntProperty(update=update_obj_search_index)
    
    material = StringProperty(update=update_material)
    mat_replace = StringProperty()
    all_materials = CollectionProperty(type=bpy.types.PropertyGroup)
    mat_objects = CollectionProperty(type=bpy.types.PropertyGroup)
    mat_index = IntProperty(update=update_mat_index)
    
    texture = StringProperty(update=update_textures)
    tex_replace = StringProperty()
    all_textures = CollectionProperty(type=bpy.types.PropertyGroup)
    tex_objects = CollectionProperty(type=bpy.types.PropertyGroup)
    tex_index = IntProperty(update=update_tex_index)
    
#-----------------------------------------------------------------------------
#                                                                             
#                             Register / Unregister                         
#                                                                             
#-----------------------------------------------------------------------------
def register():
    bpy.utils.register_module(__name__)
    bpy.types.WindowManager.MyProperties = PointerProperty(type=MyProperties, options={'SKIP_SAVE'})
    
def unregister():
    del bpy.types.WindowManager.MyProperties
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
