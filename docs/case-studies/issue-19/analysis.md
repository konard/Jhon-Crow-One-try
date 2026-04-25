# Deep Analysis — Issue #19: Migrate to Unreal Engine

## 1. Problem statement

Issue #19 (in Russian) reads:

> переведи проект на UNREAL ENGINE
> в том числе сборку portable exe

Translated: "Translate the project to UNREAL ENGINE, including the portable exe build."

No additional details or comments were provided. The request is to reverse the
Unity migration from PR #9 and restore the UE5 project structure with a working
portable exe build via GitHub Actions.

## 2. Project history and engine oscillation

| Event | Engine | Source |
|---|---|---|
| Issue #2, PR #3 | Unreal Engine 5.3 | PR #3 — blueprint-only UE5 project + BuildCookRun CI |
| Issue #8, PR #9 | Unity 6.3 LTS | PR #9 — full engine migration to Unity |
| Issues #10, #12, #15 | Unity 6.3 LTS | Three consecutive "portable exe not building" reports |
| Issue #16, PR #16 | Unity 6.3 LTS | Switch to credential-based activation (UNITY_EMAIL/PASSWORD) |
| Issue #17 | Unity 6.3 LTS | Another "still not building portable exe" report |
| Issue #19 | → Unreal Engine 5.3 | **This issue — migrate back to UE5** |

The pattern is clear: the Unity CI pathway has been persistently broken across
four separate issues (#10, #12, #15, #17) despite multiple fixes. The primary
barrier is Unity credential management — activating a Unity Personal license
in headless CI is inherently fragile (deprecated `.alf`/`.ulf` flow, credential-
based `buildalon/activate-unity-license`, and rate limits on activation slots).

## 3. Root cause of Unity CI fragility

Unity Personal license activation in CI:
- Requires email/password credentials (secrets) — any account change breaks CI.
- `buildalon/activate-unity-license` is a third-party action that may change behavior.
- Activation slot limits: Unity allows only a fixed number of concurrent activations;
  a failed build that doesn't return the license blocks subsequent builds.
- Unity 6.x deprecated the manual `.alf`→`.ulf` portal, making re-activation harder.

In contrast, the UE5 CI approach requires:
- A GitHub account linked to an Epic Games account (one-time setup, persistent).
- A GitHub PAT with `read:packages` scope to pull the Docker image.
- No per-build license activation — the Docker image contains a full UE5 installation.

## 4. Trade-off analysis: UE5 vs Unity for this project

| Factor | Unreal Engine 5.3 | Unity 6.3 LTS |
|---|---|---|
| CI portable exe | Docker image (Epic-gated but stable once set up) | Credential-based activation (fragile, historically broken) |
| Blueprint-only iteration | First-class, no compile step | N/A (C# always compiles) |
| 3D action mechanics (dash, parry) | Blueprint visual scripting or C++ | C# MonoBehaviours |
| Repository size | Config files are text (minimal until Content added) | Text YAML assets, similar footprint |
| One-time setup cost | Link GitHub + Epic account, create PAT | Add UNITY_EMAIL + UNITY_PASSWORD secrets |
| Long-term setup stability | PAT only expires if rotated | Password changes break CI immediately |
| Engine version pinning | `"EngineAssociation": "5.3"` in `.uproject` | `ProjectVersion.txt` + Unity Hub |

Given the repeated CI failures on Unity and the explicit request in issue #19,
migrating back to UE5 is the correct action.

## 5. Implementation decisions

### 5.1 UE5 version

Pin to **5.3** — the same version originally used in PR #3, matching the Epic
Docker image tag `dev-slim-5.3`. This is a stable release with full CI support.

### 5.2 Blueprint-only project

No C++ modules are included. The `OneTry.uproject` has an empty `"Modules": []`
array. This keeps:
- Compile times in CI minimal (no C++ source).
- The project accessible to designers without a C++ toolchain.
- The door open for C++ modules in future PRs.

### 5.3 GitHub Actions workflow

The workflow mirrors the structure from PR #16's Unity workflow:
- A `checklicense` job that checks for `EPIC_GITHUB_TOKEN` and emits a warning
  if missing, keeping CI green even without credentials.
- A `build` job that only runs when credentials are present, pulling Epic's
  Docker image and running `BuildCookRun` with shipping flags.
- The result is zipped and uploaded as `OneTry-Win64-<run-number>`.

### 5.4 Unity files retained as historical record

The Unity-specific files (`Assets/`, `Packages/`, `ProjectSettings/`) are
removed because they conflict with UE5 project structure. The game design
document and case studies remain in the repository as documentation.

## 6. Input mapping

The `Config/DefaultInput.ini` pre-maps the core mechanics from `GAME_DESIGN.md`:

| Action | Key |
|---|---|
| Jump | Spacebar |
| Dash | Left Shift |
| Light Attack | Left Mouse Button |
| Heavy Attack | Right Mouse Button |
| Parry | E |
| Ultimate | Q |
| Move Forward/Back | W/S |
| Move Left/Right | A/D |

These match the design document's § "Атаки" and § "Механики движения" exactly.

## 7. Open items for future PRs

- Add a custom level/map in `Content/Maps/` (currently uses the UE5 OpenWorld template).
- Add Blueprint assets for the player character, movement mechanics, and combat.
- Set up cross-compilation toolchain in the Docker image for C++ if needed later.
- Consider UE5's Enhanced Input System plugin (replaces legacy `DefaultInput.ini`
  action mappings) for the input buffering and hold-vs-tap distinctions described
  in the design doc.
