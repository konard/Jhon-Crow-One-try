# Issue #10 — всё ещё нет portable exe

**URL:** https://github.com/Jhon-Crow/One-try/issues/10  
**Author:** @Jhon-Crow  
**State:** OPEN  
**Filed:** 2026-04-25  

## Original text (Russian)

**Title:** всё ещё нет portable exe

**Body:**

> https://github.com/Jhon-Crow/One-try/actions/runs/24940456778/job/73033205019#step:3:8
>
> Please download all logs and data related about the issue to this repository,
> make sure we compile that data to `./docs/case-studies/issue-{id}` folder,
> and use it to do deep case study analysis (also make sure to search online
> for additional facts and data), in which we will reconstruct
> timeline/sequence of events, find root causes of the problem, and propose
> possible solutions.

## Translation / summary

"Still no portable exe" — the owner points to a specific CI job step URL that
shows the `Check for UNITY_LICENSE in GitHub Secrets` job running and
reporting that `UNITY_LICENSE` is not set. The packaging job is therefore
skipped and no `OneTry-Win64` ZIP artifact is uploaded. The owner requests a
deep case study: download the CI logs, reconstruct the full timeline,
find root causes, and propose solutions.

## Referenced CI run

| Field | Value |
|---|---|
| Run ID | 24940456778 |
| Workflow | Build Portable Windows EXE |
| Trigger | push to `main` (merge of PR #6) |
| Timestamp | 2026-04-25T20:54:42Z |
| Result | **success** (but the `build` job was skipped — no artifact) |
| Job pointed to | `73033205019` — "Check for UNITY_LICENSE in GitHub Secrets" |
| Step pointed to | step 3: "Report portable EXE artifact availability" |

## Explicit requirements from the issue

| # | Requirement |
|---|---|
| R1 | Download all CI logs and data related to the issue into this repository. |
| R2 | Compile data to `./docs/case-studies/issue-10/`. |
| R3 | Produce a deep case study: reconstruct timeline/sequence of events. |
| R4 | Identify root causes. |
| R5 | Search online for additional facts and data. |
| R6 | Propose possible solutions. |

## Out of scope

- Implementing new gameplay features.
- Changing the game design or project structure.
- Buying Unity Pro or switching CI providers.
- Any changes that require Unity Editor to be installed locally.
