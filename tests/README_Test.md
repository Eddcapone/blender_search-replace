# Testanleitung – Search & Replace (Objekte / Materialien / Texturen)

Zwei Testwerkzeuge in diesem Ordner:

| Datei | Zweck |
|---|---|
| `test_search_and_replace.py` | **Automatisierter** Regressionstest für alle drei Bereiche. Legt eigene Testdaten an, prüft per Assertion, räumt danach auf. |
| `setup_manual_test_scene.py` | Baut eine **Demo-Szene** auf, die stehen bleibt, damit du die Extension selbst im N-Panel ausprobieren kannst. |

Extension muss aktiviert sein: *Edit > Preferences > Get Extensions/Add-ons* → „Search & Replace".

**Wichtig:** Beide Skripte im Blender Text-Editor ausführen, während im selben Fenster ein 3D-Viewport sichtbar ist. Der Objekt-„Replace"-Operator braucht zwingend einen echten VIEW_3D-Kontext.

---

## Zum Textur-Konzept

„Textur" bedeutet hier: das Bild am **aktiven Node** im Shader-Node-Baum des aktiven Materials (`node_tree.nodes.active`), sofern das ein Image-Texture-Node ist. Das alte Blender-Textur-Slot-System (`bpy.data.textures`, `material.active_texture`) wurde mit Blender 2.80 entfernt und existiert nicht mehr — das ist der nächstliegende moderne Ersatz. Praktisch heißt das: Klicke im Shader-Editor auf den gewünschten Image-Texture-Node, um ihn zum „aktiven" zu machen, bevor du ihn über dieses Panel suchst/ersetzt.

---

## 1. Automatisierter Test (schneller Regressionscheck)

1. `Window > Toggle System Console` einschalten.
2. `test_search_and_replace.py` im Text-Editor öffnen, mit `Alt+P` ausführen.
3. Am Ende steht `Ergebnis: 30/30 OK, 0 FEHLER`.

Räumt sich selbst auf (Präfix `SNR_TEST_`, unabhängig von der Demo-Szene unten, die `SNR_DEMO_` verwendet).

---

## 2. Manuelle Testszene

1. `setup_manual_test_scene.py` im Text-Editor öffnen, mit `Alt+P` ausführen.
2. Im 3D-Viewport `N` drücken → Tab **Tools** → Panel **„Search&Replace"** öffnen.
3. Auf den Refresh-Button klicken, um alle drei Listen erstmalig zu füllen.

Erneutes Ausführen baut die Szene sauber neu auf. Nur entfernen: `CLEANUP_ONLY = True` setzen und erneut ausführen.

### Angelegte Objekte

**Objekte-Bereich (y=0):**

| Objekt | Zweck |
|---|---|
| `SNR_DEMO_Obj_Source_A` | Würfel, 45° gedreht. Vorausgewählt. |
| `SNR_DEMO_Obj_Source_B` | Würfel, 30° gedreht, doppelte Größe. Vorausgewählt. |
| `SNR_DEMO_Obj_Source_C_nicht_ausgewaehlt` | Absichtlich nicht ausgewählt. |
| `SNR_DEMO_Obj_ReplaceWithSphere` | Ersatzobjekt-Kandidat. |

**Materialien-Bereich (y=3, farbig sichtbar im Viewport):**

| Objekt | Slots |
|---|---|
| `SNR_DEMO_Mat_Cube1_nurX` | Rot (X) |
| `SNR_DEMO_Mat_Cube2_X_dann_Y` | Rot (X), Grün (Y) |
| `SNR_DEMO_Mat_Cube3_Y_dann_X` | Grün (Y), Rot (X) — prüft Slot-Reihenfolge |
| `SNR_DEMO_Mat_Cube4_nurY` | Grün (Y) |

Material `Mat_Blau_Z_unbenutzt` existiert, ist aber keinem Objekt zugewiesen — als Replace-Ziel gedacht.

**Texturen-Bereich (y=6):**

| Objekt | Aktiver Image-Texture-Node |
|---|---|
| `SNR_DEMO_Tex_Cube1` | Bild „Rot A" |
| `SNR_DEMO_Tex_Cube2` | Bild „Rot A" |
| `SNR_DEMO_Tex_Cube3` | Bild „Grün B" |

Bild `Bild_Blau_C_unbenutzt` existiert, ist aber nirgends aktiv zugewiesen — als Replace-Ziel gedacht. Zum optischen Vergleich Shading-Modus „Material Preview" oder „Rendered" nutzen (Solid-Modus zeigt keine Texturfarben).

---

### Checkliste – manuell durchklicken

**Objekte**
- [ ] Refresh klicken → Liste zeigt alle Szenenobjekte.
- [ ] Listeneintrag anklicken → Ansicht springt zum Objekt.
- [ ] `Source_A`/`Source_B` sind vorausgewählt. Zielobjekt `Obj_ReplaceWithSphere` wählen, „Replace selection with :" klicken.
  → Beide Würfel werden durch Kugeln ersetzt, mit übernommener Rotation/Skalierung (falls „Copy Rot&Scale" aktiv). `Source_C` bleibt unangetastet.

**Materialien**
- [ ] Im Suchfeld „Rot X" wählen → Liste zeigt `Mat_Cube1`, `Mat_Cube2`, `Mat_Cube3` (auch wo Rot in Slot 1 sitzt).
- [ ] Zielmaterial „Blau Z" wählen, „Replace All" klicken → alle Rot-Vorkommen werden blau, Grün-Slots bleiben unverändert.
- [ ] Ein oder mehrere Würfel auswählen, „Random" klicken → Slots bekommen zufällige vorhandene Materialien, bei jedem Klick ein neues Ergebnis.

**Texturen**
- [ ] Im Suchfeld „Rot A" wählen → Liste zeigt `Tex_Cube1`, `Tex_Cube2`.
- [ ] Zielbild „Blau C" wählen, „Replace All" klicken → beide Materialien zeigen jetzt Blau C im Image-Texture-Node (im Shader-Editor oder Material-Preview-Shading sichtbar). `Tex_Cube3` (Grün B) bleibt unverändert.
- [ ] Listeneintrag anklicken → Ansicht springt zum Objekt.

**Fehlerfälle (dürfen nichts tun, keine Fehlermeldung in der Konsole)**
- [ ] Replace/„Replace All" jeweils ohne gewähltes Zielobjekt/-material/-bild klicken → nichts passiert.
- [ ] Panel im Edit Mode (Tab-Taste auf einem Mesh) prüfen → Panel wird ausgeblendet (nur im Object Mode sichtbar).

---

## 3. Aufräumen

- Manuelle Testszene entfernen: `setup_manual_test_scene.py` mit `CLEANUP_ONLY = True` erneut ausführen.
- Der automatisierte Test räumt sich immer selbst auf, auch nach einem Fehlschlag.
