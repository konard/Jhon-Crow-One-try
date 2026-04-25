# Proposed solutions — Issue #10

## Overview

The problem is not in the code — the workflow and Unity project are correct.
The problem is a missing one-time configuration step. All proposed solutions
address this gap.

---

## Option comparison

| # | Option | Effort | Risk | Outcome |
|---|---|---|---|---|
| **A** | **Complete Unity Personal license activation (recommended)** | ~5 min, one-time | Low | Portable EXE produced on every push |
| B | Fail CI explicitly when secrets missing | 5 min code change | Low | No EXE, but CI is visibly red as a reminder |
| C | Add CI status badge + warning comment to README | 5 min | Low | No EXE, but missing setup is more visible |
| D | Switch to Unity Pro (paid) | Ongoing cost | Medium | EXE via serial-based activation; same workflow |
| E | Switch to self-hosted Windows runner | High setup | High | Avoids license issue, but requires maintained Windows machine |
| F | Switch to another CI provider (e.g. CircleCI, Buildkite) | High | Medium | Same fundamental problem: Unity license still needed |

---

## Option A — Complete Unity Personal license activation (selected)

This is the only option that actually produces the portable EXE artifact. All
other options are workarounds that either improve visibility or change tooling
without resolving the underlying secret gap.

### Step-by-step process

#### Step 1 — Trigger the activation workflow

1. Go to the repository's **Actions** tab:
   `https://github.com/Jhon-Crow/One-try/actions/workflows/build.yml`
2. Click **"Run workflow"** → select `main` branch → click the green
   **"Run workflow"** button.
3. Wait for the run to complete (~30 seconds).
4. Open the run summary. The `activation` job should have run (because
   `workflow_dispatch` was used and `UNITY_LICENSE` is not yet set).
5. Download the artifact whose name ends in `.alf`
   (e.g. `Unity_v6000.3.5f1.alf`).

#### Step 2 — Exchange .alf for .ulf

1. Navigate to `https://license.unity3d.com/manual`.
2. Log in with your Unity account (create one free at `https://id.unity.com`
   if you don't have one).
3. Upload the `.alf` file.
4. **Known issue (2025–2026):** The "Personal" license option may be hidden
   by CSS. If you see no license type options:
   - Open browser dev tools (F12).
   - Find the element with `style="display: none;"` that wraps the Personal
     option and remove the `display: none` style.
   - The Personal option becomes clickable.
5. Select **Personal** and complete the form.
6. Download the resulting `.ulf` file (a few-KB XML file).

#### Step 3 — Add repository secrets

Go to **Settings → Secrets and variables → Actions → New repository secret**
and add all three:

| Secret name | Value |
|---|---|
| `UNITY_LICENSE` | Entire content of the `.ulf` XML file (copy-paste all text including the XML header) |
| `UNITY_EMAIL` | Your Unity account email address |
| `UNITY_PASSWORD` | Your Unity account password |

> **Note on passwords:** GameCI has documented issues with passwords containing
> special characters (e.g. `@`, `!`, `#`). If activation fails, try a
> temporary Unity password with only alphanumeric characters.

#### Step 4 — Trigger a build

Push any commit to `main` (or re-run the workflow manually). The `build` job
will now:
1. Check out the repository.
2. Cache `Library/` (first run downloads; subsequent runs are fast).
3. Build via GameCI → `build/StandaloneWindows64/OneTry.exe` + data folder.
4. Zip to `OneTry-Win64.zip`.
5. Upload as artifact `OneTry-Win64-<run-number>` (30-day retention).

#### Step 5 — Verify

1. In the run summary, open the **Artifacts** section.
2. Download `OneTry-Win64-<run-number>`.
3. Extract the ZIP on a Windows machine.
4. Run `StandaloneWindows64/OneTry.exe` — no installation required.

---

## Option B — Fail CI explicitly when secrets missing

If Option A is not immediately feasible, the workflow can be modified to fail
loudly instead of silently skipping.

In `checklicense`, replace the `Report portable EXE artifact availability`
step with:

```yaml
- name: Fail — portable EXE cannot be produced without UNITY_LICENSE
  if: steps.checklicense_job.outputs.is_unity_license_set == 'false' && github.event_name != 'workflow_dispatch'
  run: |
    echo "::error title=Portable EXE artifact is not available::UNITY_LICENSE is missing."
    echo "Complete the activation steps in README.md to enable Windows builds."
    exit 1
```

**Effect:** Every push/PR CI run fails visibly until the secrets are added.
This was tried in commit `e916857` and reverted because it made PR branches
show red. It is a valid choice if the owner prefers an unmissable red signal
over a misleading green one.

---

## Option C — Improve README callout

Add a prominent callout at the very top of `README.md`:

```markdown
> **⚠️ No portable EXE is produced until three repository secrets are configured.**
> See [GitHub Actions — Setup](#github-actions--portable-windows-exe) below.
```

This does not fix the root cause but reduces the chance of the setup step
being overlooked.

---

## Why Option A is the right choice

1. **Directly resolves the issue**: The owner asked for a portable EXE. Only
   adding the secrets makes one appear.
2. **The workflow code is already correct**: No changes needed to
   `build.yml`, `README.md`, or any project file.
3. **Cost: zero.** Unity Personal is free for non-commercial/small-revenue
   projects.
4. **Time: ~5 minutes**, one-time, never repeated (unless the license expires
   or the repository transfers ownership).
5. **Fully self-service**: The owner can complete it independently without
   any third-party involvement.

---

## Long-term considerations

### License expiry

Unity Personal licenses tied to a `.ulf` file do not expire in the same way
as Unity Pro serial leases, but Unity may require re-activation if:
- The account credentials change.
- The Unity version changes significantly.
- The license service detects unusual usage patterns.

If CI starts failing with license errors in the future, re-run the activation
workflow (`workflow_dispatch`) and repeat steps 1–3.

### Artifact retention

The current workflow retains artifacts for 30 days. For a permanent download
link, consider uploading to a GitHub Release instead of (or in addition to)
the artifact. This requires adding a release-creation step or a separate
`release.yml` workflow — left as a future enhancement.

### Library cache size

GameCI caches `Library/` to speed up subsequent builds. As the project grows
(more assets, more packages), the cache key
`Library-StandaloneWindows64-<hash>` may become stale. The cache is
automatically invalidated when `Packages/manifest.json` or
`ProjectSettings/ProjectVersion.txt` changes.
