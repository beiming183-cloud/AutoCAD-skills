---
name: mechanical-drafting-gbt
description: Create, revise, audit, validate, and present mechanical CAD using Chinese GB/T drafting conventions. Use for AutoCAD/AutoCAD MCP; parametric 2D/3D parts, complex assemblies, mechanisms, engines, gears, and machined parts; DXF/DWG/PDF/STEP and model-based definition workflows; assembly/detail drawings and cross-view verification; dimensions, fits, GD&T/GPS, surface texture, tolerance stacks, and inspection planning; BOMs, item balloons, configurations, revisions, and release packages; CAD DRC/DFM, physical plausibility, engineering-analysis evidence, and drawing-standard compliance.
---

# GB/T Mechanical Drafting

Create readable manufacturing drawings, not decorative CAD illustrations. Treat geometry, line hierarchy, view layout, dimensions, and notes as one system.

## Portability Contract

- Keep the core workflow agent- and vendor-neutral. Apply it in Codex, Claude Code, or another compatible skill runner without changing the engineering acceptance criteria.
- Treat `SKILL.md` and `references/` as the authoritative instructions. Ignore optional runtime-specific metadata, such as `agents/openai.yaml`, when the current runner does not use it.
- Discover the available CAD application, MCP/automation bridge, shell, parsers, and renderers before execution. Map capability-level steps to exposed safe tools instead of assuming a particular tool namespace or exact operation name.
- Treat operation names and JSON payloads in the references as interface examples unless the active bridge explicitly exposes them. Never invent a tool call or claim a check ran when only an example schema exists.
- Keep deliverables and validation evidence in standard CAD/exchange/report artifacts so another agent or application can reopen and independently verify them.

## Required Workflow

1. Classify the task and load only the required references: always read `references/gbt-drafting.md` for engineering drawings; read `references/autocad-mcp-workflow.md` for AutoCAD/MCP execution, `references/complex-assembly-drafting.md` for engines or other multi-system assembly drawings, `references/cad-workflows.md` for 2D/3D conversion or presentation, `references/cad-3d-modeling.md` for 3D parts/assemblies, `references/gps-inspection.md` for GD&T/GPS, tolerance-stack, or inspection work, `references/product-definition-release.md` for configurations, BOMs, revisions, MBD/PMI, dependencies, or release packages, `references/engineering-analysis.md` for any physical-performance calculation or simulation claim, and `references/drc-review.md` for every DRC, DFM, fit, interference, or release review.
2. Inspect the source CAD, drawing, screenshot, and user requirements. Record concrete defects and separate supplied values from derived or assumed values.
3. Preserve unrelated user geometry. Create a clean replacement in a separate area when extensive repair is needed; remove old geometry only when the user authorizes it.
4. Confirm the sheet size, scale, units, projection method, CAD plot style, and required deliverable before laying out views. For a GB/T mechanical drawing, default to first-angle projection only when the user, approved project template, and source drawing do not specify another method; record the assumption and keep view placement, projection symbol, and title-block data consistent.
5. Establish semantic layers and properties before geometry. Select line widths from the applicable standard series and the sheet/scale; keep a clear thick-to-thin ratio. A practical fallback is:
   - `OUTLINE`: thick continuous.
   - `THIN`: thin continuous.
   - `CENTER`: thin chain.
   - `HIDDEN`: thin dashed.
   - `HATCH`: thin continuous.
   - `DIM`: thin continuous.
   - `TEXT`: thin continuous.
6. Use a monochrome plotted hierarchy. Layer colors may aid CAD editing only when the configured plot style produces the required line types, widths, and monochrome output.
7. Lay out aligned orthographic views first and keep projection correspondence exact. Add sections only when they clarify internal geometry.
8. Add dimensions from the part outward. Prefer functional datums; avoid closed chains, duplicates, crossings, and dimensions attached to hidden lines.
9. Add tolerances, fits, surface texture, material, process notes, and title-block data only when supplied or technically justified. Mark unresolved production data as `TBD` or clearly identify it as assumed.
10. Run the selected verification tier and presentation checks. For Tier 1, inspect the active affected geometry/view and report deferred release gates; for Tier 3, inspect model space plus the current final plotted/exported sheet at readable and full-sheet zoom before declaring release readiness.

## CAD Execution Rules

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
- Select the verification tier from `cad-workflows.md`. Use changed-scope checks for a narrow nonrelease edit; require full release DRC, final plot review, and applicable exchange re-import only for release/export handoff or when an escalation trigger invalidates global evidence. A successful command or attractive render is never a design-review pass by itself.
- For AutoCAD/MCP work, prove readiness before mutation, use bounded recovery, track created handles, and prefer atomic transactions. For release/export work, also verify actual plotted paper/scale and re-imported DXF geometry; do not force those unchanged artifacts through a Tier 1 local edit. A successful IPC response, save, entity count, or manifest is not release evidence by itself.
- For a complex assembly, require a parameter table, component tree, common datums, intended connection graph, and view plan before creating detailed entities. Build and review one coherent subsystem at a time; do not release a monolithic coordinate batch that has not passed intermediate topology and visual checks.
- When native 3D, constraints, projection, trim/join, or reliable preview capabilities are unavailable, define the 2D fallback scope before drawing and label it accurately. Never present a separately estimated 2D concept as equivalent to a validated 3D assembly or manufacturing drawing.
- Treat agent-generated manufacturing artifacts as `candidate after human review` unless an authorized external process records approval. Never turn missing evidence, stale waivers, or unavailable checks into a favorable release verdict.
- When a tool cannot create or verify required linetypes, symbols, fonts, dimension styles, or plot behavior, state the limitation and use the closest documented fallback. Do not claim full compliance.

## Progressive References

- `references/gbt-drafting.md`: standards baseline, drawing rules, physical and mathematical checks, staged verification, and release audit.
- `references/autocad-mcp-workflow.md`: AutoCAD readiness, dispatcher recovery, structured errors, safe setup, transactions, annotation handles, geometry audit, plotting, DXF comparison, and mechanical primitives.
- `references/complex-assembly-drafting.md`: complex assembly classification, parameterized skeletons, component/connectivity planning, staged construction, topology checks, view consistency, line cleanup, and release gates.
- `references/cad-workflows.md`: evidence hierarchy, native 2D editing, 3D-backed drawing, 2D-to-3D consistency reconstruction, PDF/image intake, 3D review packets, tool routing, and risk-scaled validation.
- `references/cad-3d-modeling.md`: parametric solid/surface modeling, assemblies, motion, representation choice, exchange formats, iteration, and 3D presentation.
- `references/gps-inspection.md`: GD&T/GPS semantics, datum systems, tolerance stacks, model/drawing agreement, inspection planning, and measurement uncertainty.
- `references/product-definition-release.md`: configuration/revision authority, stable identity, BOM/balloons, dependencies, semantic change review, interoperability, and reproducible release packages.
- `references/engineering-analysis.md`: dimensional and conservation checks, load cases, hand calculations, structural/thermal/fluid analysis evidence, convergence, and claim boundaries.
- `references/drc-review.md`: deterministic validator contract, universal geometry and drawing gates, assembly checks, process-specific DFM, severity, evidence, and release reporting.

## Revision Strategy

For an isolated defect with stable source geometry and identifiers, edit the responsible feature/entity in place, preserve a rollback point, and run targeted dependent checks. Create a clean replacement in a separate area only when defects are widespread, topology/view authority is unreliable, or repair would cross several subsystems/views. Compare geometry, annotations, and plotted output before replacing the obsolete version, and erase it only with explicit permission. In the final response, summarize corrected defects, assumptions, unresolved `TBD` items, files produced, deferred release checks, and any compliance limitation.
