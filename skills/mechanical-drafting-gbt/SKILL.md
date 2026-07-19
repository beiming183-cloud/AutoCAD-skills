---
name: mechanical-drafting-gbt
description: Create, revise, audit, validate, and present mechanical CAD using Chinese GB/T drafting conventions. Use for AutoCAD/AutoCAD MCP; parametric 2D/3D parts, complex assemblies, mechanisms, engines, gears, machined parts, consumer products, enclosures, and powered appliances; DXF/DWG/PDF/STEP and model-based definition workflows; assembly/detail drawings and cross-view verification; product concept gates, purchased-component envelopes, mains/moving-part safety architecture, ergonomics, cable management, stability, dimensions, fits, GD&T/GPS, inspection planning, BOMs, revisions, CAD DRC/DFM, engineering-analysis evidence, and release compliance.
---

# GB/T Mechanical Drafting

Chinese maintenance mirror: [`SKILL.zh-CN.md`](SKILL.zh-CN.md).

Create readable manufacturing drawings, not decorative CAD illustrations. Treat geometry, line hierarchy, view layout, dimensions, and notes as one system.

## Portability Contract

- Keep the core workflow agent- and vendor-neutral. Apply it in Codex, Claude Code, or another compatible skill runner without changing the engineering acceptance criteria.
- Treat `SKILL.md` and `references/` as the authoritative instructions. Ignore optional runtime-specific metadata, such as `agents/openai.yaml`, when the current runner does not use it.
- Discover the available CAD application, MCP/automation bridge, shell, parsers, and renderers before execution. Map capability-level steps to exposed safe tools instead of assuming a particular tool namespace or exact operation name.
- Treat operation names and JSON payloads in the references as interface examples unless the active bridge explicitly exposes them. Never invent a tool call or claim a check ran when only an example schema exists.
- Keep deliverables and validation evidence in standard CAD/exchange/report artifacts so another agent or application can reopen and independently verify them.

### Tool Inventory Preflight

Before installing, downloading, upgrading, patching, removing, or relocating any tool, dependency, browser runtime, plug-in, CAD backend, renderer, or validator:

1. Read `D:\Codex\TOOLS-INVENTORY.md`.
2. Check its recorded path, version, and verification command. Reuse the existing environment when verification passes; a different task or window is not a reason to reinstall it.
3. Install or repair only when the entry is absent, its path is missing, or verification fails.
4. After any change, update the inventory with the date, exact path, version, purpose, verification result, and known limitations.
5. Never store credentials, tokens, license keys, or other secrets in the inventory.

## Required Workflow

1. Classify the task and load only the required references: always read `references/gbt-drafting.md` for engineering drawings; read `references/autocad-mcp-workflow.md` for AutoCAD/MCP execution, `references/complex-assembly-drafting.md` for engines or other multi-system assembly drawings, `references/consumer-product-concept.md` for new/substantially redesigned consumer products, enclosures, appliances, ports/cables/controls, moving parts, or mains-powered products, `references/cad-workflows.md` for 2D/3D conversion or presentation, `references/cad-3d-modeling.md` for 3D parts/assemblies, `references/gps-inspection.md` for GD&T/GPS, tolerance-stack, or inspection work, `references/product-definition-release.md` for configurations, BOMs, revisions, MBD/PMI, dependencies, or release packages, `references/engineering-analysis.md` for any physical-performance calculation or simulation claim, and `references/drc-review.md` for every DRC, DFM, fit, interference, or release review.
2. For a new or substantially redesigned consumer product, pass the applicable concept, purchased-component, mains/moving-part safety, early-preview, and product-design gates before detailed dimensions or production CAD. If selection or safety architecture is unresolved, stop at an explicitly provisional concept package.
3. Inspect the source CAD, drawing, screenshot, and user requirements. Record concrete defects and separate supplied values from derived or assumed values.
4. Preserve unrelated user geometry. Create a clean replacement in a separate area when extensive repair is needed; remove old geometry only when the user authorizes it.
5. Confirm the sheet size, scale, units, projection method, CAD plot style, and required deliverable before laying out views. For a GB/T mechanical drawing, default to first-angle projection only when the user, approved project template, and source drawing do not specify another method; record the assumption and keep view placement, projection symbol, and title-block data consistent.
6. Establish semantic layers and properties before geometry. Select line widths from the applicable standard series and the sheet/scale; keep a clear thick-to-thin ratio. A practical fallback is:
   - `OUTLINE`: thick continuous.
   - `THIN`: thin continuous.
   - `CENTER`: thin chain.
   - `HIDDEN`: thin dashed.
   - `HATCH`: thin continuous.
   - `DIM`: thin continuous.
   - `TEXT`: thin continuous.
7. Use a monochrome plotted hierarchy. Layer colors may aid CAD editing only when the configured plot style produces the required line types, widths, and monochrome output.
8. Lay out aligned orthographic views first and keep projection correspondence exact. Add sections only when they clarify internal geometry.
9. Add dimensions from the part outward. Prefer functional datums; avoid closed chains, duplicates, crossings, and dimensions attached to hidden lines.
10. Add tolerances, fits, surface texture, material, process notes, and title-block data only when supplied or technically justified. Mark unresolved production data as `TBD` or clearly identify it as assumed.
11. Run the selected verification tier and presentation checks. For Tier 1, inspect the active affected geometry/view and report deferred release gates; for Tier 3, inspect model space plus the current final plotted/exported sheet at readable and full-sheet zoom before declaring release readiness.

### P0 Mutation Gates (must pass before every drawing or model edit)

- **Document identity gate**: Before `create`, `open`, `activate`, `save`, `export`, or any mutation, capture and compare `doc_id`, requested absolute path, active document ID/path, configuration, units, and revision. Every mutation carries `doc_id` and `expected_revision`; a mismatch is `E_DOCUMENT_ID_MISMATCH`, not a warning. Never silently switch the user's active document.
- **Transaction gate**: Group each logical subsystem in `transaction.begin`/`commit`. A failed entity, COM exception, timeout, stale revision, missing layer, or postcondition mismatch rolls back the complete transaction. Verify the entity count and revision returned to their pre-batch values; a partial rollback is `FAIL`.
- **Postcondition gate**: After every mutable call, perform a native readback and compare requested versus actual type, coordinates, dimensions, layer, semantic role, associations, closure, bounds, and volume/area. Any unexplained `diff` is a hard stop; delete the suspect entity, attempt one bounded recovery, then switch backend or report `BLOCKED`.
- **Layer and authority gate**: Resolve all required layers, linetypes, dimension styles, fonts, and source authorities before creating geometry. A missing layer or unverified purchased-part interface must fail before entity creation; never fall back to layer `0` or guessed production dimensions.
- **User-session gate**: Attach to an existing AutoCAD process in read/preserve window mode by default. Do not activate, minimize, restore, or alter profile variables unless the caller explicitly requests that operation and the ownership check permits it.

### Evidence Synchronization Gates

- **Registry/B-rep atomic sync (P0)**: Treat the semantic feature registry, native AutoCAD entity registry, and B-rep/model state as one transaction. A feature is committed only when all three contain the same stable feature ID, component ownership, parameters, bounds, and revision. If one store updates and another does not, roll back every side effect (entities, layers, registry rows, generated previews, and journal pointers) and return `E_REGISTRY_BREP_OUT_OF_SYNC`.
- **Rollback side effects (P0)**: Rollback evidence must include entity/feature counts, registry row counts, layer changes, output files, and document revision before/after. Delete temporary files with an atomic cleanup record; never report rollback success merely because a command raised an exception.
- **AABB containment semantics (P1)**: Use axis-aligned bounding boxes only as broad-phase evidence. Every containment result must identify `container_component_id`, `contained_component_id`, `design_role`, coordinate frame, tolerance, and whether it is `exact_brep` or `aabb_screening`. AABB overlap or containment cannot certify contact, wall thickness, or interference clearance.
- **Render truth (P1)**: A preview is valid only when it records `visual_style`, `material_render_verified`, camera/projection, visible components, nonblank ratio, clipping, and content hash. `material_render_verified=false` is not a shaded/material review pass; a line-only PNG must be labeled wireframe evidence.
- **Scale truth (P1)**: `FIT`/`NTS` and a fixed numeric scale (`1:1`, `1:2`, etc.) are mutually exclusive. If `FIT` is used, the title block must say `FIT` or `NTS`; if a fixed ratio is declared, calculate and verify the actual paper/media-box scale. Any mixed declaration is `PLOT_SCALE_CONSISTENCY=FAIL`.
- **Prepared review geometry (P1)**: Section and exploded views require prepared, revision-bound geometry states before rendering: section plane and cut set, or component transforms and exploded offsets. A screenshot created by ad-hoc camera movement without a prepared state is not section/exploded evidence.
- **Round evidence (P1)**: Each campaign round must retain `reports/round.json` with identity, transaction/rollback records, requested-vs-actual diffs, DRC results, AABB semantics, render truth, scale truth, deliverable hashes, and lessons. Missing or hand-edited evidence downgrades the round to `BLOCKED`.

## CAD Execution Rules

### Execution Stability Gate

- Keep every external test, renderer, CAD bridge, and subprocess call bounded. Use a hard per-operation timeout plus a hard campaign timeout; never await an unbounded process or nested execution cell.
- A timeout is a recorded `TIMEOUT`/`BLOCKED` result, not permission to retry indefinitely. Preserve the JSON evidence and terminate only processes owned by the test wrapper.
- Do not restart the Codex/Claude host application to recover a CAD or test failure. Do not start, close, or alter a user-owned AutoCAD session implicitly; use read-only `preflight` first and require explicit user opt-in for live startup.
- Keep GUI viewers suppressed during automation. Write PNG/PDF artifacts to the managed output root and return their paths; do not open an external viewer or steal foreground focus.

- Use native CAD line, arc, circle, polyline, hatch, text, and dimension entities.
- Prefer associative dimension objects. Do not fake dimensions using loose text and arrows.
- Keep geometry and annotation in their intended spaces. Verify viewport scale, annotation scale, and plot lineweights when paper space is used.
- Keep centerlines beyond outlines by a small, even amount. Use proper center linetype; never use a continuous colored axis through the part.
- For Chinese GB/T text, use a verified technical lettering style with complete Chinese/symbol coverage and faithful plotted output. Font filenames such as `gbenor`/`gbcbig` or TrueType substitutes are environment choices, not compliance evidence by themselves.
- Put diameter symbols and fit designations in the dimension object or associated requirement, not as unrelated notes inside the part.
- Keep dimension text horizontal where the active dimensioning method requires it and use a consistent text height.
- Keep cutting-plane identifiers and section labels paired when the convention requires them. Call a simple end view an end view, not `SECTION A-A`.
- Use a standard title block proportioned for the selected sheet. Avoid oversized decorative text.
- Do not infer manufacturing-critical values from appearance alone. Never invent a fit, tolerance, surface texture, material, heat treatment, or process requirement.
- Treat view agreement as a geometric proof obligation. A clean-looking view is not valid when its features cannot describe the same part as the other views and sections.
- Separate geometric/kinematic plausibility from engineering performance. Without loads, material properties, boundary conditions, and acceptance criteria, do not claim strength, stiffness, fatigue, thermal, fluid, or safety validation.
- Keep editable parametric/native CAD as the source of truth. Treat STEP/DXF/PDF exports, meshes, renders, and plots as derived artifacts unless no stronger source exists.
- Use named parameters, stable datums/axes, native features, and native patterns. Build assemblies from explicit mating interfaces and degrees of freedom, not unexplained world-coordinate offsets.
- Identify the exact configuration, revision, units, CAD/kernel/API versions, and external dependencies before mutation or release. Use semantic IDs/datums instead of volatile face/edge indices where possible, and prove that each intended edit changed the correct geometry rather than trusting a success flag.
- After every mutable CAD call, read back the created/modified semantic entities and compare requested versus actual type, layer/role, coordinates/parameters, associations, and closure. Any unexplained mismatch is a hard stop: rollback the stage, attempt one bounded recovery, then switch to a verified backend or report `blocked`; never continue decorating suspect geometry.
- Select the verification tier from `cad-workflows.md`. Use changed-scope checks for a narrow nonrelease edit; require full release DRC, final plot review, and applicable exchange re-import only for release/export handoff or when an escalation trigger invalidates global evidence. A successful command or attractive render is never a design-review pass by itself.
- For AutoCAD/MCP work, prove readiness before mutation, use bounded recovery, track created handles, and prefer atomic transactions. For release/export work, also verify actual plotted paper/scale and re-imported DXF geometry; do not force those unchanged artifacts through a Tier 1 local edit. A successful IPC response, save, entity count, or manifest is not release evidence by itself.
- For semantic interference, classify every crossing or contact by `component_id`, `design_role`, `view_id`, `intentional_open_end`, `permitted_crossing`, and `source_authority`. Motion overlays, section indicators, leaders, and title-block lines must not be audited as solid geometry. Any unclassified crossing, dangling endpoint, near-contact gap, or interpenetrating solid is `FAIL`, including for concept drawings.
- For native 3D presentation, set an allow-listed visual style (`ShadedWithEdges`, `Conceptual`, or another verified style), fixed camera, projection, background, resolution, and output path. Read back the actual camera/style and image metrics; require nonblank pixels, no clipping, stable content hash, and a centered frame. A wireframe or desktop screenshot is not a shaded-render pass.
- For plotting, compare title-block scale with the actual PDF/PNG paper, orientation, viewport scale, and media box. `FIT`, `NTS`, and `1:1` are different claims; a fit-to-extents output labeled `1:1` is an immediate `PLOT_SCALE_CONSISTENCY` failure.
- For a complex assembly, require a parameter table, component tree, common datums, intended connection graph, and view plan before creating detailed entities. Build and review one coherent subsystem at a time; do not release a monolithic coordinate batch that has not passed intermediate topology and visual checks.
- For a new consumer-product concept or major form-factor change, establish people, scenarios, interface/port count, user actions, cable directions, and product intent; compare at least three low-cost silhouettes and obtain an authorized selection before detailed modeling. A supplied approved concept may bypass comparison only with recorded revision/authority.
- When mains, hazardous energy, or moving/rotating hazards are in scope, require a preliminary isolation/grounding/fire/motion-protection/compliance architecture before internal detail. Until then, create only exterior concepts and hazard/keep-out envelopes; never label them manufacturable, safe, compliant, or certifiable.
- Use supplier data or controlled physical measurements for detail-driving purchased-part envelopes and mounting interfaces. Keep unverified installation dimensions as `TBD` and outside manufacturing authority.
- Immediately preview the parameterized skeleton before detailed features or annotation. Check proportion, layout, people/actions, port count/direction, cable routes, support footprint, purchased-part envelopes, and safety/service keep-outs; return to concept selection when the skeleton fails.
- Keep geometry/drawing DRC and product-design review as separate verdicts. For applicable consumer products, review appearance intent, ergonomics, reach/access, service, cable management, and stability with explicit evidence; a geometrically valid model or polished render is not a product-design pass.
- A concept/schematic label may reduce production annotation, analysis, and detail requirements; it never waives basic topology, ownership, view-source, scale-truth, or visual-integrity gates. Require zero unexplained dangling endpoints, interior crossings, unowned lines, and open material boundaries.
- When native 3D, constraints, projection, trim/join, or reliable preview capabilities are unavailable, define the 2D fallback scope before drawing and label it accurately. Never present a separately estimated 2D concept as equivalent to a validated 3D assembly or manufacturing drawing.
- Treat agent-generated manufacturing artifacts as `candidate after human review` unless an authorized external process records approval. Never turn missing evidence, stale waivers, or unavailable checks into a favorable release verdict.
- When a tool cannot create or verify required linetypes, symbols, fonts, dimension styles, or plot behavior, state the limitation and use the closest documented fallback. Do not claim full compliance.

## Progressive References

- `references/gbt-drafting.md`: standards baseline, drawing rules, physical and mathematical checks, staged verification, and release audit.
- `references/autocad-mcp-workflow.md`: AutoCAD readiness, dispatcher recovery, structured errors, safe setup, transactions, annotation handles, geometry audit, plotting, DXF comparison, and mechanical primitives.
- `references/complex-assembly-drafting.md`: complex assembly classification, parameterized skeletons, component/connectivity planning, staged construction, topology checks, view consistency, line cleanup, and release gates.
- `references/consumer-product-concept.md`: consumer-product brief, three-concept comparison, purchased-part evidence, mains/moving-part safety gates, early skeleton preview, product-design review, and failure review.
- `references/cad-workflows.md`: evidence hierarchy, native 2D editing, 3D-backed drawing, 2D-to-3D consistency reconstruction, PDF/image intake, 3D review packets, tool routing, and risk-scaled validation.
- `references/cad-3d-modeling.md`: parametric solid/surface modeling, assemblies, motion, representation choice, exchange formats, iteration, and 3D presentation.
- `references/gps-inspection.md`: GD&T/GPS semantics, datum systems, tolerance stacks, model/drawing agreement, inspection planning, and measurement uncertainty.
- `references/product-definition-release.md`: configuration/revision authority, stable identity, BOM/balloons, dependencies, semantic change review, interoperability, and reproducible release packages.
- `references/engineering-analysis.md`: dimensional and conservation checks, load cases, hand calculations, structural/thermal/fluid analysis evidence, convergence, and claim boundaries.
- `references/drc-review.md`: deterministic validator contract, universal geometry and drawing gates, assembly checks, process-specific DFM, severity, evidence, and release reporting.

## Five-Round Hard-Gate Mapping

When running the campaign in `docs/CAD-5-ROUND-CAMPAIGN-20260719.md`, apply these additional release blockers:

- **R1 mechanical part**: fail on any radius/chamfer readback outside the stated tolerance, hole-axis error above `0.05 mm`, invalid B-rep, or supplier-controlled port dimensions presented as manufacturing dimensions.
- **R2 transmission assembly**: fail on center-distance or coaxiality error above `0.05 mm`, duplicated source geometry for configurations, unclassified gear/shaft interference, or concept tooth geometry described as a production gear.
- **R3 enclosure/bracket**: fail when minimum wall thickness is below the specified limit, a rib does not structurally intersect its parent, flange/hole pattern is not concentric, or an A3/PDF media-box scale disagrees with the title block. Unrun draft-angle analysis must remain `NOT_EVALUATED` and block release-candidate status.
- **R4 consumer enclosure**: fail when parting gap is outside `0.25~0.35 mm`, inner wall is below `2.0 mm`, controls are not coaxial/accessible, USB or other purchased openings lack controlled authority, or any required shaded review view is clipped/blank. `appearance_review` and `ergonomics_review` are independent verdicts and cannot inherit geometry PASS.
- **R5 motion assembly**: fail when component instances are copied instead of transformed, joint limits accept an out-of-range command, sampled clearance falls below `2 mm`, exploded transforms are not reversible, or motion overlays lack explicit semantics. A broad-phase sweep must never be reported as exact interference proof.

## Revision Strategy

For an isolated defect with stable source geometry and identifiers, edit the responsible feature/entity in place, preserve a rollback point, and run targeted dependent checks. Create a clean replacement in a separate area only when defects are widespread, topology/view authority is unreliable, or repair would cross several subsystems/views. Compare geometry, annotations, and plotted output before replacing the obsolete version, and erase it only with explicit permission. After a gate escape, failed prototype, repeated tool failure, or misleading deliverable, use the evidence/root-cause/containment/permanent-fix/prevention structure in `consumer-product-concept.md`. In the final response, summarize corrected defects, assumptions, unresolved `TBD` items, files produced, deferred release checks, and any compliance limitation.
