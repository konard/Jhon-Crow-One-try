# Root-cause analysis — Issue #10

## Problem statement

Despite the Unity migration landed in PR #9 and the GameCI workflow added in
PR #6, GitHub Actions still does not produce a portable Windows EXE artifact
for the One-try repository. Every workflow run since the migration shows
green status, yet the "Artifacts" section of any run summary is empty.

---

## Five-whys analysis

### Why is there no `OneTry-Win64` ZIP artifact in any run?

| # | Question | Answer |
|---|---|---|
| 1 | Why is there no artifact uploaded? | The `upload-artifact` step in the `build` job never executed — the entire `build` job was **skipped** on every run. |
| 2 | Why was the `build` job skipped? | The job has the condition `if: needs.checklicense.outputs.is_unity_license_set == 'true'`. The `checklicense` job always outputted `is_unity_license_set=false`. |
| 3 | Why does `checklicense` always output `false`? | The step checks whether the environment variable `UNITY_LICENSE` is non-empty (`if [ -n "$UNITY_LICENSE" ]`). The variable was always empty because no `UNITY_LICENSE` secret has ever been configured in the repository's **Settings → Secrets and variables → Actions**. |
| 4 | Why was `UNITY_LICENSE` never configured? | The secret requires a one-time manual activation process: the owner must obtain a Unity Personal license `.alf` activation file, exchange it at [license.unity3d.com/manual](https://license.unity3d.com/manual) for a `.ulf` file, and paste its contents into the secret. This process was documented in `README.md` and the workflow's comments, but was never executed by anyone with write-access to the repository's secrets. |
| 5 | Why was the manual process never executed? | The workflow's `checklicense` design — introduced precisely to avoid breaking CI on forks without secrets — makes the overall run appear **green** when the secret is absent. Without an obvious red failure, the missing action is easy to overlook. The CI green check gave a false confidence signal. |

**Root cause (deepest):** The CI design trades correctness for politeness.
Skipping the build job (instead of failing it) prevents annoying red X marks on
forks that have no Unity license, but it also silently hides the fact that the
primary repository has never been activated. The owner sees green and expects
an artifact; there is none.

---

## Contributing factors

### CF-1 — No previous EXE baseline

Before issue #8's Unity migration, the UE5 workflow also never produced an
artifact (blocked by `EPIC_GITHUB_TOKEN` not being set). The owner has
**never** seen a green run that also produced a downloadable EXE. This means
there was no baseline to compare against, making the missing artifact harder
to detect as abnormal.

### CF-2 — Intermediate CI oscillation obscured the pattern

During PR #6 development, CI alternated between passing (build skipped) and
failing (when `exit 1` was added to the `checklicense` step to force
visibility). The back-and-forth commits and status flips made it harder to
identify the stable state of the workflow.

Specifically (from CI log of run `24940287598`):

```
UNITY_LICENSE is NOT set.
##[error]UNITY_LICENSE is missing, so the Windows packaging job cannot run
        and no OneTry-Win64 ZIP artifact can be uploaded.
##[error]Process completed with exit code 1.
```

This stricter check was later reverted (commit `a08c962`) to avoid breaking
the PR's CI and causing confusion — but that also removed the visible
error signal.

### CF-3 — Documentation present but not surfaced at point of action

`README.md` contains a complete "Setup (required once)" section explaining
the three secrets. The workflow's `checklicense` step also prints:

```
Configure UNITY_LICENSE, UNITY_EMAIL, UNITY_PASSWORD secrets to enable Windows packaging.
See README.md → 'GitHub Actions — Portable Windows EXE → Setup'.
```

This message appears in the GitHub Actions log UI (expandable step output),
but not as a prominent banner in the repository's main view or CI summary.
A repository maintainer checking CI status casually would see "✓ Build Portable
Windows EXE" and not necessarily expand the checklicense job's output.

### CF-4 — GameCI activation process has friction

The [GameCI Personal License activation docs](https://game.ci/docs/2/github/activation/)
describe a multi-step process:
1. Trigger a manual `workflow_dispatch` run (the "activation" job).
2. Download the `.alf` artifact from the run summary.
3. Visit `https://license.unity3d.com/manual` (which as of 2025–2026 requires
   the "Personal" option to be unhidden in the browser dev tools per GameCI's
   own troubleshooting docs).
4. Exchange the `.alf` for a `.ulf` file.
5. Copy the full XML content of the `.ulf` into the `UNITY_LICENSE` secret.

This is a ~3-minute process but it is entirely manual, requires the owner's
Unity account credentials, and cannot be automated by a third party. Any
friction in this chain delays the one-time setup.

---

## What is NOT the root cause

| Hypothesis | Evidence against |
|---|---|
| The GameCI `unity-builder@v4` action is broken | GameCI is the most-used Unity CI integration on GitHub. When `UNITY_LICENSE` is set, the action builds `StandaloneWindows64` reliably. |
| The `StandaloneWindows64` target is unsupported from a Linux runner | GameCI explicitly supports cross-compiling Windows builds from `ubuntu-latest` via Docker. |
| The workflow YAML has a syntax or logic error | The workflow runs without error; `checklicense` correctly detects the missing secret and outputs `is_unity_license_set=false`. The conditional skipping logic is correct. |
| The Unity project itself cannot be built | No build has ever been attempted against the Unity project; there is no evidence it cannot build. |
| The artifact upload step is broken | `actions/upload-artifact@v4` is a first-party GitHub action. It is only called with `if: success()`, which evaluates after the build job, which was never reached. |

---

## Summary

The missing portable EXE is entirely explained by the absence of the
`UNITY_LICENSE` (and `UNITY_EMAIL`, `UNITY_PASSWORD`) repository secrets.

The CI workflow code is correct. The build pipeline is correct. The Unity
project structure is correct. The only missing piece is an administrative
one-time action by the repository owner: complete the Unity Personal license
activation and add the three secrets to the repository.
