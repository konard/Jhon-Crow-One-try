# Timeline / Sequence of events — Issue #10

Reconstructed from `git log --all --oneline`, GitHub CI run history, issue/PR
timestamps, and CI log timestamps. All times are UTC unless noted.

---

## Part 1 — Project bootstrap and the first broken build (before issue #10)

| When (UTC) | Commit / event | Key observation |
|---|---|---|
| 2026-04-20 10:59 | `40ae0aa` — "Initial commit" | Empty repository. |
| 2026-04-20 11:03 | `40a2893` — PR #3: "Add game design document" | `GAME_DESIGN.md` states **Движок: Unity**. This is the canonical engine declaration. |
| 2026-04-20 11:04 | `fd9254a` — PR #4: "Add empty UE5 3D scene + portable EXE build" | First appearance of the CI workflow. Targets Epic's Docker image `ghcr.io/epicgames/unreal-engine:dev-slim-5.3.2`. Requires `EPIC_GITHUB_TOKEN` secret linked to an Epic-Games-org-member GitHub account. **The EXE build could never have worked**: the owner never set `EPIC_GITHUB_TOKEN`. |
| 2026-04-25 19:49 | CI run `24939209327` — push of `babd257` (merge of PR #3) | **Failure** (workflow name: `.github/workflows/build.yml`). First public evidence of the broken CI. The Epic Docker pull fails on credential check. |

## Part 2 — Issue #5 response creates more failing CI iterations

| When (UTC) | Commit / event | Key observation |
|---|---|---|
| 2026-04-25 19:56 | `1efd896` — "Add player mannequin via Python setup script + case study" | First automated agent response to issue #5. Implements Unreal mannequin (wrong engine). CI run `24939480705` **fails** — same Epic Docker credential error. |
| 2026-04-25 20:15 | `695088d` — "docs(case-study): add issue-8 case study" | Issue #8 branch begins Unity migration. CI run `24939711653` **fails** under the old workflow name `.github/workflows/build.yml`. The new Unity workflow has not yet replaced the old UE5 one. |
| 2026-04-25 20:17 | `0247caf` — "ci: replace UE5 Docker build with GameCI Unity Windows build" | **Key transition**: workflow switched from Epic Docker to GameCI `unity-builder@v4`. First `checklicense` job appears. `UNITY_LICENSE` is absent → build job skipped → CI run `24939754725` **succeeds** (with skipped build job). |

## Part 3 — Issue #5 PR development: CI failures caused by stricter workflow

| When (UTC) | Commit / event | CI run | Result | Reason |
|---|---|---|---|---|
| 20:28 | `45ece90` — "feat(player): add multi-part Unity mannequin + idle" | `24939962723` | **success** | `checklicense` pass; build skipped (no secrets). |
| 20:32 | `d71e6e1` — "Revert initial commit" | `24940033514` | **success** | Same: build skipped. |
| 20:34 | `0ef7768` — "docs(case-study): add timeline + root-cause analysis" | `24940070674` | **success** | Same: build skipped. |
| 20:43 | `e916857` — "ci: fail when portable exe artifact cannot be built" | `24940250715` | **failure** | A stricter `checklicense` step added `exit 1` when license is missing, making the overall run **fail** instead of appearing green. This was an attempt to surface the missing license as a hard error. |
| 20:44–20:45 | `26b4f1f`, `d304876`, `7d9ec78`, `bfcd41e` — archive CI logs | `24940263350` `24940272298` `24940279147` `24940287598` | **failure** | Same strict workflow with `exit 1`. |
| 20:49 | `a08c962` — "ci: pass license preflight without unity secrets" | `24940360613` | **success** | Step reverted to warning-only (no `exit 1`). Build skipped again. |
| 20:50 | `5a22edc` — "docs: archive passing license preflight log" | `24940369167` | **success** | Build skipped. |

## Part 4 — PR #6 merges to main; issue #10 is opened

| When (UTC) | Commit / event | Key observation |
|---|---|---|
| 20:54 | `f62c94a` — "Merge pull request #6" (merges issue-5 → main) | CI run `24940456778` on `main`. Workflow passes `checklicense`; build job **skipped** (no secrets). No artifact. **This is the exact run referenced in issue #10**. |
| ~20:54–21:00 | **Issue #10 opened** by @Jhon-Crow | Title: "всё ещё нет portable exe". Owner points to the CI run above and asks for case study + root cause + solutions. |
| 21:00 | `8ee5860` — "Initial commit with task details" (issue-10 branch) | Automated agent starts working on issue #10. PR #11 created as WIP. |
| 21:00 | CI run `24940562683` — PR #11 | **success** (build skipped; no secrets in fork). |

## Visual timeline

```
[2026-04-20] Initial commit → GAME_DESIGN.md says "Движок: Unity"
      │
      ▼
[2026-04-20] PR #4 lands UE5 scaffold + UE5 build.yml
      │         ← EPIC_GITHUB_TOKEN never set → build never works
      ▼
[2026-04-25 19:49] First CI run → FAILURE (Epic Docker pull fails)
      │
      ▼
[2026-04-25 20:17] Issue #8 → PR #9: Unity migration
      │         build.yml → GameCI unity-builder
      │         checklicense job added
      │         UNITY_LICENSE absent → build SKIPPED (CI green)
      ▼
[2026-04-25 20:28-20:50] Issue #5 → PR #6 iterations
      │         Multiple CI runs: some green (build skipped)
      │         Some red (exit 1 added then reverted to force visibility)
      ▼
[2026-04-25 20:54] PR #6 merged to main
      │         CI run 24940456778: checklicense passes, build SKIPPED
      │         ← no artifact uploaded ← ZERO OneTry-Win64 ZIPs ever
      ▼
[2026-04-25 ~21:00] Issue #10 opened: "всё ещё нет portable exe"
      │         Owner points to CI run 24940456778, step 3
      ▼
[2026-04-25 21:00] Issue #10 branch created → PR #11 → THIS CASE STUDY
```

## Key observation: "still" in the title

The word "всё ещё" ("still") in the issue title is significant. It means the
owner noticed that the portable EXE was *already* missing before PR #6, and
PR #6 did not fix it. This aligns with the full CI history:

- Under the UE5 workflow: EXE never built because `EPIC_GITHUB_TOKEN` was missing.
- Under the Unity workflow (after PR #9): EXE never built because `UNITY_LICENSE`,
  `UNITY_EMAIL`, `UNITY_PASSWORD` were missing.

In both eras, the blocking factor was an **unconfigured secret**, not broken
build code. The code was structurally correct each time; the secrets were
simply never added to the repository's Settings.
