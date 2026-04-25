# Case study — Issue #5: добавь модельку игрока

This folder collects the research and design rationale behind the player-model implementation.

| File | Purpose |
|---|---|
| [issue.md](./issue.md) | Original issue text (RU + EN translation), explicit requirements table, out-of-scope list. |
| [analysis.md](./analysis.md) | Project context, why we reuse Epic's Manny/Quinn mannequin, SIGNALIS aesthetic notes, build-environment constraints, validation plan, risks. |
| [proposed-solutions.md](./proposed-solutions.md) | Comparison of 5 approaches and the selected solution. |
| [references.md](./references.md) | All consulted sources (SIGNALIS press kit, UE5 docs, mannequin asset references, headless-editor automation guides). |

## TL;DR

We add a multi-part player mannequin (`SKM_Quinn_Simple`, 89-bone Manny/Quinn skeleton) with the stock `MF_Idle` animation, wrapped in `BP_PlayerCharacter` and a `BP_PlayerGameMode` that sets it as the default pawn. The mannequin is *not* committed as binary `.uasset` files — instead a single Python editor script (`Tools/Setup_PlayerMannequin.py`) materialises it on first open, keeping the PR diff text-only and reviewable. Skeleton and animations are preserved so a future SIGNALIS-styled mesh can be swapped in without touching the Blueprint or animation graph.
