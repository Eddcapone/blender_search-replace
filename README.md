# blender_search-replace
This Add-On provides a simple search/replace menu for use in the 3D view tools sidebar (under the register "Tools"). Allows users to search for all objects from the scene and replace them or filter them by material/texture and also to replace the material/texture very fast.
<div id="content">
				<a name="top" id="top"></a>
								<div id="bodyContent">
					<h3 id="siteSub">From BlenderWiki</h3>
					
															<div id="jump-to-nav">Jump to: <a href="#column-one">navigation</a>, <a href="#searchInput">search</a></div>					
					<!-- START content -->
					<table class="prettytable" width="100%" style="">
<caption><span style="color: orange;"><b>Search&amp;Replace</b></span><br><i>Search&amp;Replace</i>
</caption><tbody><tr>
<th width="15%"> UI location
</th><td colspan="3"> Group: 3D View
</td></tr>
<tr>
<th> Usage
</th><td colspan="3"> Open the Tools sidebar in 3D-View and search for the panel named "Search&amp;Replace"
</td></tr>
<tr>
<th width="15%"> Version
</th><td width="25%"> 1.44.1
</td><th width="15%"> Author(s)
</th><td> Eduard Fekete
</td></tr>
<tr>
<th> Blender
</th><td>2.78c - 2.66
</td><th width="15%">License
</th><td>GPL
</td></tr>



</tbody></table>
<p><br>
</p>
<table class="prettytable" width="100%" style="">
<caption><span style="color: orange;"><b>Executable information</b></span>
</caption><tbody><tr>
<th> File name
</th><td> space_view3d_search&amp;replace.py
</td></tr>
<tr>
<th width="30%"> Current version download
</th><td> <a href="http://wiki.blender.org/uploads/c/cd/Space_view3d_search%26replace1.44.1.zip" class="external free" rel="nofollow">http://wiki.blender.org/uploads/c/cd/Space_view3d_search%26replace1.44.1.zip</a>
</td></tr>




<tr>
<th> Data
</th><td> 2013-11-20
</td></tr></tbody></table>
<p><br>
</p>
<table class="prettytable" width="100%" style="">
<caption>

</caption>





</table>
<script>if (window.showTocToggle) { var tocShowText = "show"; var tocHideText = "hide"; showTocToggle(); } </script>
<p><br>
</p>
<h3> <span class="mw-headline" id="Installation"> Installation </span></h3>
<ul><li> <a href="http://wiki.blender.org/uploads/1/1b/Space_view3d_search%26replace_v1.44.zip" class="external text" rel="nofollow">Download</a> the script then copy it into your \\.blender\scripts\addons folder.
</li><li> Open Blender and go to the addons tab in User Preferences.
</li><li> Enable the script
</li></ul>
<p>Installation: (click <a href="http://www.youtube.com/watch?v=A-4-8h2WEMk" class="external text" rel="nofollow">here</a> if the video controls do not embed, for you.)
</p>
<table align="center">
<tbody><tr>
<td> <iframe width="1000" height="500" src="https://www.youtube.com/embed/A-4-8h2WEMk?wmode=opaque" frameborder="0" allowfullscreen=""></iframe>
</td></tr></tbody></table>
<h3> <span class="mw-headline" id="Description">Description</span></h3>
<p>This Add-On provides a simple search/replace menu for use in the 3D view tools sidebar (under the register "Tools"). Allows users to search for all objects from the scene and replace them or filter them by material/texture and also to replace the material/texture very fast.
</p><p>The searchresult will be written into a interactive output field where users can select the found objects. Selecting an object from the output field will also select the object in the scene, set it to the active object and focus the view on it.
</p>
<div class="tableNormal">
<h3> <span class="mw-headline" id="Functions"> Functions </span></h3>
<div class="floatright"><a href="/index.php/File:AddOn.png" class="image" title="search material menu"><img alt="search material menu" src="/uploads/8/84/AddOn.png" width="330" height="735"></a></div>
<ul><li> Search for objects/materials or textures and replace them very fast.
</li><li> Assign a material to all selected objects.
</li><li> Find out where all objects with the material/texture you've searched are located, or search for all objects in scene.
</li><li> Replace materials of all selected objects with a random material.
</li></ul>
<h3> <span class="mw-headline" id="Instructions"> Instructions </span></h3>
<p>Open the tools sidebar in 3D-View and search for the panel named "Search&amp;Replace".
</p><p><u>Object:</u>
Press on the refresh button. All objects from scene (including lamps, cameras, fields etc) will apear in the list below where you can choice them to select and focus the view on them.
</p><p><u>Material/Texture:</u>
Either choose a material/texture from the list or type in the name of the material/texture you want to search, manually.
</p><p>The result (all objects with the searched material/texture assigned) will be send into the list below the button. Then you are able to select the found objects from the list.
</p>
<center><b><u>Replace Function</u></b></center>
<p><u>Object:</u> At first select all objects you want to replace, from the scene, then choice the new object from the drop down menu right beside the replace button, then press on the replace button.
</p><p><u>Texture/Material:</u> Put the material/texture you want to replace on the left and the new material/texture to the right, then press the "Replace All" button if you like to replace all or if you like to replace just the materials of the selected objects, then press the "Replace selected" button.
</p>
<center><b>Options</b></center>
<p><u>Copy Rot&amp;Scale:</u> If the control box of "Copy Rot&amp;Scale" is set, then replaced objects will keep their old rotation and scale. Works with euler, quaternion and axis-angle.
</p><p><u>Always Deselect:</u> Deselect all objects before selecting an object from the list, if this option is set. Otherwise every object which you select from the list will be added to the selection, this allows to select multiple objects from the list.
</p><p>Replace Objects Demonstration: (click <a href="http://youtu.be/GF-9bIw-EG4" class="external text" rel="nofollow">here</a> if the video controls do not embed, for you.)
</p>
<table align="center">
<tbody><tr>
<td> <iframe width="800" height="380" src="https://www.youtube.com/embed/GF-9bIw-EG4?wmode=opaque" frameborder="0" allowfullscreen=""></iframe>
</td></tr></tbody></table>
<p><br>
</p>
<center><b><u>Assign Functions</u></b></center>
<p><strong>Assing Materials</strong>: If you select on ore more objects and <strong style="color:red">don't select a search material</strong>, then you are able to assing the material which you selected on "replace material" to the objects.</p>
<p>Assing Materials demonstration: (click <a href="http://youtu.be/PqaX9SbwC5c" class="external text" rel="nofollow">here</a> if the video controls do not embed, for you.)
</p>
<table align="center">
<tbody><tr>
<td> <iframe width="1024" height="550" src="https://www.youtube.com/embed/PqaX9SbwC5c?wmode=opaque" frameborder="0" allowfullscreen=""></iframe>
</td></tr></tbody></table>
<center><u>Info</u></center>
<ul><li>You have to press one of the refresh buttons everytime you add/remove/assign/de-assign a material/texture/object to update the list. It's not important which refresh button you press, since all refresh buttons are pointing at the same refresh method.
</li></ul>
<ul><li> You don't have to press a "start search" button or similar, just put the searched material/texture in and the search will start automatically.
</li></ul>
<p><br>
</p><p><br>
</p>
<p><strong>Assign Random Materials</strong>: Select one or more objects and press on the "Random" button, this will replace the objects material with random materials.</p>
<p>HowTo:
</p><p>1. Make sure that you already created some materials, because the materials which you created will be taken to initialise the objects.
</p><p>2. Now just select all the objects you want to change, and press the "Random" Button
</p><p>Random Materials Demonstration: (click <a href="http://youtu.be/IORkjg7l_E8" class="external text" rel="nofollow">here</a> if the video controls do not embed, for you.)
</p>
<table align="center">
<tbody><tr>
<td> <iframe width="1024" height="550" src="https://www.youtube.com/embed/IORkjg7l_E8?wmode=opaque" frameborder="0" allowfullscreen=""></iframe>
</td></tr></tbody></table>
<p><br>
<br style="clear: both">
</p>
</div>
<h3> <span class="mw-headline" id="Advice"> Advice </span></h3>
<p>If you are just interested in the object replace function and don't need the material / texture replacement, then click <a href="http://wiki.blender.org/uploads/6/67/Space_view3d_search%26replace_object.zip" class="external text" rel="nofollow">here</a> to download only this function.
</p><p>Menu: Search-Objects demonstration: (click <a href="http://www.youtube.com/watch?v=Atcw-pv1g1M" class="external text" rel="nofollow">here</a> if the video controls do not embed, for you.)
</p>
<table align="center">
<tbody><tr>
<td> <iframe width="640" height="480" src="https://www.youtube.com/embed/Atcw-pv1g1M?wmode=opaque" frameborder="0" allowfullscreen=""></iframe>
</td></tr></tbody></table>
<h3> <span class="mw-headline" id="Changelog"> Changelog </span></h3>
<ul><li> v1.44 <a href="/index.php?title=User:Eduardf&amp;action=edit&amp;redlink=1" class="new" title="User:Eduardf (page does not exist)">Eduardf</a>
<ul><li> The Search &amp; Replace Menu will now only appear under the Tools section
</li></ul>
</li><li> v1.44 <a href="/index.php?title=User:Eduardf&amp;action=edit&amp;redlink=1" class="new" title="User:Eduardf (page does not exist)">Eduardf</a>
<ul><li> Added the function "Replace with Random Material"
</li></ul>
</li><li> v1.43 <a href="/index.php?title=User:Eduardf&amp;action=edit&amp;redlink=1" class="new" title="User:Eduardf (page does not exist)">Eduardf</a>
<ul><li> Added a new function which allows to assign materials directly
</li></ul>
</li><li> v1.42.2 - <a href="/index.php?title=User:Eduardf&amp;action=edit&amp;redlink=1" class="new" title="User:Eduardf (page does not exist)">Eduardf</a> 14:19, 15 December 2013 (CET)
<ul><li> The Panel will now only be visible in object mode
</li></ul>
</li><li> v1.42.1 - <a href="/index.php?title=User:Eduardf&amp;action=edit&amp;redlink=1" class="new" title="User:Eduardf (page does not exist)">Eduardf</a> 17:39, 1 December 2013 (CET)
<ul><li> Added a function for object replacement
</li><li> Fixed a bug at texture replacement.
</li></ul>
</li><li> v1.42 - <a href="/index.php?title=User:Eduardf&amp;action=edit&amp;redlink=1" class="new" title="User:Eduardf (page does not exist)">Eduardf</a> 22:22, 8 December 2013 (CET) 
<ul><li>I added two control boxes for more functions  (Downloadlink on top of this page)
</li></ul>
</li><li> v1.4 - <a href="/index.php?title=User:Eduardf&amp;action=edit&amp;redlink=1" class="new" title="User:Eduardf (page does not exist)">Eduardf</a> <a href="http://wiki.blender.org/uploads/6/6e/Space_view3d_search%26replace_v1.4.zip" class="external text" rel="nofollow">Download v1.4</a>
<ul><li>I've added a new feature to let users search for all objects in the scene (including cameras, lamps, curves, emptys, fields etc.) and select and focus to them.
</li><li>I've add some labels to make the Add-On easier to understand
</li><li>All refresh buttons point at the same method now.
</li><li>The material menu has now a new button which allows to replace only the materials from the selected objects.
</li></ul>
</li><li> v1.3 - <a href="http://wiki.blender.org/uploads/5/57/Space_view3d_search%26replace_m%26t_v1.3.zip" class="external text" rel="nofollow">Download v1.3</a> <a href="/index.php?title=User:Eduardf&amp;action=edit&amp;redlink=1" class="new" title="User:Eduardf (page does not exist)">Eduardf</a>
<ul><li>I've added a texture replace function
</li></ul>
</li><li> v1.2 - <a href="http://wiki.blender.org/uploads/c/c2/Search_replace_material_1.2.1.zip" class="external text" rel="nofollow">Download v1.2</a> <a href="/index.php?title=User:Eduardf&amp;action=edit&amp;redlink=1" class="new" title="User:Eduardf (page does not exist)">Eduardf</a>
<ul><li>I've added a material replace function. 
</li></ul>
</li><li> v1.11 - <a href="http://wiki.blender.org/uploads/2/20/Space_view3d_search_material_v1.1.1.zip" class="external text" rel="nofollow">Download v1.11</a> <a href="/index.php?title=User:Eduardf&amp;action=edit&amp;redlink=1" class="new" title="User:Eduardf (page does not exist)">Eduardf</a>
<ul><li>The Drop Down List does not contain materials without users anymore. 
</li><li>Problem: Users has to press the Refresh Button to update the material list. 
</li></ul>
</li><li> v1.1 - <a href="http://wiki.blender.org/uploads/0/09/Space_view3d_search_material.zip" class="external text" rel="nofollow">Download v1.1</a> <a href="/index.php?title=User:Eduardf&amp;action=edit&amp;redlink=1" class="new" title="User:Eduardf (page does not exist)">Eduardf</a> + CoDEmanX (created the DropDown List)
<ul><li>Contains a drop down list which is also searchable manually. Problem: List will also show Materials with no users. 
</li></ul>
</li><li> v1.0 - <a href="http://wiki.blender.org/uploads/0/0a/Space_view3d_search_material_1.0.1.zip" class="external text" rel="nofollow">Download v1.0</a> <a href="/index.php?title=User:Eduardf&amp;action=edit&amp;redlink=1" class="new" title="User:Eduardf (page does not exist)">Eduardf</a> + beta-tester (helped me to produce the UI)
<ul><li>Manuall input only.
</li></ul>
</li></ul>
<h3> <span class="mw-headline" id="To-do_list"> To-do list </span></h3>
<ul><li> <div style="border-style:solid; border-width:1px; padding:0px 5px; color:blue; background-color:lightblue; font-weight: bold; font-size:smaller; width: 135px; float:left; text-align:center;">done</div>&nbsp; Let replaced objects keep the old rotation &amp; scale as the old object.
</li><li> <div style="border-style:solid; border-width:1px; padding:0px 5px; color:blue; background-color:lightblue; font-weight: bold; font-size:smaller; width: 135px; float:left; text-align:center;">done</div>&nbsp; Add a random material function.
</li><li> <div style="border-style:solid; border-width:1px; padding:0px 5px; color:blue; background-color:lightblue; font-weight: bold; font-size:smaller; width: 135px; float:left; text-align:center;">done</div>&nbsp; Add a object replacement function.
</li><li> <div style="border-style:solid; border-width:1px; padding:0px 5px; color:blue; background-color:lightblue; font-weight: bold; font-size:smaller; width: 135px; float:left; text-align:center;">done</div>&nbsp; Merge this Add-On and my other Add-On ("GoTo Object").
</li><li> <div style="border-style:solid; border-width:1px; padding:0px 5px; color:blue; background-color:lightblue; font-weight: bold; font-size:smaller; width: 135px; float:left; text-align:center;">done</div>&nbsp; Add a feature to search&amp;replace textures.
</li><li> <div style="border-style:solid; border-width:1px; padding:0px 5px; color:blue; background-color:lightblue; font-weight: bold; font-size:smaller; width: 135px; float:left; text-align:center;">done</div>&nbsp; Add a feature to replace materials.
</li><li> <div style="border-style:solid; border-width:1px; padding:0px 5px; color:blue; background-color:lightblue; font-weight: bold; font-size:smaller; width: 135px; float:left; text-align:center;">done</div>&nbsp; Add a button to replace only selected objects.  
</li><li> <div style="border-style:solid; border-width:1px; padding:0px 5px; color:blue; background-color:lightblue; font-weight: bold; font-size:smaller; width: 135px; float:left; text-align:center;">done</div>&nbsp; Only search for materials/textures with assigned users.
</li><li> <div style="border-style:solid; border-width:1px; padding:0px 5px; color:blue; background-color:lightblue; font-weight: bold; font-size:smaller; width: 135px; float:left; text-align:center;">done</div>&nbsp; Replace the manuall input with a drop down list.
</li><li> <div style="border-style: solid; border-width: 1px; padding: 0px 5px; color: green; background-color: lightgreen; font-weight: bold; font-size: smaller; width: 135px; float: left; text-align: center;">in progress <img alt="Inprogress50.jpg" src="/uploads/6/6c/Inprogress50.jpg" width="25" height="8"> 50%</div>&nbsp; Add a Function to replace only the material/texture of the filtered objects.
</li><li> <div style="border-style: solid; border-width: 1px; padding: 0px 5px; color: green; background-color: lightgreen; font-weight: bold; font-size: smaller; width: 135px; float: left; text-align: center;">in progress <img alt="Inprogress0.jpg" src="/uploads/f/f9/Inprogress0.jpg" width="25" height="8"> 0%</div>&nbsp; Let the search material/texture list update automatically. (not possible due to blender)
</li></ul>
<h3> <span class="mw-headline" id="Support"> Support </span></h3>
<ul><li> e-mail: eduard_fekete@yahoo.de
</li></ul>
<h3> <span class="mw-headline" id="Credits"> Credits </span></h3>
<ul><li> CoDEmanX - Thank you for your tips and for teaching me how to create a drop down list!
</li><li> beta-tester - Thank you for your start help in the forum to create the user interface!
</li></ul>
<p><br>
</p>
<!-- 
NewPP limit report
Preprocessor node count: 263/1000000
Post-expand include size: 3618/2097152 bytes
Template argument size: 451/2097152 bytes
Expensive parser function count: 0/100
-->

<!-- Saved in parser cache with key mediawiki_1_16_2_live_110303-mediawiki_:pcache:idhash:56169-0!1!0!!en!2!edit=0 and timestamp 20170807194729 -->
<div class="printfooter">
Retrieved from "<a href="https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Material_Search">https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Material_Search</a>"</div>
					<div id="catlinks"><div id="catlinks" class="catlinks"><div id="mw-normal-catlinks"><a href="/index.php/Special:Categories" title="Special:Categories">Category</a>: <span dir="ltr"><a href="/index.php/Category:Script" title="Category:Script">Script</a></span></div></div></div>					<!-- END content -->
					
					<div class="visualClear"></div>
				</div>
			</div>
