# Issue #5 — Player Model

**Source:** https://github.com/Jhon-Crow/One-try/issues/5
**Author:** Jhon-Crow
**Opened:** 2026-04-25

## Original text (RU)

> добавь модельку игрока
>
> простого манекена (без оружия и других вещей)
> моделька должан быть обязательно многосоставной (плечи, предплечья, кисти и такая же детализация ног).
> учти что в будущем нужно будет стилизовать визуал под SIGNALIS
> так же сразу добавь idle анимацию для проверки.
> используй пресеты если необходимо.
>
> Please collect data related about the issue to this repository, make sure we compile that data to `./docs/case-studies/issue-{id}` folder, and use it to do deep case study analysis (also make sure to search online for additional facts and data), and propose possible solutions (including known existing components/libraries, that solve similar problem or can help in solutions).
> и реализуй

## Translation (EN)

> Add a player model.
>
> A simple mannequin (no weapons or other gear).
> The model **must** be multi-part (shoulders, forearms, hands, and the same level of detail for the legs).
> Note that in the future the visuals will need to be styled to match **SIGNALIS**.
> Also, immediately add an **idle animation** for verification.
> Use presets if needed.
>
> Compile related data into `./docs/case-studies/issue-5`, do a deep case-study analysis (also search online for facts and data), propose possible solutions (including known existing components/libraries that solve a similar problem or can help). And implement.

## Hard requirements (extracted)

| # | Requirement | Acceptance criterion |
|---|---|---|
| R1 | Player model exists in the project | A `Character` Blueprint is set as the default pawn of the active GameMode. |
| R2 | Mannequin only — no weapons or gear | The mesh has no attached weapon sockets / props. |
| R3 | Multi-part skeleton | Skeleton exposes separate bones for clavicle, upper-arm, lower-arm, hand, thigh, calf, foot, ball — independently animatable. |
| R4 | Future styling to SIGNALIS | Mesh material and silhouette must be replaceable without re-rigging (clean skeleton, material slots exposed). |
| R5 | Idle animation for verification | Standing in PIE plays a looping idle pose. |
| R6 | Use presets if needed | Reusing the engine's stock mannequin / animation assets is explicitly allowed. |

## Out of scope (this issue)

- SIGNALIS-styled materials / textures (planned as a follow-up).
- Locomotion blendspace, jump, attack animations.
- Networking / multiplayer.
