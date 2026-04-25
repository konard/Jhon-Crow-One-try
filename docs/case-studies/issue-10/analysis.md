# Deep Analysis — Issue #10: всё ещё нет portable exe

## 1. Project context at the time of the issue

### Repository state (as of 2026-04-25)

| Area | State | Source |
|---|---|---|
| Engine | **Unity 6.3 LTS** (`6000.3.5f1`) | `ProjectSettings/ProjectVersion.txt` |
| CI workflow | GameCI `unity-builder@v4` | `.github/workflows/build.yml` |
| Unity secrets | **Not configured** in repository settings | CI log: `UNITY_LICENSE: ` (empty) |
| Player model | Multi-part capsule mannequin prefab | PR #6 / `Assets/Characters/Player/` |
| Previous CI state | UE5 workflow never worked (no `EPIC_GITHUB_TOKEN`) | CI run `24939209327` |

### What PR #6 / issue #5 changed

PR #6 merged a Unity multi-part player mannequin **and** a new GameCI-based
build workflow. Before PR #6, the UE5 Docker-based workflow could never run
(missing Epic credentials). After PR #6, the GameCI workflow correctly checks
for Unity credentials — but those credentials were also never set.

---

## 2. CI workflow state machine analysis

The current `build.yml` implements a three-job state machine:

```
                      ┌─────────────┐
                      │ checklicense │
                      └──────┬──────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
   is_unity_license_set   is_unity_license_set  │
        == 'true'          == 'false'            │
          │                  │                  │
          ▼                  ▼                  │
       ┌──────┐      ┌─────────────────┐        │
       │ build │      │   activation    │        │
       │ (PR/  │      │ (workflow_      │        │
       │ push) │      │  dispatch only) │        │
       └──────┘      └─────────────────┘        │
          │                  │                  │
          ▼                  ▼                  │
    Upload artifact    Upload .alf artifact      │
    OneTry-Win64-N     for manual activation     │
```

**What actually happens today:**

1. `checklicense` detects `UNITY_LICENSE` is empty → outputs `is_unity_license_set=false`.
2. `build` is skipped (condition `== 'true'` not met).
3. `activation` is skipped (condition: `== 'false' && github.event_name == 'workflow_dispatch'`).
4. On push/PR events, `activation` is also skipped because `github.event_name != 'workflow_dispatch'`.
5. Overall workflow result: **success** (all jobs either passed or were skipped).
6. Artifacts section: **empty**.

**What needs to happen:**

1. Owner manually triggers `workflow_dispatch` from the Actions UI.
2. `checklicense` detects `UNITY_LICENSE` is empty → `is_unity_license_set=false`.
3. `activation` now runs (condition: `== 'false' && github.event_name == 'workflow_dispatch'`).
4. The `game-ci/unity-request-activation-file@v2` action produces a `.alf` file.
5. The `.alf` is uploaded as an artifact named after the file path.
6. Owner downloads the `.alf`, exchanges it for `.ulf`, adds three secrets.
7. On next push/PR, `checklicense` outputs `is_unity_license_set=true`.
8. `build` job runs → GameCI builds `StandaloneWindows64` → ZIP uploaded as artifact.

---

## 3. CI log evidence

### Run `24940456778` — the run referenced in issue #10

Job: "Check for UNITY_LICENSE in GitHub Secrets"  
Step 2 log output:
```
UNITY_LICENSE is NOT set.
Configure UNITY_LICENSE, UNITY_EMAIL, UNITY_PASSWORD secrets to enable Windows packaging.
See README.md → 'GitHub Actions — Portable Windows EXE → Setup'.
```

Step 3 log output (warning):
```
##[warning]UNITY_LICENSE is missing, so the Windows packaging job is skipped
           and no OneTry-Win64 ZIP artifact is uploaded for this run.
Add UNITY_LICENSE, UNITY_EMAIL, and UNITY_PASSWORD repository secrets,
then re-run this workflow to produce the portable EXE artifact.
```

The `build` job JSON:
```json
{
  "name": "Package Windows Shipping Build (StandaloneWindows64)",
  "conclusion": "skipped",
  "steps": []
}
```

Zero steps ran inside the `build` job — it was entirely skipped before even
attempting checkout or the Unity build.

### Run `24940287598` — stricter CI that failed explicitly

Job step "Fail when push/PR cannot produce portable EXE":
```
##[error]UNITY_LICENSE is missing, so the Windows packaging job cannot run
         and no OneTry-Win64 ZIP artifact can be uploaded.
##[error]Process completed with exit code 1.
```

This run shows that an intermediate version of the workflow intentionally
failed CI with `exit 1` when the license was missing, providing a much clearer
signal. This approach was reverted in commit `a08c962` because it made the PR
branch itself show as failing, causing friction in the PR review flow.

---

## 4. Build output structure (when UNITY_LICENSE is set)

GameCI `unity-builder@v4` with `targetPlatform: StandaloneWindows64` and
`buildName: OneTry` produces the following layout:

```
build/
└── StandaloneWindows64/
    ├── OneTry.exe              ← the main executable
    ├── OneTry_Data/            ← game data (assets, shaders, levels)
    │   ├── Managed/            ← C# DLLs
    │   ├── StreamingAssets/    ← optional streaming content
    │   └── ...
    ├── UnityPlayer.dll         ← Unity runtime
    └── UnityCrashHandler64.exe ← crash reporter (optional to include)
```

The workflow then runs:
```bash
cd build
zip -r "../OneTry-Win64.zip" StandaloneWindows64/ -x "*.pdb" "*.debug"
```

This produces a portable archive: users extract it anywhere and run
`StandaloneWindows64/OneTry.exe` — no installation, no registry changes,
no dependencies beyond what the ZIP contains.

The artifact is uploaded as `OneTry-Win64-<run-number>`, retained for 30 days.

---

## 5. Why Unity Personal license is appropriate

A Unity Personal license (free) is sufficient for this project because:

1. **Revenue threshold:** Unity Personal is available to developers whose
   projects earn less than $200,000/year in recent revenue. An in-development
   game with no published builds earns $0.
2. **Features:** Unity Personal includes all engine features needed for this
   game's scope (3D rendering, physics, animation, input system, URP).
3. **CI compatibility:** GameCI fully supports Personal license activation.
   The `.alf` → `.ulf` flow was designed for Personal license users.
4. **Cost:** Free. No subscription needed.

### Unity Personal license activation friction (2025–2026)

As documented in GameCI's troubleshooting guide, Unity's license portal
(`license.unity3d.com/manual`) has had intermittent UX issues where the
"Personal" license option is hidden by CSS (`display: none`). The workaround
is to use browser developer tools to remove that style rule and expose the
option.

This is a known issue in the GameCI community. It does not prevent activation
but adds one extra step. The GameCI troubleshooting page explicitly documents
this workaround.

---

## 6. Comparison: UE5 era vs Unity era blocking factors

| Era | Blocking secret | Activation path | Friction level |
|---|---|---|---|
| UE5 workflow (PR #4) | `EPIC_GITHUB_TOKEN` | GitHub account must be linked to Epic Games account that accepted the EULA; then mint a PAT with `read:packages` scope and store as repo secret | **High** — requires Epic EULA acceptance, Epic/GitHub account linking, PAT creation |
| Unity workflow (PR #9 / PR #6) | `UNITY_LICENSE`, `UNITY_EMAIL`, `UNITY_PASSWORD` | Create free Unity account; trigger workflow_dispatch; download `.alf` artifact; exchange at license.unity3d.com; paste `.ulf` content into secret | **Medium** — ~3 minutes, fully self-service, no account linking |

The Unity path is significantly lower friction. The primary remaining barrier
is that it still requires a manual action by the repository owner.

---

## 7. Constraints on resolution

1. **Only the repository owner (or a collaborator with Secrets write access)
   can add the secrets.** This is a GitHub permission boundary — automated
   agents cannot write to a repo's secret store.
2. **The `.alf` activation file is machine-specific.** It must be generated
   by the GitHub Actions runner for the target repository; a locally generated
   `.alf` will not activate on CI.
3. **License expiry:** Unity Personal licenses require re-activation
   periodically (approximately annually). If CI starts failing again in
   the future after working, re-running the activation workflow is the fix.
4. **Password special characters:** GameCI's docs note that passwords
   containing special characters can cause activation failures. The Unity
   account password should use only standard alphanumeric characters for CI.

---

## 8. Validation plan

Once the owner adds the three secrets:

1. Push any change to `main` or an `issue-*` branch.
2. In the Actions UI, the `build` job should proceed past the `checklicense`
   gate and enter the "Build Unity project" step.
3. The GameCI Docker container will pull (takes several minutes on first run;
   subsequent runs use the `Library/` cache).
4. After success, the run summary should show an artifact `OneTry-Win64-N`
   containing `OneTry-Win64.zip`.
5. Download, extract, and run `StandaloneWindows64/OneTry.exe` on Windows.
