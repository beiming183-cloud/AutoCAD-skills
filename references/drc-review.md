# CAD Design Rule Check and Review

Read this reference for every DRC, DFM, fit, interference, tolerance, conversion, or release review.

## Principle

A deterministic validator owns pass/fail. The agent chooses the correct rules, parameters, evidence, and review depth; it does not replace a missing measurement with visual confidence.

There is no universal `manufacturable` result. Process, material, machine, tooling, supplier, quantity, and inspection capability determine the applicable rule deck and thresholds.

## Validator Contract

Every rule must define:

- Stable rule ID, domain, description, severity, and applicability condition.
- Source of the requirement: user specification, GB/T/other named standard, organization rule, vendor rule, or clearly labeled typical guidance.
- Explicit units, threshold, inclusivity at the boundary, tolerance, datum/direction, and configuration.
- Required representation and preconditions: native model, valid B-rep solid, watertight manifold mesh, structured DXF, drawing view, or assembly.
- Deterministic algorithm and any sampling density/error bound.
- Result schema containing status, measured value, threshold, margin, units, location/entity IDs, parameters used, and evidence artifact.
- Known false-positive and false-negative conditions.

Never bury thresholds in prose or code constants without naming their source. Never report a sampled or mesh-derived result as exhaustive/exact.

## Status and Severity

Use these result states:

- `PASS`: preconditions passed and measured evidence satisfies the applicable rule.
- `FAIL`: measured evidence violates an applicable rule.
- `WARNING`: evidence indicates risk or a nonblocking recommendation, not a disguised failure.
- `NOT_EVALUATED`: required inputs, rule deck, representation, or tool capability are absent.
- `ERROR`: the validator could not complete reliably.

Keep severity separate from confidence. A critical rule with weak evidence is `NOT_EVALUATED`, not a low-confidence pass.

## Gate Sequence

### Gate 0: intake and rule applicability

- Identify revision, units, coordinate system, configuration, material, manufacturing process, supplier/machine limits, and intended use.
- Select the applicable rule deck and record unknown inputs.
- Establish which source/model/drawing is authoritative and whether derived files are stale.
- Build a cross-reference matrix when several artifacts define the design: requirement/specification, native model, drawing, BOM, standard/purchased-part data, and release export. Missing or contradictory mappings are findings even when each file is internally valid.

### Gate 1: representation validity

- Native model: recomputes without suppressed/failed unexpected features or dangling references.
- B-rep: valid topology, expected solid/shell count, positive volume where intended, consistent orientation, and no unintended open boundaries.
- Mesh: watertight/manifold when required, oriented normals, no self-intersections, degenerate faces, isolated fragments, or nonfinite coordinates; record tessellation tolerance.
- DXF/DWG: supported entity types, explicit units, expected layers/layouts, no corrupt blocks or unsupported proxy objects that affect the review.
- PDF/image: classify vector/raster/mixed and record extraction/OCR confidence.

Do not run downstream exact-geometry rules on a representation that failed its preconditions.
Run the native CAD/EDA application's own geometry checker, rebuild, DRC, or ERC when available. External scripts add targeted evidence; they do not replace a required native-tool verification run.

### Gate 2: universal geometry DRC

- Open or self-intersecting profiles, duplicate/coincident entities, zero-length edges, sliver faces, zero-thickness regions, unintended overlaps, disconnected material, and accidental extra bodies.
- Bounding box, mass/volume where justified, symmetry, concentricity, tangency, parallel/perpendicular intent, pattern count/pitch, and critical dimensions.
- Minimum distance, thickness, radius, angle, and feature size only against supplied/applicable thresholds.
- Imported geometry unit/orientation sanity and comparison against at least one known dimension.

### Gate 3: drawing DRC

- Projection method, view identity/alignment, 2D/3D and cross-view consistency, section truth, hidden/center lines, and feature multiplicity.
- Dimensions agree with geometry; no duplicate, contradictory, stale, detached, closed-chain, or visually ambiguous requirements.
- Fits, tolerances, datum references, feature-control frames, surface texture, notes, material, scale, revision, and title-block data are complete only when justified.
- Text, symbols, fonts, lineweights, hatches, viewports, and plot scale survive final export.
- Manufacturing and inspection information is sufficient for the intended release scope; unresolved data is explicit.

### Gate 4: assembly and motion DRC

- Expected component/body count and intended connectivity graph.
- Mate/constraint convergence, remaining degrees of freedom, stable mating datums, axis alignment, and interface orientation.
- Broad-phase candidate detection followed by exact/narrow-phase interference; distinguish contact from positive-volume penetration.
- Minimum clearances, tolerance stack, press/transition/clearance fit intent, fastener access, insertion/removal path, and service envelope.
- Motion at rest, midpoint, limits, and coupled/mirrored states. For discrete collision checks, record step size and tunneling risk.
- Every cable, tube, fastener, bearing, seal, and purchased component has a plausible receiving/retention interface.

### Gate 5: process-specific DFM

Load only rules applicable to the selected process.

#### CNC machining

- Tool access and orientation, internal corner radius versus actual tool radius, pocket/slot depth-to-width or tool reach, minimum web/wall under cutting load, drill depth and breakout, thread depth/relief, undercuts/special tooling, setup/fixturing access, deburring, and inspectability.

#### Sheet metal and 2D cutting

- Constant thickness, valid bend radius and direction, minimum flange, bend relief, hole-to-edge/bend distances, bend collision, flat-pattern validity, grain direction when relevant, closed cut profiles, no duplicates/overlaps, kerf/process layers, minimum feature/web, and part nesting separation.

#### Additive manufacturing

- Build volume/orientation, minimum wall and feature, hole compensation/clearance, overhang/support threshold, bridge span, support removal, trapped resin/powder volumes and drains, enclosed voids, bed contact, mesh manifoldness, and slicer/profile compatibility.

#### Injection molding and casting

- Pull/parting direction, core/cavity side, draft, undercuts and side actions, wall thickness/uniformity, thick transitions and sink/warp risk, ribs/bosses, shutoffs, radii, gate/ejection/tool access where data exists, and supplied shrink/machining allowances.

#### Fabrication and welding

- Joint access, fit-up gaps, weld tool/torch access, distortion-sensitive geometry, edge preparation, standard stock availability, bend/roll feasibility, fixture access, and post-weld machining/inspection allowances.

Geometry alone can flag process risk; it does not predict mold flow, distortion, residual stress, print quality, cutting force, or tool life without appropriate analysis.

### Gate 6: export and release

- Generate explicit deliverables from the authoritative source.
- Reopen/re-import each critical exchange artifact and compare units, envelope, body/component count, hierarchy, orientation, and critical measurements.
- Review plotted PDF/images and 3D review views for clipping, missing symbols/fonts, stale geometry, wrong visibility, and presentation errors.
- Confirm the original/source, derived artifacts, revision identifiers, DRC report, and `NOT_EVALUATED` items are traceable.
- Prefer a structured conversion/status report as the automation contract. Read detailed logs only when the status report is incomplete or failed; a zero exit code without the expected output and evidence is not success.

## Incremental and Full DRC

- After a local edit, run the cheapest checks that cover the changed feature and its dependents: sketch/profile validity, affected dimensions, neighboring clearances, cross-view projection, and local plot/render.
- Run expensive full topology, all-body interference, all-view regeneration, and release export checks once the geometry stabilizes or whenever a global parameter/coordinate system changes.
- Cache evidence by input content hash, configuration, rule-deck version, and validator version. Invalidate only affected results.
- Stop when all applicable release-blocking rules pass and every remaining warning or `NOT_EVALUATED` item is disclosed. Repeating an unchanged passed check adds no confidence.

## Independent Verification

Use a second route for critical requirements:

- Sum independent segments and compare with the overall dimension.
- Project the 3D model into a drawing view and compare with native 2D geometry.
- Recompute clearance from mating surfaces rather than rereading a dimension object.
- Compare source and re-imported exchange geometry.
- Test rule boundaries with just-below, exactly-at, and just-above threshold fixtures when creating or changing a validator.
- Include an invalid-geometry fixture to prove precondition gating.

Independence means a different calculation path or representation, not running the same command twice.

## DRC Report

Use a machine-readable table or JSON plus a concise human summary. Each finding must include:

```text
rule_id:
scope/configuration:
status: PASS | FAIL | WARNING | NOT_EVALUATED | ERROR
severity:
requirement_source:
measured:
threshold_and_inclusivity:
margin:
units:
location_or_entities:
method_and_tolerance:
evidence:
limitations:
recommended_action:
```

Lead with release blockers, then warnings and unevaluated scope. Never replace measurements with a numeric score, and never claim certification unless an authorized process and reviewer actually provided it.
