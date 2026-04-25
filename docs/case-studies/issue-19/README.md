# Case Study — Issue #19

> **Issue:** [Jhon-Crow/One-try#19 — переведи проект на UNREAL ENGINE](https://github.com/Jhon-Crow/One-try/issues/19)
> **Pull request:** [Jhon-Crow/One-try#20](https://github.com/Jhon-Crow/One-try/pull/20)
> **Branch:** `issue-19-d66e5b263421`

## Files

| File | Purpose |
|---|---|
| `analysis.md` | Deep analysis: project history, engine oscillation, root cause, tradeoffs of returning to UE5. |
| `raw/` | Raw data snapshots: issue JSON, all-issues JSON, all-PRs JSON. |

## TL;DR

Issue #19 requests the project be translated back to **Unreal Engine** (including
portable exe build). This is the third engine direction change in the project's
history:

1. **PR #3** — project started on Unreal Engine 5.3 (issue #2).
2. **PR #9** — migrated to Unity 6.3 LTS (issue #8), citing GAME_DESIGN.md's
   "Движок: Unity" declaration and CI friction caused by the Epic account requirement.
3. **Issue #19** — now requests migration back to Unreal Engine.

### What changed in this PR

1. **Replaced Unity project skeleton** (`Assets/`, `Packages/`, `ProjectSettings/`)
   with a UE5 blueprint-only skeleton (`OneTry.uproject`, `Config/`, `Content/Maps/`).
2. **Updated `.github/workflows/build.yml`** to use Epic's official Docker image
   (`ghcr.io/epicgames/unreal-engine:dev-slim-5.3`) and `BuildCookRun` UAT to
   produce a portable Win64 Shipping EXE artifact.
3. **Updated `.gitignore`** for UE5 generated directories.
4. **Updated `README.md`** with UE5 setup instructions and the `EPIC_GITHUB_TOKEN`
   secret requirement.
5. **Updated `GAME_DESIGN.md`** to reflect "Движок: Unreal Engine 5.3".

### Required owner action

Add one repository secret in **Settings → Secrets and variables → Actions**:

| Secret | Value |
|---|---|
| `EPIC_GITHUB_TOKEN` | GitHub PAT (`read:packages` scope) from an account linked to Epic Games |

Steps to obtain:
1. Link your GitHub account at <https://www.unrealengine.com/en-US/ue-on-github>.
2. Create a GitHub PAT at <https://github.com/settings/tokens> with `read:packages`.
3. Add it as `EPIC_GITHUB_TOKEN` in the repository secrets.

Without this secret, the `checklicense` job logs a warning and the build job is
skipped — CI remains green.

### Validation

The issue is resolved when a workflow run shows **all** of:

1. `Check for Epic Games credentials in GitHub Secrets` logs that credentials are found.
2. `Package Windows Shipping Build (Win64)` runs (not skipped).
3. `BuildCookRun` completes without error.
4. `OneTry-Win64.zip` is created and uploaded as artifact `OneTry-Win64-<run-number>`.
