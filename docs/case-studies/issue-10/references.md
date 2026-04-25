# References — Issue #10

All sources consulted during this case study analysis.

## GitHub CI runs (Jhon-Crow/One-try)

| Run ID | Date (UTC) | Branch | Result | Notes |
|---|---|---|---|---|
| [24940456778](https://github.com/Jhon-Crow/One-try/actions/runs/24940456778) | 2026-04-25T20:54:42Z | `main` | success (build skipped) | **Referenced in issue #10**; merge of PR #6 |
| [24940562683](https://github.com/Jhon-Crow/One-try/actions/runs/24940562683) | 2026-04-25T21:00:19Z | `issue-10-1eb4c57c516b` | success (build skipped) | First run for PR #11 |
| [24940369167](https://github.com/Jhon-Crow/One-try/actions/runs/24940369167) | 2026-04-25T20:50:07Z | `issue-5-d34229c636e3` | success (build skipped) | Final passing state of PR #6 |
| [24940360613](https://github.com/Jhon-Crow/One-try/actions/runs/24940360613) | 2026-04-25T20:49:40Z | `issue-5-d34229c636e3` | success (build skipped) | After reverting exit-1 |
| [24940287598](https://github.com/Jhon-Crow/One-try/actions/runs/24940287598) | 2026-04-25T20:45:44Z | `issue-5-d34229c636e3` | **failure** | exit 1 on missing license |
| [24940279147](https://github.com/Jhon-Crow/One-try/actions/runs/24940279147) | 2026-04-25T20:45:13Z | `issue-5-d34229c636e3` | **failure** | Same |
| [24940272298](https://github.com/Jhon-Crow/One-try/actions/runs/24940272298) | 2026-04-25T20:44:54Z | `issue-5-d34229c636e3` | **failure** | Same |
| [24940263350](https://github.com/Jhon-Crow/One-try/actions/runs/24940263350) | 2026-04-25T20:44:29Z | `issue-5-d34229c636e3` | **failure** | Same |
| [24940250715](https://github.com/Jhon-Crow/One-try/actions/runs/24940250715) | 2026-04-25T20:43:46Z | `issue-5-d34229c636e3` | **failure** | First exit-1 attempt |
| [24939754725](https://github.com/Jhon-Crow/One-try/actions/runs/24939754725) | 2026-04-25T20:17:54Z | `issue-8-02cf259d291f` | success (build skipped) | First GameCI workflow run after Unity migration |
| [24939711653](https://github.com/Jhon-Crow/One-try/actions/runs/24939711653) | 2026-04-25T20:15:36Z | `issue-8-02cf259d291f` | **failure** | Old workflow `.github/workflows/build.yml` name mismatch |
| [24939480705](https://github.com/Jhon-Crow/One-try/actions/runs/24939480705) | 2026-04-25T20:03:18Z | `issue-5-d34229c636e3` | **failure** | UE5 Docker credential error |
| [24939209327](https://github.com/Jhon-Crow/One-try/actions/runs/24939209327) | 2026-04-25T19:49:12Z | `main` | **failure** | First ever CI run; UE5 Docker pull fails |

## Repository data

| Item | URL |
|---|---|
| Issue #10 | https://github.com/Jhon-Crow/One-try/issues/10 |
| PR #11 (issue #10 branch) | https://github.com/Jhon-Crow/One-try/pull/11 |
| PR #6 (issue #5 — player mannequin + Unity workflow) | https://github.com/Jhon-Crow/One-try/pull/6 |
| PR #9 (issue #8 — Unity migration) | https://github.com/Jhon-Crow/One-try/pull/9 |
| Current `build.yml` | `.github/workflows/build.yml` (this repo) |
| `GAME_DESIGN.md` | `GAME_DESIGN.md` (this repo) |

## GameCI documentation

| Title | URL |
|---|---|
| GameCI — Builder reference | https://game.ci/docs/github/builder/ |
| GameCI — Activation (personal license) | https://game.ci/docs/2/github/activation/ |
| GameCI — Troubleshooting common issues | https://game.ci/docs/troubleshooting/common-issues/ |
| GameCI `unity-builder` GitHub repository | https://github.com/game-ci/unity-builder |
| GameCI `unity-request-activation-file` action | https://github.com/marketplace/actions/unity-request-activation-file |
| GameCI `unity-actions-example` repository | https://github.com/game-ci/unity-actions-example |
| GameCI — Artifacts build folder issue #224 | https://github.com/game-ci/unity-builder/issues/224 |
| GameCI — License activation failure issue #597 | https://github.com/game-ci/unity-builder/issues/597 |

## Unity documentation

| Title | URL |
|---|---|
| Unity 6.3 LTS announcement | https://unity.com/blog/unity-6-3-lts-is-now-available |
| Unity 6 release & support matrix | https://unity.com/releases/unity-6-releases |
| Unity Manual — Manage license via CLI | https://docs.unity3d.com/6000.3/Documentation/Manual/ManagingYourUnityLicense.html |
| Unity Manual — License troubleshooting | https://docs.unity3d.com/Manual/ActivationFAQ.html |
| Unity license portal (manual activation) | https://license.unity3d.com/manual |

## GitHub Actions documentation

| Title | URL |
|---|---|
| `actions/upload-artifact@v4` | https://github.com/actions/upload-artifact |
| GitHub Actions — Non-zipped artifacts (Feb 2026) | https://github.blog/changelog/2026-02-26-github-actions-now-supports-uploading-and-downloading-non-zipped-artifacts/ |
| Unity Builder on GitHub Marketplace | https://github.com/marketplace/actions/unity-builder |

## Community resources

| Title | URL |
|---|---|
| "GameCI 1: Intro to GitHub Actions for Unity" — David Finol | https://davidmfinol.medium.com/gameci-1-intro-to-github-actions-for-unity-4e48e6491eef |
| "Automating Unity Builds with GitHub Actions" — DEV Community | https://dev.to/virtualmaker/automating-unity-builds-with-github-actions-1inf |
| "Setting up a CI/CD build pipeline for Unity using GitHub Actions" — Anchorpoint | https://www.anchorpoint.app/blog/setting-up-a-ci-cd-build-pipeline-for-unity-using-github-actions |
| "Building Unity with GitHub Actions" — Isaac Broyles | https://isaacbroyles.com/gamedev/2020/07/04/unity-github-actions.html |
| "GitHub Actions Unity Builder license activation fails" — Unity Discussions | https://discussions.unity.com/t/github-actions-unity-builder-license-activation-fails/816239 |

## Related case studies (this repository)

| Issue | Location | Summary |
|---|---|---|
| Issue #5 (player model) | `docs/case-studies/issue-5/` | Root cause of engine drift (UE5 vs Unity); details the checklicense design rationale and the Unity workflow introduction. |
| Issue #8 (Unity migration) | `docs/case-studies/issue-8/` | Deep analysis of the UE5 → Unity migration; includes comparison of `EPIC_GITHUB_TOKEN` vs `UNITY_LICENSE` activation paths. |
