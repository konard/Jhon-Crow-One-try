# Proposed solutions — comparison

| # | Approach | Effort | Multi-part skeleton (R3) | Idle anim (R5) | SIGNALIS-friendly (R4) | Reviewable diff | Verdict |
|---|---|---|---|---|---|---|---|
| **A** | **Reuse `SKM_Quinn_Simple` + `MF_Idle` from the engine's Third Person template via a Python setup script** | **Low** | **Yes** (89-bone Manny/Quinn skeleton) | **Yes** (`MF_Idle`) | **Yes** (low-poly silhouette, easy retexture, skeleton kept for retargeting) | **Yes** (only text artefacts: 1 Python script, 1 .ini change, docs) | **Selected** |
| B | Commit the `.uasset` mannequin files directly into `Content/Characters/Mannequins/` | Low–Medium | Yes | Yes | Yes | **No** — binary `.uasset` blobs, opaque diff, ~MB-sized commits | Rejected |
| C | Pull a Mixamo character (e.g. *Y-Bot*) + idle, retarget to mannequin skeleton | High | Yes | Yes (after retarget) | Yes | Partly (FBX is binary too, retarget chain is non-trivial) | Deferred to a future PR |
| D | Use a `MetaHuman` | Very High | Yes (different skeleton) | Yes | **No** — wrong aesthetic for SIGNALIS | No (binary, very large) | Rejected |
| E | Author a custom low-poly mesh + bones + idle in Blender | Very High | Yes | Yes | Yes | Partly (FBX binary) | Rejected — re-inventing what UE ships |

## Why A wins for this issue

1. **Zero binary assets in the diff.** The PR is exclusively text: a Python script, an `.ini` change, and Markdown. Every byte is reviewable.
2. **Self-bootstrapping.** The first time the project is opened in UE 5.3, the contributor runs **Tools → Execute Python Script…** once and the mannequin, ABP, character BP and game mode appear in `Content/`. No drag-and-drop.
3. **Headless-CI compatible.** The same script works as a `-run=PythonScript` commandlet inside Epic's Docker image, which the existing `.github/workflows/build.yml` already pulls. A future CI step can re-materialise the assets at build time without a local checkout step.
4. **Clean upgrade path to SIGNALIS.** Once a low-poly Replika mesh exists, swapping it in is two lines in the same script (replace `SKM_Quinn_Simple` reference); the skeleton, ABP and BP keep working unchanged.

## Existing components reused

| Component | Source | Role |
|---|---|---|
| `SKM_Quinn_Simple` (skeletal mesh) | UE 5.3 Third Person template | Player body — multi-part, low-poly. |
| `SK_Mannequin` (skeleton) | UE 5.3 Third Person template | Bone hierarchy (89 bones). |
| `MF_Idle` (animation sequence) | UE 5.3 Third Person template | Idle pose, satisfies R5. |
| `Character` (engine class) | UE 5.3 (`/Script/Engine.Character`) | Base class for `BP_PlayerCharacter` — capsule + mesh + character movement. |
| `GameModeBase` (engine class) | UE 5.3 (`/Script/Engine.GameModeBase`) | Base class for `BP_PlayerGameMode`, sets default pawn. |
| `AnimInstance` (engine class) | UE 5.3 (`/Script/Engine.AnimInstance`) | Base class for `ABP_PlayerCharacter` — drives the idle. |
| Python Editor Scripting Plugin | UE 5.3 built-in | Runs the setup script. |

No third-party plugins, no Marketplace dependencies, no network downloads.
