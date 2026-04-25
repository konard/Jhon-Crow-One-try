# One-try

3D action / roguelite game project built with **Unreal Engine 5.3** (blueprint-only).

See [`GAME_DESIGN.md`](./GAME_DESIGN.md) for the design document and
[`docs/case-studies/issue-19/`](./docs/case-studies/issue-19/) for the
case study explaining the migration back to Unreal Engine.

## Requirements

- [Epic Games Launcher](https://www.unrealengine.com/en-US/download)
- Unreal Engine **5.3** installed via the Epic Games Launcher

## Opening the project

1. Install the Epic Games Launcher and sign in.
2. In the **Library** tab, install Unreal Engine **5.3**.
3. Double-click `OneTry.uproject` — the Launcher will open it in UE5.3.
4. The first open takes a few minutes while shaders compile.

## GitHub Actions — Portable Windows EXE

The workflow [`.github/workflows/build.yml`](./.github/workflows/build.yml)
packages a portable Windows EXE on every push. It uses Epic's official
`ghcr.io/epicgames/unreal-engine` Docker image, runs on a free GitHub-hosted
Linux runner, cross-compiles to `Win64` via `BuildCookRun`, and uploads
the result as a workflow artifact.

### Setup (required once)

The build pulls Epic's private Docker image, which requires a GitHub account
linked to your Epic Games account.

1. Log in at <https://www.unrealengine.com/en-US/ue-on-github> and link
   your GitHub account to your Epic Games account (free).
2. Create a GitHub Personal Access Token (PAT) with `read:packages` scope
   at <https://github.com/settings/tokens>.
3. Add the following secret in **Settings → Secrets and variables → Actions**:
   - `EPIC_GITHUB_TOKEN` — the PAT created in step 2.

Until that secret is set, push and pull-request runs pass the
`Check for Epic Games credentials in GitHub Secrets` preflight but skip the
packaging job, so no portable EXE artifact is uploaded.

### Running the build

- Triggers automatically on push to `main` / `issue-*` branches and on
  PRs targeting `main`. Can also be run manually via **Actions → Build
  Portable Windows EXE → Run workflow**.
- After a successful run, open the run summary and download the artifact
  named `OneTry-Win64-<run-number>`. The artifact contains `OneTry-Win64.zip`;
  extract it and run `WindowsNoEditor/OneTry.exe` — no installation required.
