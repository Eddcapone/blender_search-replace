# SPDX-License-Identifier: GPL-2.0-or-later
"""
Testskript fuer die "Search & Replace"-Extension (Objekte, Materialien, Texturen).

Ausfuehren:
  - Im Blender Text-Editor: Datei oeffnen und mit "Run Script" (Alt+P) starten,
    waehrend im selben Fenster ein 3D-Viewport sichtbar ist (Standard-Workspaces
    "Layout"/"Scripting" haben das automatisch). Der "Replace"-Operator fuer
    Objekte braucht zwingend einen echten VIEW_3D-Kontext.
  - Oder per Blender-MCP: Inhalt an execute_blender_code uebergeben.

Legt eigene Testdaten (Praefix "SNR_TEST_") an, prueft alle drei Bereiche per
Assertion und raeumt danach wieder auf.
"""

import bpy

ADDON_MODULE = "bl_ext.user_default.search_and_replace"
PREFIX = "SNR_TEST_"

_results = []


def check(name, condition, detail=""):
    status = "OK" if condition else "FEHLER"
    _results.append((name, bool(condition)))
    print(f"[{status}] {name}" + (f"  -- {detail}" if detail else ""))


def skip(name, detail=""):
    print(f"[UEBERSPRUNGEN] {name}" + (f"  -- {detail}" if detail else ""))


def get_view3d_override():
    window = bpy.context.window
    if window is None:
        return None
    area = next((a for a in window.screen.areas if a.type == 'VIEW_3D'), None)
    if area is None:
        return None
    region = next((r for r in area.regions if r.type == 'WINDOW'), None)
    if region is None:
        return None
    return {"window": window, "screen": window.screen, "area": area, "region": region}


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


def deselect_all():
    for obj in bpy.context.scene.objects:
        obj.select_set(False)


def round_vec(v):
    return tuple(round(c, 3) for c in v)


def make_tex_material(name, image):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    tex_node = nt.nodes.new("ShaderNodeTexImage")
    tex_node.image = image
    nt.nodes.active = tex_node
    bsdf = nt.nodes.get("Principled BSDF")
    if bsdf:
        nt.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def active_img_name(mat):
    node = mat.node_tree.nodes.active
    return node.image.name if node and node.image else None


def run_tests():
    _results.clear()
    print("=" * 60)
    print("Search & Replace -- Testlauf")
    print("=" * 60)

    cleanup()

    if ADDON_MODULE not in bpy.context.preferences.addons:
        bpy.ops.preferences.addon_enable(module=ADDON_MODULE)
    check("Addon ist aktiviert", ADDON_MODULE in bpy.context.preferences.addons)
    check("WindowManager.snr_properties ist registriert",
          hasattr(bpy.types.WindowManager, "snr_properties"))

    ov = get_view3d_override()
    if ov is None:
        print("Kein sichtbarer 3D-Viewport gefunden - der Objekt-Replace-Test "
              "wird uebersprungen (braucht zwingend VIEW_3D-Kontext).")

    props = bpy.context.window_manager.snr_properties

    # =======================================================================
    # 1) OBJEKTE
    # =======================================================================
    if ov:
        with bpy.context.temp_override(**ov):
            bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
            src1 = bpy.context.active_object
            src1.name = PREFIX + "Source1"
            src1.rotation_euler = (0.3, 0.1, 0.5)
            src1.scale = (1.5, 1.5, 1.5)

            bpy.ops.mesh.primitive_uv_sphere_add(location=(10, 10, 10))
            target = bpy.context.active_object
            target.name = PREFIX + "ReplaceTarget"

        target_name = target.name

        with bpy.context.temp_override(**ov):
            result = bpy.ops.view3d.obj_search_refresh()
        check("Refresh -> FINISHED", result == {'FINISHED'}, detail=str(result))
        listed = {i.name for i in props.srch_objects}
        check("Objekt-Refresh listet Testobjekte", {src1.name, target_name} <= listed)

        with bpy.context.temp_override(**ov):
            names_in_list = [i.name for i in props.srch_objects]
            idx = names_in_list.index(target_name)
            deselect_all()
            props.srch_index = idx
            selected = [o.name for o in bpy.context.selected_objects]
        check("Klick auf Objektliste waehlt richtiges Objekt", selected == [target_name],
              detail=str(selected))

        with bpy.context.temp_override(**ov):
            deselect_all()
            src1.select_set(True)
            bpy.context.view_layer.objects.active = src1
            props.srch_replace = ""
            result = bpy.ops.replace_selected.objects()
        check("Objekt-Replace ohne Ziel -> CANCELLED", result == {'CANCELLED'}, detail=str(result))
        check("Objekt-Replace ohne Ziel aendert nichts", src1.name in bpy.data.objects)

        src1_name = src1.name
        with bpy.context.temp_override(**ov):
            deselect_all()
            src1.select_set(True)
            bpy.context.view_layer.objects.active = src1
            props.copy_rotation = True
            props.srch_replace = target_name
            result = bpy.ops.replace_selected.objects()
        check("Objekt-Replace (Keep Rotation) -> FINISHED", result == {'FINISHED'}, detail=str(result))
        check("Quellobjekt geloescht", src1_name not in bpy.data.objects)
        dupes = [o for o in bpy.data.objects if o.name.startswith(target_name) and o.name != target_name]
        check("Ein Ersatzobjekt erzeugt", len(dupes) == 1, detail=str([o.name for o in dupes]))
        if dupes:
            dup = dupes[0]
            check("Ersatzobjekt hat Source1-Rotation/Skalierung uebernommen",
                  round_vec(dup.rotation_euler) == round_vec((0.3, 0.1, 0.5))
                  and round_vec(dup.scale) == round_vec((1.5, 1.5, 1.5)))
            mesh = dup.data
            bpy.data.objects.remove(dup, do_unlink=True)
            if mesh is not None and mesh.users == 0:
                bpy.data.meshes.remove(mesh)
    else:
        skip("Objekt-Refresh / Jump / Replace (kein VIEW_3D-Kontext)")

    # =======================================================================
    # 2) MATERIALIEN
    # =======================================================================
    mat_x = bpy.data.materials.new(PREFIX + "MatX")
    mat_y = bpy.data.materials.new(PREFIX + "MatY")
    mat_z = bpy.data.materials.new(PREFIX + "MatZ")

    mesh1 = bpy.data.meshes.new(PREFIX + "MatMesh1")
    mcube1 = bpy.data.objects.new(PREFIX + "MatCube1", mesh1)
    bpy.context.collection.objects.link(mcube1)
    mcube1.data.materials.append(mat_x)

    mesh2 = bpy.data.meshes.new(PREFIX + "MatMesh2")
    mcube2 = bpy.data.objects.new(PREFIX + "MatCube2", mesh2)
    bpy.context.collection.objects.link(mcube2)
    mcube2.data.materials.append(mat_y)
    mcube2.data.materials.append(mat_x)  # MatX in Slot 1 -> prueft, dass alle Slots durchsucht werden

    props.material = mat_x.name
    matched = {i.name for i in props.mat_objects}
    check("Material-Suche findet MatCube1 und MatCube2 (MatX auch in Slot 1)",
          matched == {mcube1.name, mcube2.name}, detail=str(matched))

    props.mat_replace = ""
    result = bpy.ops.replace_all.materials()
    check("Material-Replace ohne Ziel -> CANCELLED", result == {'CANCELLED'}, detail=str(result))

    props.mat_replace = mat_z.name
    result = bpy.ops.replace_all.materials()
    check("Material-Replace -> FINISHED", result == {'FINISHED'}, detail=str(result))
    slots1 = [s.material.name if s.material else None for s in mcube1.material_slots]
    slots2 = [s.material.name if s.material else None for s in mcube2.material_slots]
    check("MatCube1 Slot 0: MatX -> MatZ", slots1 == [mat_z.name], detail=str(slots1))
    check("MatCube2: Slot 0 (MatY) unveraendert, Slot 1 MatX -> MatZ",
          slots2 == [mat_y.name, mat_z.name], detail=str(slots2))

    deselect_all()
    mcube2.select_set(True)
    bpy.context.view_layer.objects.active = mcube2
    result = bpy.ops.random.materials()
    check("Random Materials -> FINISHED", result == {'FINISHED'}, detail=str(result))
    slots_after_random = [s.material for s in mcube2.material_slots]
    check("Random Materials hat allen Slots ein existierendes Material zugewiesen",
          all(m is not None and m.name in bpy.data.materials for m in slots_after_random))

    # =======================================================================
    # 3) TEXTUREN
    # =======================================================================
    img_a = bpy.data.images.new(PREFIX + "ImageA", width=4, height=4)
    img_b = bpy.data.images.new(PREFIX + "ImageB", width=4, height=4)
    img_c = bpy.data.images.new(PREFIX + "ImageC", width=4, height=4)

    tmat1 = make_tex_material(PREFIX + "TexMat1", img_a)
    tmat2 = make_tex_material(PREFIX + "TexMat2", img_a)
    tmat3 = make_tex_material(PREFIX + "TexMat3", img_b)
    mat_no_nodes = bpy.data.materials.new(PREFIX + "MatNoNodes")
    mat_no_nodes.use_nodes = False

    def make_tex_cube(name, mat, loc):
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)
        obj.location = loc
        obj.data.materials.append(mat)
        return obj

    tcube1 = make_tex_cube(PREFIX + "TexCube1", tmat1, (0, 5, 0))
    tcube2 = make_tex_cube(PREFIX + "TexCube2", tmat2, (2, 5, 0))
    tcube3 = make_tex_cube(PREFIX + "TexCube3", tmat3, (4, 5, 0))
    # Objekt mit materialloser bzw. node-loser Situation - darf nicht crashen
    make_tex_cube(PREFIX + "TexCube4_NoNodes", mat_no_nodes, (6, 5, 0))
    mesh5 = bpy.data.meshes.new(PREFIX + "TexMesh5")
    tcube5 = bpy.data.objects.new(PREFIX + "TexCube5_NoMaterial", mesh5)
    bpy.context.collection.objects.link(tcube5)

    props.material = ""  # Materialsuche zuruecksetzen, damit Refresh sauber laeuft
    bpy.ops.view3d.obj_search_refresh()

    all_tex = {i.name for i in props.all_textures}
    check("Texturliste enthaelt ImageA und ImageB, nicht ImageC (noch unbenutzt)",
          {img_a.name, img_b.name} <= all_tex and img_c.name not in all_tex,
          detail=str(all_tex))
    check("Objekte ohne Nodes/Material verursachen keinen Fehler beim Refresh", True)

    props.texture = img_a.name
    matched_tex = {i.name for i in props.tex_objects}
    check("Textur-Suche nach ImageA findet TexCube1 und TexCube2",
          matched_tex == {tcube1.name, tcube2.name}, detail=str(matched_tex))

    props.tex_replace = ""
    result = bpy.ops.replace_all.textures()
    check("Textur-Replace ohne Ziel -> CANCELLED", result == {'CANCELLED'}, detail=str(result))

    props.tex_replace = img_c.name
    result = bpy.ops.replace_all.textures()
    check("Textur-Replace -> FINISHED", result == {'FINISHED'}, detail=str(result))
    check("TexMat1: ImageA -> ImageC", active_img_name(tmat1) == img_c.name)
    check("TexMat2: ImageA -> ImageC", active_img_name(tmat2) == img_c.name)
    check("TexMat3 (ImageB) unveraendert", active_img_name(tmat3) == img_b.name)

    # Jump-to-object ueber die Texturliste
    if ov:
        with bpy.context.temp_override(**ov):
            props.texture = img_b.name
            names = [i.name for i in props.tex_objects]
            deselect_all()
            props.tex_index = 0
            selected = [o.name for o in bpy.context.selected_objects]
        check("Klick auf Texturliste waehlt richtiges Objekt",
              selected == names, detail=f"names={names} selected={selected}")
    else:
        skip("Jump-to-Object ueber Texturliste (kein VIEW_3D-Kontext)")

    # --- Aufraeumen ----------------------------------------------------------
    cleanup()
    check("Aufraeumen: keine Testobjekte mehr vorhanden",
          not any(o.name.startswith(PREFIX) for o in bpy.data.objects))
    check("Aufraeumen: keine Testmaterialien mehr vorhanden",
          not any(m.name.startswith(PREFIX) for m in bpy.data.materials))
    check("Aufraeumen: keine Testbilder mehr vorhanden",
          not any(i.name.startswith(PREFIX) for i in bpy.data.images))

    # --- Zusammenfassung -------------------------------------------------
    total = len(_results)
    passed = sum(1 for _, ok in _results if ok)
    failed = total - passed
    print("-" * 60)
    print(f"Ergebnis: {passed}/{total} OK, {failed} FEHLER")
    if failed:
        print("Fehlgeschlagen:")
        for name, ok in _results:
            if not ok:
                print(f"  - {name}")
    print("=" * 60)
    return failed == 0


if __name__ == "__main__":
    run_tests()
