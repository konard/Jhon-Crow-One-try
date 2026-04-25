# References

## SIGNALIS — art direction

- [Signalis — Wikipedia](https://en.wikipedia.org/wiki/Signalis) — design intent: "replicate the graphics and gameplay of fifth-generation video games", influences from *Silent Hill* and *Resident Evil*.
- [rose-engine — Signalis press kit](https://rose-engine.org/press/sheet.php?p=signalis) — official assets and stylistic statement.
- [In-Depth Review of SIGNALIS — Oreate AI Blog](https://www.oreateai.com/blog/indepth-review-of-the-game-signalis-the-perfect-fusion-of-pixel-art-and-survival-horror/9d8a59e632394f74433b9b89c4be4d82) — analysis of the low-poly + pixel-art rendering.
- [SIGNALIS Reanimating Three Survival Horror Greats — Merry Go Round](https://merrygoroundmagazine.com/signalis-finds-new-life-reanimating-three-survival-horror-greats/) — links the visual language to Silent Hill / Resident Evil / Metal Gear Solid.

## UE5 mannequin & Third Person template

- [Third Person Template in Unreal Engine — Epic Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/third-person-template-in-unreal-engine)
- [Mannequins Asset Pack — Fab](https://www.fab.com/listings/ad542ee6-34d0-4828-a56c-13846cd649d0) — Manny/Quinn assets as a stand-alone download.
- [How can I import a UE5 Mannequin into a Blank project? — Epic Forums](https://forums.unrealengine.com/t/how-can-i-import-a-ue5-mannequin-into-a-blank-project-ue5-0/654283) — confirms assets live in `Templates/TemplateResources/.../Characters/Mannequins/` inside the engine install.
- [How to get the full version of Manny/Quinn's Skeleton in 5.6 — Epic Forums](https://forums.unrealengine.com/t/how-to-get-the-full-version-of-manny-quinn-s-skeleton-in-5-6-instead-of-skm-manny-simple/2580712) — `SKM_Manny_Simple` / `SKM_Quinn_Simple` are lower-poly variants on the same skeleton.
- [UE Bone Structure and UE Mannequin — Blender-For-UnrealEngine-Addons wiki](https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/UE-Bone-Structure-and-UE-Mannequin) — full bone list (clavicle, upperarm, lowerarm, hand; thigh, calf, foot, ball) — proves multi-part requirement is satisfied.
- [Skeleton Hierarchy & Bone Structure — Mocaponline](https://mocaponline.com/blogs/mocap-news/skeleton-hierarchy-animation-guide) — confirms the standard humanoid bone chain expected by R3.

## Headless editor automation

- [Scripting the Unreal Editor Using Python — Epic Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python)
- [Run Headless Unreal Editor with Python Script — Epic Dev Community snippet](https://dev.epicgames.com/community/snippets/J5R1/unreal-engine-run-headless-unreal-editor-with-python-script)
- [Unreal Python Command Line: 3 Easy Methods — xingyulei.com](https://www.xingyulei.com/post/ue-commandline-python/index.html)
- [Migrating from one project to another using python — Epic Forums](https://forums.unrealengine.com/t/migrating-from-one-project-to-another-using-python/2598939)

## Containerised UE builds (already used by this repo's CI)

- [Official Container Images — Unreal Containers](https://unrealcontainers.com/docs/obtaining-images/official-images)
- [Quick-Start Guide for Using Container Images — Epic Documentation](https://docs.unrealengine.com/5.0/en-US/quick-start-guide-for-using-container-images-in-unreal-engine/)

## Alternative pre-built characters / libraries (considered, not used)

- [Mixamo](https://www.mixamo.com/) — free auto-rigged characters + animations; viable SIGNALIS-style replacement, but requires retargeting onto the Manny/Quinn skeleton (extra step now, deferred to a future PR).
- [MetaHuman Creator](https://www.unrealengine.com/en-US/metahuman) — opposite direction: photoreal, high-poly. Wrong silhouette for SIGNALIS; rejected.
- [Lyra Starter Game](https://dev.epicgames.com/documentation/en-us/unreal-engine/lyra-sample-game-in-unreal-engine) — has 300+ animations on the Manny/Quinn skeleton; great future source for combat animations, overkill for "idle only".
