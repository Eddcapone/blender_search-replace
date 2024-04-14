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
    "name": "Search & Replace",
    "author": "Eduard Fekete",
    "version": (2.0),
    "blender": (4, 0, 2),
    "location": "3D Viewport -> Tools (Right Menu) -> Search & Replace",
    "description": "Provides functionality to search and replace objects. It also comes with a 'jump to object' feature, that centers the view to an object if you click on it in the list.",
    "wiki_url": "https://github.com/Eddcapone/blender_search-replace/wiki",
    "category": "3D View"
}

import bpy
from bpy.props import (
    BoolProperty,
    CollectionProperty,
    PointerProperty,
    StringProperty,
    IntProperty,
)

#
# globals
#
obj_list = []

#
# classes for the template lists
#
class OBJECT_UL_object_search_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.label(icon="OBJECT_DATA", text=item.name)


class VIEW3D_PT_search_and_replace(bpy.types.Panel):
    bl_label = "Search&Replace"
    bl_category = "Tool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def draw(self, context):
        layout = self.layout

        # Options
        scene = context.scene
        properties = scene.my_tool
        layout.label(text="Options:")
        row = layout.row(align=True)
        row.prop(properties, "keep_rotation", text="Keep Rotation & Scale")

        # Object Search Menu
        layout.label(text='All Objects from {}'.format(scene.name))
        layout.operator("view3d.obj_search_refresh", text="Refresh")
        row = layout.row(align=True)
        row.operator('replace_selected.objects', text='Replace selection with :', icon='FILE_REFRESH', emboss=True)
        row.prop_search(properties, "srch_replace", bpy.data, "objects", text="")
        # Outputfield
        layout.template_list("OBJECT_UL_object_search_list", "", properties, "srch_objects", properties, "srch_index")


#
# Refresh Button
#
class VIEW3D_OT_refresh(bpy.types.Operator):
    """Refresh all"""
    bl_idname = "view3d.obj_search_refresh"
    bl_label = "Refresh objects list"

    def execute(self, context):    
        refresh()
        return {'FINISHED'}

#
# Update Objects - gets called when a refresh button or the list was clicked
#
def refresh():
    
    myTool = bpy.context.scene.my_tool
    
    # Clear existing items
    myTool.srch_objects.clear()

    # Add new items to the collection
    for ob in bpy.context.scene.objects:
        item = myTool.srch_objects.add()
        item.name = ob.name
        item.obj = ob

    deleteGarbage()


def deleteGarbage():
    dataObjectsList=[]
    sceneObjectsList=[]
    deleteList=[]
    
    for data_object in bpy.data.objects:
        dataObjectsList.append(data_object)

    for scene_object in bpy.context.scene.objects:
        sceneObjectsList.append(scene_object)
        
    for obj in dataObjectsList:
        if obj not in sceneObjectsList:
            deleteList.append(obj)
            
    with bpy.context.temp_override(selected_objects=deleteList):
        bpy.ops.object.delete()

#
# Replace Selected Objects
#
class ReplaceSelectedObjects(bpy.types.Operator):
    """Replace all selected objects with the object"""\
    """that was choosen from the search menu"""
    
    bl_idname = "replace_selected.objects"
    bl_label = "Replace"

    def execute(self, context):
        
        scene = context.scene
        myTool = scene.my_tool
        
        if myTool.srch_replace == "":
            return{'CANCELLED'}

        selected_objects = []
        selected_objects = get_selected_objects(scene)

        i = 0
        replaced = 0
        oldCursorLocation = scene.cursor.location.copy()

        try:
            # Run throug all scene objects
            for _obj in scene.objects:

                if (
                     _obj.name in selected_objects 
                     and myTool.srch_replace != _obj.name
                ):
                    # set cursor to object
                    scene.cursor.location = _obj.location.copy()

                    # Store the replace object (object that will replace the selected objects)
                    replaceObj = bpy.context.scene.objects[myTool.srch_replace]

                    # Select the object that will replace the currently selected object.
                    deselect_all_objects(scene)
                    replaceObj.select_set(True)
                    bpy.context.view_layer.objects.active = replaceObj

                    # save old values to restore them later
                    replaceObjProps = RotationScaleProperties(replaceObj)

                    if myTool.keep_rotation:                              

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

                        # set new rotation values. 
                        # Take values from the object which will be replaced.
                        self.setRotation(replaceObj, rw, rx, ry, rz, rmode)

                        # set new scale values.
                        # Take values from the object which will be replaced.
                        replaceObj.scale.x = sx
                        replaceObj.scale.y = sy
                        replaceObj.scale.z = sz
                        
                        # create a copy from the active object 
                        self.duplicateObj()
                        replaced = 1

                        if myTool.keep_rotation:     # if checkbox "Keep Rotation & Scale" is checked
                            self.restoreRotationAndScale(replaceObj, replaceObjProps)

                        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
                        i = i+1
                    else:
                        replaceObj.rotation_mode = "XYZ"
                        replaceObj.rotation_euler.x = 0
                        replaceObj.rotation_euler.y = 0
                        replaceObj.rotation_euler.z = 0

                        self.duplicateObj()

                        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
                        replaced = 1
                        self.restoreRotationAndScale(replaceObj, replaceObjProps)


        except Exception as e:
            print(f"Error #5 in ReplaceSelectedObjects: {e}")
            scene.cursor.location = oldCursorLocation
            
        #delete replaced objects
        if replaced == 1:
            for obj in scene.objects:
                if myTool.srch_replace != "" and myTool.srch_replace != obj.name:
                    if obj.name in selected_objects:
                        deselect_all_objects(scene)
                        obj.select_set(True)
                        bpy.context.view_layer.objects.active = obj
                        bpy.ops.object.delete(use_global=False)
                        
        # trigger refresh
        refresh()
                        
        # reset cursor
        scene.cursor.location = oldCursorLocation
        return{'FINISHED'}


    #
    # restore old rotation and scale values
    #
    def restoreRotationAndScale(self, obj, properties):
        
        # restore old rotation values
        if properties.old_rotation_mode == "QUATERNION":
            obj.rotation_mode = properties.old_rotation_mode
            obj.rotation_quaternion.w = properties.old_rw
            obj.rotation_quaternion.x = properties.old_rx
            obj.rotation_quaternion.y = properties.old_ry
            obj.rotation_quaternion.z = properties.old_rz
                
        elif properties.old_rotation_mode == "AXIS_ANGLE":
            obj.rotation_axis_angle[0] = properties.old_rw
            obj.rotation_axis_angle[1] = properties.old_rx
            obj.rotation_axis_angle[2] = properties.old_ry
            obj.rotation_axis_angle[3] = properties.old_rz
        else:
            obj.rotation_mode = properties.old_rotation_mode
            obj.rotation_euler.x = properties.old_rx
            obj.rotation_euler.y = properties.old_ry
            obj.rotation_euler.z = properties.old_rz

        # restore old scale values    
        obj.scale.x = properties.old_sx
        obj.scale.y = properties.old_sy
        obj.scale.z = properties.old_sz


    def setRotation(self, ob, rw, rx, ry, rz, rmode):
        if rmode == "QUATERNION":
            ob.rotation_mode = rmode
            ob.rotation_quaternion = (rw, rx, ry, rz)
        elif rmode == "AXIS_ANGLE":
            ob.rotation_mode = rmode
            ob.rotation_axis_angle = (rw, rx, ry, rz)
        else:
            ob.rotation_mode = rmode
            ob.rotation_euler = (rx, ry, rz)
            
    def duplicateObj(self):
        bpy.ops.object.duplicate_move(
            OBJECT_OT_duplicate={
                "linked":False,
                "mode":'TRANSLATION'
            },
            TRANSFORM_OT_translate={
                "value":(0, 0, 0),
                "constraint_axis":(False, False, False),
                "mirror":False,
                "proportional_edit_falloff":'SMOOTH',
                "proportional_size":1,
                "snap":False,
                "snap_target":'CLOSEST',
                "snap_point":(0, 0, 0),
                "snap_align":False,
                "snap_normal":(0, 0, 0),
                "texture_space":False,
                "remove_on_cancel":False,
                "release_confirm":False
            }
        )



class RotationScaleProperties:
    """ToDo"""\
    """XXX"""
    
    bl_idname = "rotation_scale_properties"
    bl_label = "Rotation Scale Properties"
    bl_rna = ""
    
    def __init__(self, obj):
        self.obj_name = obj.name
        self.old_rotation_mode = obj.rotation_mode
        
        if obj.rotation_mode == "QUATERNION":
            self.old_rw = obj.rotation_quaternion.w
            self.old_rx = obj.rotation_quaternion.x
            self.old_ry = obj.rotation_quaternion.y
            self.old_rz = obj.rotation_quaternion.z
        elif obj.rotation_mode == "AXIS_ANGLE":
            self.old_rw = obj.rotation_axis_angle[0]
            self.old_rx = obj.rotation_axis_angle[1]
            self.old_ry = obj.rotation_axis_angle[2]
            self.old_rz = obj.rotation_axis_angle[3]
        else:
            self.old_rw = 0
            self.old_rx = obj.rotation_euler.x
            self.old_ry = obj.rotation_euler.y
            self.old_rz = obj.rotation_euler.z

        self.old_sx = obj.scale.x
        self.old_sy = obj.scale.y
        self.old_sz = obj.scale.z


def get_selected_objects(scene):
    
    list=[]
    
    for obj in scene.objects:
        if obj.select_get() == True:
            
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

#
# index update function for the object search outputfield
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


#
# Other Functions
#

def jump_to_object(scene, ob):
    try:
        areas  = [area for area in bpy.context.window.screen.areas if area.type == 'VIEW_3D']

        with bpy.context.temp_override(
            window=bpy.context.window,
            area=areas[0],
            region=[region for region in areas[0].regions if region.type == 'WINDOW'][0],
            screen=bpy.context.window.screen
        ):
            deselect_all_objects(scene)
            ob.select_set(True)
            bpy.ops.view3d.view_selected()
            
            refresh()
    except Exception as e:
        print(f"Error in jump_to_object: {e}")
        return False



def deselect_all_objects(scene):
    for obj in scene.objects:
        obj.select_set(False)

#
# Properties
#
class ObjectItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    obj: bpy.props.PointerProperty(type=bpy.types.Object)

class MyProperties(bpy.types.PropertyGroup):
    select: bpy.props.BoolProperty(default=True)
    keep_rotation: bpy.props.BoolProperty(default=True, description="Keep original rotation and scale of the selected objects")
    object: bpy.props.StringProperty()
    srch_replace: bpy.props.StringProperty(description="Select the replacement object")
    srch_objects: bpy.props.CollectionProperty(type=ObjectItem)
    srch_index: bpy.props.IntProperty(update=update_obj_search_index)

classes = [
    ObjectItem,
    OBJECT_UL_object_search_list,
    VIEW3D_PT_search_and_replace,
    VIEW3D_OT_refresh,
    ReplaceSelectedObjects,
    MyProperties,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # Register MyProperties
    bpy.types.WindowManager.my_tool = bpy.props.PointerProperty(type=MyProperties)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    # Unregister MyProperties
    del bpy.types.Scene.my_tool
    del bpy.types.WindowManager.my_tool


if __name__ == "__main__":
    register()