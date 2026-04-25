# Analysis — Player Model for One-try (UE 5.3, blueprint-only)

## 1. Project context

The repository is currently a **blank, blueprint-only Unreal Engine 5.3 project** (`OneTry.uproject`, no `Source/` module). Previous PRs only added:

- the `.uproject` descriptor with the `ModelingToolsEditorMode` plugin enabled,
- empty `Config/Default*.ini` files pointing at the engine template map `/Engine/Maps/Templates/Template_Default`,
- a CI workflow that packages a Win64 Shipping build inside Epic's official `ghcr.io/epicgames/unreal-engine:dev-slim-5.3` Docker image.

No `Content/` assets exist yet, no `GameMode`, no `Character`. The existing `DefaultInput.ini` already declares axis mappings (`MoveForward`, `MoveRight`, `Turn`, `LookUp`) and a `Jump` action that match a third-person character contract — these will be the input handles for the new pawn.

## 2. Why we should reuse Epic's mannequin

The issue explicitly authorises the use of presets ("используй пресеты если необходимо"). Three independent reasons to use **SKM_Quinn** (or its simplified variant **SKM_Quinn_Simple**) shipped with the UE5 *Third Person* template:

1. **Multi-part skeleton out of the box.** UE5's mannequin skeleton has 89 bones following the standard humanoid hierarchy `Root → Pelvis → Spine_01..03 → Clavicle_L/R → UpperArm_L/R → LowerArm_L/R → Hand_L/R → fingers` and `Pelvis → Thigh_L/R → Calf_L/R → Foot_L/R → Ball_L/R`. This satisfies R3 (separate shoulders, forearms, hands; the same detail on the legs).
2. **Stock idle animations are bundled.** `MM_Idle` (Manny) and `MF_Idle` (Quinn) ship with the same template and play directly on the same skeleton — satisfies R5 with no asset authoring.
3. **First-class retargeting.** The Manny/Quinn skeleton is the de-facto target for the IK Retargeter, Control Rig, Lyra, and the entire Marketplace/Fab animation ecosystem. Future SIGNALIS-styled meshes (low-poly, PSX-era) can be re-skinned to the same skeleton without throwing away any animation work — satisfies R4.

The "Simple" variant (`SKM_Quinn_Simple`) is a lower-poly, no-fingers mesh that still uses the full mannequin skeleton — visually closer to the SIGNALIS aesthetic (low-poly humanoid with chunky limbs, no high-detail fingers) and a cleaner starting point for a survival-horror retexture.

## 3. SIGNALIS aesthetic — what we are aiming at

From the rose-engine press kit and reviews:

- SIGNALIS deliberately replicates **fifth-generation (PS1-era) survival horror** rendering — low-poly 3D characters with limited texture resolution, blended with 2D sprites and dithered post-processing.
- Visual references: **Silent Hill 1–3, Resident Evil 1–3**, East-German 1980s industrial design, analog CRT artefacts.
- Character silhouette: humanoid Replika (worker-android) — slim, uniformed, **clearly readable silhouette at low resolution**.
- Lighting: low-key, high-contrast, monochrome accents over muted reds/teals.

**Implication for the player model:** the choice of `SKM_Quinn_Simple` (low-poly, clean silhouette, no fingers) is the closest stock starting point. The eventual SIGNALIS pass will be:

1. Replace material with a flat / cel-shaded master material + 256² diffuse.
2. Optionally swap mesh for a re-skinned low-poly Replika using the same mannequin skeleton.
3. Add a post-process volume with dithering and chromatic aberration (out of scope for this issue).

## 4. Constraints imposed by the build environment

- **No UE Editor in CI / dev shell.** The repository's CI runs in Epic's Linux Docker image and packages via `BuildCookRun` — there is no interactive editor. The agent that authored this PR also cannot launch the editor to drag-and-drop assets.
- **Binary `.uasset` files cannot be hand-authored.** Skeletal meshes, animations and Blueprints are serialized binary blobs. We cannot generate them from a text-only environment without running the editor.
- **The Docker image already ships the Third Person template.** Epic's `ghcr.io/epicgames/unreal-engine:dev-slim-5.3` image contains the engine at `/home/ue4/UnrealEngine`, which includes `Engine/Content/...` and `Templates/TP_ThirdPersonBP/Content/Characters/Mannequins/...`. We can therefore migrate the mannequin assets headlessly via a Python commandlet at build time.

## 5. Solution approach

The implementation is split into three text-only artefacts that, together, cause the mannequin and idle animation to materialise inside `Content/` the first time the project is opened in the editor (or built in CI):

1. **`Tools/Setup_PlayerMannequin.py`** — an Unreal Editor Python script that:
   - Locates the engine-bundled Third Person template content.
   - Migrates `SKM_Quinn_Simple`, `SK_Mannequin`, `MM_Idle`, `MF_Idle` and the physics asset into `/Game/Characters/Mannequin/`.
   - Creates `/Game/Player/ABP_PlayerCharacter` (an Animation Blueprint that plays `MF_Idle` on loop).
   - Creates `/Game/Player/BP_PlayerCharacter` (a `Character` Blueprint with the skeletal mesh and ABP wired up, capsule sized to the mannequin, mesh rotated -90° on yaw and offset -90 cm on Z to match Epic's convention).
   - Creates `/Game/Player/BP_PlayerGameMode` with `BP_PlayerCharacter` as the default pawn.
2. **`Config/DefaultEngine.ini`** — set `GameMode=/Game/Player/BP_PlayerGameMode.BP_PlayerGameMode_C` so PIE uses the new pawn.
3. **`docs/PlayerModel.md`** — a one-page runbook that explains the two ways to materialise the assets (Tools menu in the editor, or `-run=PythonScript` from the command line / CI).

This keeps the repository **fully text-based and diff-reviewable** — no binary `.uasset` blobs are committed — while making the player model reproducible on any machine that has UE 5.3 installed.

## 6. Validation plan

Manual (in editor):

1. Open `OneTry.uproject` in UE 5.3.
2. Run **Tools → Execute Python Script…** → pick `Tools/Setup_PlayerMannequin.py`.
3. Open the default map, press **Play**. Expect: a multi-part mannequin spawns at PlayerStart, plays `MF_Idle` on loop, WASD moves it, mouse turns it, Space jumps.

Automated (CI, future PR — not required by this issue):

- Add a CI step that runs the script headlessly:
  `UnrealEditor-Cmd OneTry.uproject -run=PythonScript -script="Tools/Setup_PlayerMannequin.py"` before `BuildCookRun`.
- Verify the `BP_PlayerCharacter`, `ABP_PlayerCharacter` and `BP_PlayerGameMode` assets are present in the staged build.

## 7. Risks & mitigations

| Risk | Mitigation |
|---|---|
| User opens the project without running the setup script → no pawn spawns. | `docs/PlayerModel.md` and `README.md` mention the one-click setup. The `DefaultEngine.ini` change is benign if the asset is missing (UE falls back to `DefaultPawn`). |
| UE updates change template asset paths. | Script discovers the template root dynamically via `unreal.Paths.engine_dir()` and tries multiple known sub-paths. |
| Future SIGNALIS retexture needs a different mesh. | Skeleton is preserved; only the `SkeletalMesh` and `Materials` slots need swapping. ABP is mesh-agnostic. |
