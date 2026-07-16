---
name: mechanical-drafting-gbt
description: Create, revise, audit, validate, and present mechanical CAD using Chinese GB/T drafting conventions. Use for parametric 3D parts and assemblies, DXF/DWG/PDF/STEP workflows, CAD design-rule checks (DRC), design-for-manufacturing (DFM) reviews, shafts, sleeves, flanges, machined parts, assembly and detail drawings, orthographic projection, views and sections, dimensions, fits and tolerances, surface texture, title blocks, line types, 2D/3D cross-verification, 3D review presentations, and drawing-standard compliance reviews.
---

# GB/T Mechanical Drafting

Create readable manufacturing drawings, not decorative CAD illustrations. Treat geometry, line hierarchy, view layout, dimensions, and notes as one system.

## Required Workflow

1. Classify the task and load only the required references: always read `references/gbt-drafting.md` for engineering drawings; read `references/cad-workflows.md` for 2D/3D conversion or presentation, `references/cad-3d-modeling.md` for 3D parts/assemblies, and `references/drc-review.md` for every DRC, DFM, fit, interference, or release review.
2. Inspect the source CAD, drawing, screenshot, and user requirements. Record concrete defects and separate supplied values from derived or assumed values.
3. Preserve unrelated user geometry. Create a clean replacement in a separate area when extensive repair is needed; remove old geometry only when the user authorizes it.
4. Confirm the sheet size, scale, units, projection method, CAD plot style, and required deliverable before laying out views. If any are unknown, state a conservative assumption.
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
10. Run the staged verification in the reference, then the presentation audit. Inspect model space and the final plotted/exported sheet at readable and full-sheet zoom before declaring completion.

## CAD Execution Rules

- Use native CAD line, arc, circle, polyline, hatch, text, and dimension entities.
- Prefer associative dimension objects. Do not fake dimensions using loose text and arrows.
- Keep geometry and annotation in their intended spaces. Verify viewport scale, annotation scale, and plot lineweights when paper space is used.
- Keep centerlines beyond outlines by a small, even amount. Use proper center linetype; never use a continuous colored axis through the part.
- Put diameter symbols and fit designations in the dimension object or associated requirement, not as unrelated notes inside the part.
- Keep dimension text horizontal where the active dimensioning method requires it and use a consistent text height.
- Keep cutting-plane identifiers and section labels paired when the convention requires them. Call a simple end view an end view, not `SECTION A-A`.
- Use a standard title block proportioned for the selected sheet. Avoid oversized decorative text.
- Do not infer manufacturing-critical values from appearance alone. Never invent a fit, tolerance, surface texture, material, heat treatment, or process requirement.
- Treat view agreement as a geometric proof obligation. A clean-looking view is not valid when its features cannot describe the same part as the other views and sections.
- Separate geometric/kinematic plausibility from engineering performance. Without loads, material properties, boundary conditions, and acceptance criteria, do not claim strength, stiffness, fatigue, thermal, fluid, or safety validation.
- Keep editable parametric/native CAD as the source of truth. Treat STEP/DXF/PDF exports, meshes, renders, and plots as derived artifacts unless no stronger source exists.
- Use named parameters, stable datums/axes, native features, and native patterns. Build assemblies from explicit mating interfaces and degrees of freedom, not unexplained world-coordinate offsets.
- Run incremental DRC on changed geometry and one full release DRC before handoff. A successful command or attractive render is not a passed design review.
- When a tool cannot create or verify required linetypes, symbols, fonts, dimension styles, or plot behavior, state the limitation and use the closest documented fallback. Do not claim full compliance.

## Progressive References

- `references/gbt-drafting.md`: standards baseline, drawing rules, physical and mathematical checks, staged verification, and release audit.
- `references/cad-workflows.md`: evidence hierarchy, native 2D editing, 3D-backed drawing, 2D-to-3D consistency reconstruction, PDF/image intake, 3D review packets, tool routing, and risk-scaled validation.
- `references/cad-3d-modeling.md`: parametric solid/surface modeling, assemblies, motion, representation choice, exchange formats, iteration, and 3D presentation.
- `references/drc-review.md`: deterministic validator contract, universal geometry and drawing gates, assembly checks, process-specific DFM, severity, evidence, and release reporting.

## Revision Strategy

For a poor existing drawing, create a clean replacement in a separate area first. Compare geometry, annotations, and plotted output, then erase the obsolete version only with explicit permission. In the final response, summarize corrected defects, assumptions, unresolved `TBD` items, files produced, and any compliance limitation.
