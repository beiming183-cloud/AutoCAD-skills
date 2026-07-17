# Example: Consumer Product Concept Gate

This example shows the expected decision structure, not a finished product design.

## User request

```text
Design a compact desktop cable organizer with six AC outlets, two USB-C ports,
a rotating upper module, one power inlet, and a single external cable.
```

## Required intake before detailed CAD

| Field | Example status |
| --- | --- |
| People | Office users; reach/strength population is `TBD` |
| Scenarios | Setup, daily plug/unplug, rotation, cleaning, transport |
| Interfaces | 6 AC, 2 USB-C, 1 inlet; exact purchased modules are `TBD` |
| Actions | Plug, unplug, rotate, reset, lift, route cable |
| Cable direction | Rear exit preferred; bend radius and strain relief are `TBD` |
| Product intent | Quiet desktop object; compact footprint; no exposed cable loop |

`CONSUMER_CONCEPT_GATE` remains blocked until the scope-defining `TBD` items are either resolved or explicitly kept outside the concept comparison.

## Three low-cost concepts

| Concept | Distinguishing idea | Benefit | Main risk |
| --- | --- | --- | --- |
| A: low radial base | Outlets around a wide stationary base; USB-C on top | Stable, short reach | Large desk footprint |
| B: vertical tower | Outlets on two vertical faces; rotating top control ring | Small footprint | Tip risk and cable torque |
| C: split wedge | Angled outlet banks with a fixed center hub | Clear access and cable separation | More enclosure parts |

Each concept needs the same-scale outline, port directions, hand/cable context, support footprint, purchased-module envelopes, and safety keep-outs. A color-only option does not count.

## Safety gate

Because the product contains mains and a rotating module, `MAINS_SAFETY_GATE` is triggered. Before internal detail, the project needs a qualified owner and preliminary decisions for:

- Supply topology, intended markets, product category and applicable standards.
- Protective class, grounding or reinforced-insulation boundary.
- Isolation, creepage/clearance rule source, fire enclosure and materials.
- Overcurrent, stall, abnormal operation, touch access and strain relief.
- Rotation limit, cable twisting, pinch/entanglement zones and service lockout.
- Certification-critical outlet, inlet, supply, USB-C and switch modules.

Until then, the valid output is an exterior concept plus hazard and keep-out envelopes. It must not be labeled safe, certified, or manufacturing-ready.

## Early preview

After the user selects a concept, generate a parameterized skeleton and immediately review:

- Human/product scale and overall proportion.
- All nine interfaces and their mating directions.
- Hand access and plug removal paths.
- Cable exit, bend, strain relief and rotation conflict.
- Support polygon, estimated mass uncertainty and obvious tipping risk.

Only after the preview and applicable gates pass should detailed ribs, fasteners, vents, fillets, dimensions, and manufacturing annotations begin.
