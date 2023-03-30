# blender_search-replace
This Add-On provides a simple search/replace menu for use in the 3D view tools sidebar (under the register "Tools"). Allows users to search for all objects from the scene and replace them or filter them by material/texture and also to replace the material/texture very fast.

## Installation

<!-- TODO add download link -->
- Download the script then copy it into your `\\.blender\scripts\addons` folder.
- Open Blender and go to the addons tab in User Preferences.
- Enable the script

- [archived blender wiki entry](https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Material_Search)

## Documentation

- Add On Installation Video
[![Watch the video](https://img.youtube.com/vi/A-4-8h2WEMk/maxresdefault.jpg)](https://youtu.be/A-4-8h2WEMk)

### Description

The searchresult will be written into a interactive output field where users can select the found objects. Selecting an object from the output field will also select the object in the scene, set it to the active object and focus the view on it.

### Functions
- search material menu
- Search for objects/materials or textures and replace them very fast.
- Assign a material to all selected objects.
- Find out where all objects with the material/texture you've searched are located, or search for all objects in scene.
- Replace materials of all selected objects with a random material.

### Instructions
Open the tools sidebar in 3D-View and search for the panel named "Search&Replace".

Object: Press on the refresh button. All objects from scene (including lamps, cameras, fields etc) will apear in the list below where you can choice them to select and focus the view on them.

Material/Texture: Either choose a material/texture from the list or type in the name of the material/texture you want to search, manually.

The result (all objects with the searched material/texture assigned) will be send into the list below the button. Then you are able to select the found objects from the list.

### Replace Function
Object: At first select all objects you want to replace, from the scene, then choice the new object from the drop down menu right beside the replace button, then press on the replace button.

Texture/Material: Put the material/texture you want to replace on the left and the new material/texture to the right, then press the "Replace All" button if you like to replace all or if you like to replace just the materials of the selected objects, then press the "Replace selected" button.

### Options
Copy Rot&Scale: If the control box of "Copy Rot&Scale" is set, then replaced objects will keep their old rotation and scale. Works with euler, quaternion and axis-angle.

Always Deselect: Deselect all objects before selecting an object from the list, if this option is set. Otherwise every object which you select from the list will be added to the selection, this allows to select multiple objects from the list.

Replace Objects Demonstration: (click here if the video controls do not embed, for you.)

- Replace Objects Demonstration Video
[![Watch the video](https://img.youtube.com/vi/GF-9bIw-EG4/maxresdefault.jpg)](https://youtu.be/GF-9bIw-EG4)

### Assign Functions
Assing Materials: If you select on ore more objects and don't select a search material, then you are able to assing the material which you selected on "replace material" to the objects.


- Assing Materials demonstration Video
[![Watch the video](https://img.youtube.com/vi/PqaX9SbwC5c/maxresdefault.jpg)](https://youtu.be/PqaX9SbwC5c)

### Info
- You have to press one of the refresh buttons everytime you add/remove/assign/de-assign a material/texture/object to update the list. It's not important which refresh button you press, since all refresh buttons are pointing at the same refresh method.
- You don't have to press a "start search" button or similar, just put the searched material/texture in and the search will start automatically.

#### Assign Random Materials: 
Select one or more objects and press on the "Random" button, this will replace the objects material with random materials.

HowTo:
1. Make sure that you already created some materials, because the materials which you created will be taken to initialise the objects.
2. Now just select all the objects you want to change, and press the "Random" Button

- Assing Random Materials demonstration Video
[![Watch the video](https://img.youtube.com/vi/IORkjg7l_E8/maxresdefault.jpg)](https://youtu.be/IORkjg7l_E8)

### Advice
If you are just interested in the object replace function and don't need the material / texture replacement, then click here to download only this function.

- Menu: Search-Objects demonstration Video
[![Watch the video](https://img.youtube.com/vi/Atcw-pv1g1M/maxresdefault.jpg)](https://youtu.be/Atcw-pv1g1M)

### Changelog
- v1.44 Eduardf
    - The Search & Replace Menu will now only appear under the Tools section
- v1.44 Eduardf
    - Added the function "Replace with Random Material"
- v1.43 Eduardf
    - Added a new function which allows to assign materials directly
- v1.42.2 - Eduardf 14:19, 15 December 2013 (CET)
    - The Panel will now only be visible in object mode
- v1.42.1 - Eduardf 17:39, 1 December 2013 (CET)
    - Added a function for object replacement
    - Fixed a bug at texture replacement.
- v1.42 - Eduardf 22:22, 8 December 2013 (CET)
    - I added two control boxes for more functions (Downloadlink on top of this page)
- v1.4 - Eduardf Download v1.4
    - I've added a new feature to let users search for all objects in the scene (including cameras, lamps, curves, emptys, fields etc.) and select and focus to them.
    - I've add some labels to make the Add-On easier to understand
    - All refresh buttons point at the same method now.
    - The material menu has now a new button which allows to replace only the materials from the selected objects.
- v1.3 - Download v1.3 Eduardf
    - I've added a texture replace function
- v1.2 - Download v1.2 Eduardf
    - I've added a material replace function.
- v1.11 - Download v1.11 Eduardf
    - The Drop Down List does not contain materials without users anymore.
    - Problem: Users has to press the Refresh Button to update the material list.
- v1.1 - Download v1.1 Eduardf + CoDEmanX (created the DropDown List)
    - Contains a drop down list which is also searchable manually. Problem: List will also show Materials with no users.
- v1.0 - Download v1.0 Eduardf + beta-tester (helped me to produce the UI)
    - Manuall input only.
    
### To-do list
| | |
|--|--|
|done | Let replaced objects keep the old rotation & scale as the old object.|
|done | Add a random material function.|
|done | Add a object replacement function.|
|done | Merge this Add-On and my other Add-On ("GoTo Object").|
|done | Add a feature to search&replace textures.|
|done | Add a feature to replace materials.|
|done | Add a button to replace only selected objects.|
|done | Only search for materials/textures with assigned users.|
|done | Replace the manuall input with a drop down list.|
|in progress 50% | Add a Function to replace only the material/texture of the filtered objects.|
|in progress 0% | Let the search material/texture list update automatically. (not possible due to blender)|

### Support
e-mail: eduard_fekete@yahoo.de
(believe support is not given anymore since plugin development is put on hold.)

### Credits
- Eduard Fekete: original author
- CoDEmanX - Thank you for your tips and for teaching me how to create a drop down list!
- beta-tester - Thank you for your start help in the forum to create the user interface!
- Hannes D: Ported all docs to README
