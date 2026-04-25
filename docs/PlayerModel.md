# Player model — setup runbook

This project ships with a one-shot Python script that materialises the player
mannequin (`SKM_Quinn_Simple`, the engine-stock multi-part Manny/Quinn skeleton),
the idle animation (`MF_Idle`), and the matching `BP_PlayerCharacter` /
`BP_PlayerGameMode` Blueprints inside `Content/`.

The script is committed as text — no binary `.uasset` files are stored in the
repository — so you must run it once before pressing **Play**.

## TL;DR

1. Open `OneTry.uproject` in **Unreal Engine 5.3**.
2. **Tools → Execute Python Script…** → select `Tools/Setup_PlayerMannequin.py`.
3. Open the default map → press **Play**.
   You should see a multi-part mannequin standing at the PlayerStart, looping
   the idle animation, controllable via WASD + mouse + Space.

## What the script creates

```
Content/
├── Characters/
│   └── Mannequin/
│       ├── SKM_Quinn_Simple   (skeletal mesh — multi-part, low-poly)
│       ├── SK_Mannequin       (89-bone skeleton)
│       ├── PA_Mannequin       (physics asset)
│       └── MF_Idle            (idle animation sequence)
└── Player/
    ├── BP_PlayerCharacter     (Character — mesh + idle wired up)
    ├── ABP_PlayerCharacter    (Animation Blueprint targeting the skeleton)
    └── BP_PlayerGameMode      (sets BP_PlayerCharacter as default pawn)
```

`Config/DefaultEngine.ini` already references
`/Game/Player/BP_PlayerGameMode` as the global default GameMode, so PIE picks
up the new pawn automatically once the script has run.

## Headless / CI use

The same script runs without an interactive editor:

```bash
UnrealEditor-Cmd OneTry.uproject \
    -run=PythonScript \
    -script="Tools/Setup_PlayerMannequin.py"
```

Inside Epic's official `ghcr.io/epicgames/unreal-engine:dev-slim-5.3` Docker
image (which the `.github/workflows/build.yml` workflow already uses), the
binary is at `/home/ue4/UnrealEngine/Engine/Binaries/Linux/UnrealEditor-Cmd`.

The script is idempotent — re-running it is a no-op once the assets exist.

## Why a script and not committed `.uasset` files?

| Reason | Detail |
|---|---|
| **Reviewable diffs** | Skeletal meshes, animations and Blueprints serialize as opaque binary blobs. A Python script is plain text. |
| **Repository size** | The mannequin asset pack is several MB; we keep the repo lean. |
| **Always uses your engine version** | The script copies the assets that ship with whichever UE version the user has installed, avoiding cross-version `.uasset` migration warnings. |
| **Reproducible** | The same script works on every contributor's machine and inside CI. |

## SIGNALIS styling — future work

The current setup intentionally uses Epic's stock `SKM_Quinn_Simple`. Once a
SIGNALIS-style low-poly Replika mesh is available it can be dropped in by:

1. Importing the new mesh and skinning it to the existing `SK_Mannequin`
   skeleton (or retargeting via the IK Retargeter).
2. Editing two lines in `Tools/Setup_PlayerMannequin.py`
   (`SK_MESH_NAME = "<new mesh>"`).
3. Re-running the script — `BP_PlayerCharacter`, the idle animation and the
   GameMode are unchanged.

See [`docs/case-studies/issue-5/`](./case-studies/issue-5/) for the full
analysis behind this design.
