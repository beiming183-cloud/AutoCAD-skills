# AutoCAD MCP Workflow

Read this reference whenever AutoCAD is operated through MCP, file IPC, COM, scripts, or another automation bridge.

Keep this workflow bridge-neutral. Names such as `system.ensure_ready`, transaction operations, and JSON bodies describe required capabilities or preferred contracts; call them only when the active bridge exposes them, otherwise use an available safe equivalent and record the limitation.

## Contents

- Readiness and capability discovery
- Failure contract and bounded recovery
- Mechanical drawing setup
- Transactions and entity ownership
- Geometry and annotation execution
- Geometry DRC
- Preview, plotting, and scale proof
- Delivery and DXF re-import
- Mechanical primitives and gears
- Standard workflow

## Readiness and Capability Discovery

Treat readiness as an idempotent state transition, not as a side effect of a status query.

1. Discover installed AutoCAD products and executable paths from the environment or bridge. Do not hardcode `AutoCAD LT`, a version, or a user-specific path.
2. Inspect whether AutoCAD is running and identify the actual product/version.
3. Wait for an active document or create one only when the user requested a new drawing.
4. Verify that the dispatcher/bridge is loaded, compatible, and responsive with a version handshake and IPC ping.
5. Prefer an exposed `system.ensure_ready`-style operation when available. Otherwise execute the equivalent discover/start/wait/load/handshake/ping steps using only exposed safe tools.
6. Keep `status` observational. Do not hide startup, LISP loading, document creation, or retries inside a call presented as read-only.

Return or record separate state for installation, process, document, dispatcher version, transport, and readiness. Never infer the product edition from a missing window or dispatcher error.

Use bounded recovery:

- Autostart or reload the trusted dispatcher at most once per unchanged failure state.
- Re-ping after the recovery action.
- Stop and report the exact failed state when the retry does not change it. Do not loop on startup or IPC timeouts.
- Do not run mutable CAD calls in parallel against the same document or file-IPC queue.

## Failure Contract and Bounded Recovery

Treat any payload containing an error as failure even when an outer MCP wrapper incorrectly reports `isError: false`. Normalize nested text JSON before deciding whether an operation succeeded.

Prefer structured failures containing:

```json
{
  "ok": false,
  "error": {
    "code": "E_DISPATCHER_NOT_LOADED",
    "message": "AutoCAD is running but the dispatcher is unavailable",
    "recoverable": true,
    "recommended_action": "autoload_dispatcher"
  }
}
```

Distinguish at least these states when the bridge exposes enough evidence:

- `E_AUTOCAD_NOT_INSTALLED`
- `E_AUTOCAD_NOT_RUNNING`
- `E_NO_ACTIVE_DOCUMENT`
- `E_DISPATCHER_NOT_LOADED`
- `E_DISPATCHER_VERSION_MISMATCH`
- `E_IPC_TIMEOUT`
- `E_COMMAND_STATE_BLOCKED`
- `E_OUTPUT_PATH_REJECTED`

Do not guess recovery from message fragments when a code or state probe is available. Report bridge defects separately from drawing defects.

## Mechanical Drawing Setup

Create or verify one explicit setup contract before geometry:

```json
{
  "standard": "GB/T",
  "units": "mm",
  "sheet": "A3",
  "orientation": "landscape",
  "projection": "first-angle",
  "scale": "1:1"
}
```

Apply the contract to actual CAD state, not only delivery metadata:

- Drawing units and insertion units.
- Layer names, linetypes, and lineweights.
- Text, dimension, leader, and table styles.
- Paper-space layout, page setup, plot device, paper size, printable area, orientation, plot style, plot area, and scale mode.
- Frame/title-block attributes, including the same sheet, projection, units, and scale values used by plotting.

Prefer a safe whitelisted variable-setting operation. Restrict variable names, types, and ranges; read values back after setting. Do not bypass the bridge with arbitrary LISP merely to change units or dimension variables.

Treat values such as dimension text height as configuration selected for the sheet/style, not universal constants.

## Transactions and Entity Ownership

Prefer atomic batch creation or explicit `begin` / `commit` / `rollback` semantics.

- `continue_on_error: false` stops later calls but does not prove rollback.
- Require `atomic: true` or `rollback_on_error: true` when the bridge supports it.
- If transactions are unavailable, create new work on a unique staging layer/block, record every returned handle, validate the batch, then promote it. On failure, remove only the tracked new entities when deletion is authorized.
- Never use a broad erase or layer purge as an improvised rollback in a user drawing.
- Preserve the original drawing and save to a revision/copy when the blast radius is uncertain.

Maintain an operation manifest containing source operation IDs, entity handles, layer, role, and grouping. This manifest supports targeted repair and evidence reporting.

## Geometry and Annotation Execution

- Use native AutoCAD entities and associative dimensions wherever supported.
- Prefer blocks, arrays, constraints, or parameterized repeated features over copied loose geometry.
- Require creation responses to return all relevant handles. A leader-plus-text operation should identify the leader, text, and association/group rather than only the top-level entity type.
- Group annotation changes so they can be moved, deleted, or rolled back together.
- Use native annotation styles, explicit text height, and collision/clearance checks. Re-audit after automatic placement; auto-avoidance is evidence only after visual review.
- When an API lacks a native or associative construct, document the fallback and its editability/export limitations.

## Geometry DRC

Run geometry DRC before presentation review and again on the exported/re-imported artifact.

For lines, arcs, circles, and polylines, check:

- Consecutive duplicate vertices and repeated closing vertices.
- Zero-length and below-tolerance segments.
- Zero/invalid radius, nonfinite coordinates, and degenerate arcs.
- Open profiles that must be closed.
- Self-intersections, local reversals, spikes, and inconsistent winding where orientation matters.
- Duplicate or reversed duplicate entities.
- Overlapping collinear segments and unintended coincident geometry.
- Unexpected entity islands, layer/type mismatches, and stray construction geometry that will plot.

Use an explicit model-space tolerance with units. Each failure must identify the entity handle, segment/subentity index, location, measured value, and threshold. Entity count, closed flags, save success, and DXF readability do not prove clean geometry.

Prefer repairing the source generator and regenerating. Automated cleanup may remove consecutive duplicate vertices or zero-length segments only on newly generated/tracked geometry and only when topology and intent remain unchanged. Re-run the full affected audit after cleanup.

## Preview, Plotting, and Scale Proof

Keep preview and release plotting semantically distinct:

- A PNG preview operation must produce PNG at an explicit resolution/DPI or return image content/thumbnail data.
- A PDF plot operation must produce a plotted PDF with explicit page setup.
- If only PDF is available, rasterize it with an available structured PDF renderer and disclose the fallback; do not pretend the PDF path is a PNG preview.

For every release plot, explicitly set and verify:

- Plot device and media/paper name.
- Orientation and printable area.
- Layout/window/extents plot area.
- Monochrome or required plot style.
- Fixed versus fit-to-paper scale.
- Center/offset and lineweight behavior.

When the title block says `1:1`, require fixed 1:1 plotting. Record the calculated plot scale and reject a fit-to-paper result mislabeled as 1:1. Reopen the PDF and inspect full-sheet plus readable-detail views for blank output, clipping, overlaps, missing fonts/symbols, incorrect lineweights, and scale/title-block disagreement.

## Delivery and DXF Re-import

Deliver from the verified authoritative drawing and then re-import or independently parse the exchange artifact.

For DXF, record and compare:

- `$INSUNITS`, `$ACADVER`, coordinate precision, and extents.
- Entity counts grouped by type and layer.
- Canonical geometry fingerprints at a declared tolerance.
- Polyline vertex count, closed flag, bulge/arc data, and segment lengths.
- Circle/arc centers, radii, and angles.
- Unicode text and attributes.
- Native dimension/leader preservation versus exploded lines, text, or proxy objects.
- Critical dimensions and reference coordinates.

Compare the source drawing, DXF re-import, plotted PDF, and manifest as different evidence channels. A matching total entity count is only a coarse inventory check.

The final report must state actual files, paper, plot scale, units, DRC results, re-import comparison, assumptions, unsupported objects, and every `NOT_EVALUATED` item.

## Mechanical Primitives and Gears

Use domain-aware primitives when exposed. Do not advertise a generic polyline as a validated mechanical gear.

Classify gear output explicitly:

- `symbolic`: diagrammatic symbol only.
- `simplified`: approximate teeth for layout/communication; mark `NOT FOR MANUFACTURING`.
- `manufacturing`: true validated involute geometry with complete design inputs.

For spur, internal, and planetary gears, validate as applicable:

- Module, pressure angle, tooth counts, profile shifts, addendum/dedendum, and center distance.
- Root-cut/undercut risk; for an unshifted standard full-depth external gear, compare tooth count with the applicable minimum such as `2 / sin(alpha)^2` before claiming a standard tooth form.
- Internal/external mesh compatibility, interference, contact ratio, backlash, and tooth thickness.
- Planetary relation `Zr = Zs + 2*Zp` for the standard concentric arrangement.
- Equal-planet assembly phase, including divisibility of `(Zs + Zr) / Np` for the applicable arrangement.
- Planet-to-planet clearance, carrier pin positions, tooth phase, and motion/interference through a full cycle.

Manufacturing output requires true involute geometry and process/tolerance data. If the bridge lacks these primitives, perform the calculations with a proven mechanical library or keep the drawing symbolic/simplified and disclose the limitation.

## Standard Workflow

Use this sequence, skipping only steps that are genuinely inapplicable:

```text
discover capabilities and installation
-> ensure AutoCAD/dispatcher/document readiness
-> create or verify mechanical setup
-> begin atomic/staged transaction
-> create structured geometry and annotations
-> audit geometry
-> audit presentation
-> plot and inspect preview
-> commit/promote the transaction
-> deliver DWG/DXF/PDF
-> re-import and compare DXF geometry
-> publish artifacts and evidence
```

Do not collapse `audit geometry`, `audit presentation`, `plot review`, and `exchange re-import` into one generic `validated` flag.
