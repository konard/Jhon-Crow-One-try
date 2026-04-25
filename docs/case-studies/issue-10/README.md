# Case study — Issue #10: всё ещё нет portable exe

This folder collects all logs, data, and analysis for issue #10, which reports
that the portable Windows EXE is **still** not being produced by GitHub Actions.

| File | Purpose |
|---|---|
| [issue.md](./issue.md) | Original issue text, requirements table, scope. |
| [timeline.md](./timeline.md) | Reconstructed sequence of events across issues #1 → #5 → #8 → #10. |
| [root-cause.md](./root-cause.md) | Five-whys analysis: why there is still no portable EXE artifact despite the Unity migration in PR #9. |
| [analysis.md](./analysis.md) | Deep technical analysis: CI behavior, license-gate design, workflow state machine, build output structure. |
| [proposed-solutions.md](./proposed-solutions.md) | Comparison of options and the selected solution with step-by-step implementation plan. |
| [references.md](./references.md) | All consulted sources (GameCI docs, GitHub Actions docs, Unity license docs, community reports). |
| [raw/](./raw/) | Raw data: issue JSON, PR JSON, CI run list, log snapshots, workflow snapshot. |

## TL;DR

Issue #10 ("всё ещё нет portable exe" — "still no portable exe") was filed
after PR #6 merged, which introduced the GameCI-based Unity build pipeline.
The owner observed that the CI workflow runs were **green** yet **produced no
downloadable artifact**.

### Root cause (short version)

The `checklicense` job detects that `UNITY_LICENSE` is absent from the
repository secrets. It sets `is_unity_license_set=false`, which causes the
`build` job to be **skipped** (not failed). GitHub Actions marks skipped jobs
as neutral (grey), so the overall workflow run shows green. No build ever
ran → no ZIP artifact was ever uploaded.

This is a **configuration gap**, not a code bug: the three Unity secrets
(`UNITY_LICENSE`, `UNITY_EMAIL`, `UNITY_PASSWORD`) have never been added to
the repository's **Settings → Secrets and variables → Actions** page.

### Resolution path

The owner must complete the one-time manual activation sequence (described in
detail in [proposed-solutions.md](./proposed-solutions.md) and in the
repository's `README.md`):

1. Trigger the workflow manually (Actions → Run workflow) without any secrets
   set — the `activation` job produces a `.alf` file as a download artifact.
2. Upload the `.alf` to <https://license.unity3d.com/manual> to exchange it
   for a `.ulf` license file.
3. Add `UNITY_LICENSE` (full content of the `.ulf`), `UNITY_EMAIL`, and
   `UNITY_PASSWORD` as repository secrets.
4. Re-run the workflow. The `build` job will now execute and upload
   `OneTry-Win64-<run-number>` containing `OneTry-Win64.zip` →
   `StandaloneWindows64/OneTry.exe`.

The workflow code itself is correct and complete — no changes to
`.github/workflows/build.yml` are required. This is a secrets-configuration
task only.
