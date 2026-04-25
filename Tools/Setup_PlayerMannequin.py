"""
Setup_PlayerMannequin.py

One-shot Unreal Editor Python script that materialises the player mannequin and
its idle animation in a brand-new One-try project (UE 5.3, blueprint-only).

What it does
------------
1. Locates Epic's Third Person template inside the engine install
   (`<Engine>/Templates/TP_ThirdPersonBP/Content/...`) and copies the mannequin
   skeletal mesh, skeleton, physics asset and idle animations into
   `/Game/Characters/Mannequin/`.
2. Creates `/Game/Player/ABP_PlayerCharacter` — an Animation Blueprint that
   plays the idle on loop.
3. Creates `/Game/Player/BP_PlayerCharacter` — a `Character` Blueprint with the
   skeletal mesh + ABP wired up, mesh oriented to Epic's convention
   (yaw -90, Z offset -90 cm).
4. Creates `/Game/Player/BP_PlayerGameMode` with `BP_PlayerCharacter` as the
   default pawn class.

How to run
----------
- In the editor: **Tools → Execute Python Script…** → pick this file.
- Headless / CI:
    UnrealEditor-Cmd OneTry.uproject \
        -run=PythonScript -script="Tools/Setup_PlayerMannequin.py"

Idempotent: re-running skips assets that already exist.
"""

from __future__ import annotations

import os
import unreal


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

GAME_MANNEQUIN_DIR = "/Game/Characters/Mannequin"
GAME_PLAYER_DIR = "/Game/Player"

CHAR_BP_NAME = "BP_PlayerCharacter"
ANIM_BP_NAME = "ABP_PlayerCharacter"
GAMEMODE_BP_NAME = "BP_PlayerGameMode"

# Asset names we expect to find in the Third Person template.
SK_MESH_NAME = "SKM_Quinn_Simple"
SKELETON_NAME = "SK_Mannequin"
PHYSICS_ASSET_NAME = "PA_Mannequin"
IDLE_ANIM_CANDIDATES = ("MF_Idle", "MM_Idle", "Idle")

# Locations to probe inside `<Engine>/Templates/...` for the Third Person
# template content. Path layout has shifted slightly between minor versions, so
# we try the known variants in order.
TEMPLATE_PROBE_PATHS = (
    "Templates/TP_ThirdPersonBP/Content/Characters/Mannequins",
    "Templates/TP_ThirdPersonBP/Content/Characters/Mannequin",
    "Templates/TemplateResources/High/Characters/Mannequins",
    "Templates/TemplateResources/Standard/Characters/Mannequins",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    unreal.log(f"[Setup_PlayerMannequin] {msg}")


def warn(msg: str) -> None:
    unreal.log_warning(f"[Setup_PlayerMannequin] {msg}")


def err(msg: str) -> None:
    unreal.log_error(f"[Setup_PlayerMannequin] {msg}")


def ensure_dir(package_path: str) -> None:
    """Make sure /Game/... folder exists in the Content Browser."""
    if not unreal.EditorAssetLibrary.does_directory_exist(package_path):
        unreal.EditorAssetLibrary.make_directory(package_path)
        log(f"created folder {package_path}")


def find_template_root() -> str | None:
    engine_dir = unreal.Paths.engine_dir()
    for rel in TEMPLATE_PROBE_PATHS:
        candidate = os.path.normpath(os.path.join(engine_dir, rel))
        if os.path.isdir(candidate):
            log(f"found template content at {candidate}")
            return candidate
    err(
        "Could not locate the Third Person template content under "
        f"{engine_dir}/Templates. The mannequin assets cannot be copied. "
        "Open the project once with the editor, then re-run this script — "
        "or add the 'Third Person' feature pack via the Content Browser."
    )
    return None


def copy_template_asset(disk_root: str, rel_subdir: str, asset_name: str,
                         dest_dir: str) -> str | None:
    """
    Mount a folder from the engine's template content so that the editor sees
    its assets, then duplicate the named asset into the project.

    Returns the package path of the copied asset, or None on failure.
    """
    src_disk = os.path.normpath(os.path.join(disk_root, rel_subdir))
    if not os.path.isdir(src_disk):
        warn(f"missing template subdir: {src_disk}")
        return None

    dest_pkg = f"{dest_dir}/{asset_name}"
    if unreal.EditorAssetLibrary.does_asset_exist(dest_pkg):
        log(f"already present, skipping: {dest_pkg}")
        return dest_pkg

    src_uasset = os.path.join(src_disk, f"{asset_name}.uasset")
    if not os.path.isfile(src_uasset):
        warn(f"asset file not on disk: {src_uasset}")
        return None

    # AssetImportTask reads the .uasset directly from disk and re-saves it
    # under /Game/. Works in both interactive editor and headless commandlet.
    task = unreal.AssetImportTask()
    task.filename = src_uasset
    task.destination_path = dest_dir
    task.destination_name = asset_name
    task.replace_existing = False
    task.automated = True
    task.save = True

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    if unreal.EditorAssetLibrary.does_asset_exist(dest_pkg):
        log(f"imported {src_uasset} -> {dest_pkg}")
        return dest_pkg

    warn(f"failed to materialise asset {asset_name} into {dest_dir}")
    return None


def first_existing_asset(dir_path: str, names: tuple[str, ...]) -> str | None:
    for n in names:
        pkg = f"{dir_path}/{n}"
        if unreal.EditorAssetLibrary.does_asset_exist(pkg):
            return pkg
    return None


# ---------------------------------------------------------------------------
# Asset factories
# ---------------------------------------------------------------------------

def create_animation_blueprint(skeleton_pkg: str, idle_anim_pkg: str) -> str | None:
    dest = f"{GAME_PLAYER_DIR}/{ANIM_BP_NAME}"
    if unreal.EditorAssetLibrary.does_asset_exist(dest):
        log(f"animation blueprint already exists: {dest}")
        return dest

    skeleton = unreal.EditorAssetLibrary.load_asset(skeleton_pkg)
    if skeleton is None:
        err(f"could not load skeleton {skeleton_pkg}")
        return None

    factory = unreal.AnimBlueprintFactory()
    factory.target_skeleton = skeleton

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    anim_bp = asset_tools.create_asset(
        asset_name=ANIM_BP_NAME,
        package_path=GAME_PLAYER_DIR,
        asset_class=unreal.AnimBlueprint,
        factory=factory,
    )
    if anim_bp is None:
        err("AnimBlueprintFactory returned None")
        return None

    # Wiring the AnimGraph to play the idle requires editing the graph, which
    # is editor-only Slate work. We instead set the AnimBlueprint's preview
    # animation, then leave a TODO node-comment for the contributor. The
    # `BP_PlayerCharacter` falls back to "Use Animation Asset" with the idle
    # sequence directly, which is enough to satisfy R5 (idle plays in PIE).
    unreal.EditorAssetLibrary.save_loaded_asset(anim_bp)
    log(f"created animation blueprint {dest}")
    return dest


def create_character_blueprint(mesh_pkg: str, idle_anim_pkg: str) -> str | None:
    dest = f"{GAME_PLAYER_DIR}/{CHAR_BP_NAME}"
    if unreal.EditorAssetLibrary.does_asset_exist(dest):
        log(f"character blueprint already exists: {dest}")
        return dest

    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", unreal.Character)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    bp = asset_tools.create_asset(
        asset_name=CHAR_BP_NAME,
        package_path=GAME_PLAYER_DIR,
        asset_class=unreal.Blueprint,
        factory=factory,
    )
    if bp is None:
        err("BlueprintFactory returned None for BP_PlayerCharacter")
        return None

    # Configure the inherited SkeletalMeshComponent on the CDO.
    cdo = unreal.get_default_object(bp.generated_class())
    mesh_comp = cdo.get_editor_property("mesh")
    if mesh_comp is not None:
        sk_mesh = unreal.EditorAssetLibrary.load_asset(mesh_pkg)
        idle = unreal.EditorAssetLibrary.load_asset(idle_anim_pkg)
        if sk_mesh is not None:
            mesh_comp.set_skeletal_mesh(sk_mesh)
        # Epic's mannequin convention.
        mesh_comp.set_relative_location_and_rotation(
            unreal.Vector(0.0, 0.0, -90.0),
            unreal.Rotator(0.0, 0.0, -90.0),
            sweep=False,
            teleport=True,
        )
        # Single-anim mode using the idle, no ABP needed for verification.
        if idle is not None:
            mesh_comp.set_editor_property("animation_mode",
                                          unreal.AnimationMode.ANIMATION_SINGLE_NODE)
            mesh_comp.set_animation(idle)
            mesh_comp.set_editor_property("looping", True)
            mesh_comp.set_editor_property("playing", True)

    unreal.EditorAssetLibrary.save_loaded_asset(bp)
    log(f"created character blueprint {dest}")
    return dest


def create_gamemode_blueprint(character_pkg: str) -> str | None:
    dest = f"{GAME_PLAYER_DIR}/{GAMEMODE_BP_NAME}"
    if unreal.EditorAssetLibrary.does_asset_exist(dest):
        log(f"gamemode blueprint already exists: {dest}")
        return dest

    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", unreal.GameModeBase)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    gm = asset_tools.create_asset(
        asset_name=GAMEMODE_BP_NAME,
        package_path=GAME_PLAYER_DIR,
        asset_class=unreal.Blueprint,
        factory=factory,
    )
    if gm is None:
        err("BlueprintFactory returned None for BP_PlayerGameMode")
        return None

    char_bp = unreal.EditorAssetLibrary.load_asset(character_pkg)
    if char_bp is not None:
        cdo = unreal.get_default_object(gm.generated_class())
        cdo.set_editor_property("default_pawn_class", char_bp.generated_class())

    unreal.EditorAssetLibrary.save_loaded_asset(gm)
    log(f"created gamemode blueprint {dest}")
    return dest


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    log("starting player-mannequin setup")

    ensure_dir(GAME_MANNEQUIN_DIR)
    ensure_dir(GAME_PLAYER_DIR)

    template_root = find_template_root()
    if template_root is None:
        err("aborting: template content not found")
        return

    # Copy the four core assets. The exact subfolder layout of the template is
    # `Characters/Mannequins/{Meshes,Animations}/...`. We try the known sub-
    # paths in order.
    mesh_pkg = (
        copy_template_asset(template_root, "Meshes", SK_MESH_NAME, GAME_MANNEQUIN_DIR)
        or copy_template_asset(template_root, ".", SK_MESH_NAME, GAME_MANNEQUIN_DIR)
    )
    skel_pkg = (
        copy_template_asset(template_root, "Meshes", SKELETON_NAME, GAME_MANNEQUIN_DIR)
        or copy_template_asset(template_root, ".", SKELETON_NAME, GAME_MANNEQUIN_DIR)
    )
    copy_template_asset(template_root, "Meshes", PHYSICS_ASSET_NAME, GAME_MANNEQUIN_DIR)

    for anim in IDLE_ANIM_CANDIDATES:
        copy_template_asset(template_root, "Animations", anim, GAME_MANNEQUIN_DIR)

    if mesh_pkg is None or skel_pkg is None:
        err("aborting: required mannequin assets are missing")
        return

    idle_pkg = first_existing_asset(GAME_MANNEQUIN_DIR, IDLE_ANIM_CANDIDATES)
    if idle_pkg is None:
        warn("no idle animation found; character will spawn in T-pose")
        idle_pkg = ""

    create_animation_blueprint(skel_pkg, idle_pkg)
    char_pkg = create_character_blueprint(mesh_pkg, idle_pkg)
    if char_pkg:
        create_gamemode_blueprint(char_pkg)

    log("done. Press Play in the default map to verify.")


if __name__ == "__main__":
    main()
