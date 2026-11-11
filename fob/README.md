# MW4 DMZ — FOB Tactical Explorer

A separate, self-contained browser-based 3D reconstruction project located in `/fob/`. The existing X-01 Tactical Explorer at the repository root is left untouched.

## Open

After GitHub Pages publishes the latest commit:

https://adamjd-bit.github.io/-x01-tactical-explorer/fob/

## Current build

- Procedural 3D woodland encampment based on official FOB overview imagery.
- First-person, third-person and orbit camera modes.
- Keyboard movement (WASD / arrow keys), touch movement pad, drag-to-look and orbit zoom.
- Interactive station directory and station information panels.
- Physical station set dressing: field huts, tented work areas, workbenches, crates, screens, satellite dishes, antennae, trees, rocks, range targets and a transport-helicopter silhouette.
- Reference data separated into `data/fob-reference.json`.

## Evidence and accuracy

The current scene is a navigable reference-led blockout, not a verified 1:1 measured replica. Official Call of Duty screenshots establish the wooded mountain clearing, field structures, station visual language, wooded firing range and helicopter deployment threshold. Exact site dimensions, station coordinates, orientation and paths are not supplied in the public guide and must be measured from continuous in-game footage or screenshots before the geometry can be called exact.

## Primary references

- [Official Call of Duty FOB Intel Guide](https://www.callofduty.com/blog/2026/10/call-of-duty-modern-warfare-4-dmz-how-to-play-forward-operating-base-guide)
- [Official COD POD DMZ First Look — FOB discussion at 27:20](https://www.youtube.com/watch?v=qmkmQ1AWPVE)
- [Official FOB overview image](https://imgs.callofduty.com/content/dam/atvi/callofduty/cod-touchui/blog/body/mw4/dmz-fob/MW4-DMZ-FOB-002.webp)
- [Official station examples — Operators, Orders, Stash, Bounty Board](https://imgs.callofduty.com/content/dam/atvi/callofduty/cod-touchui/blog/body/mw4/dmz-fob/MW4-DMZ-FOB-004.webp)
- [Official station examples — Printer, Boss Board, Vendor, Gunsmith](https://imgs.callofduty.com/content/dam/atvi/callofduty/cod-touchui/blog/body/mw4/dmz-fob/MW4-DMZ-FOB-005.webp)

## Next reconstruction pass

1. Capture a continuous, slow FOB walkthrough from the game, including the entrance, all turns, every station and the firing range.
2. Extract reference frames and establish a measured top-down site plan.
3. Replace provisional station positions and dimensions with measured geometry.
4. Refine individual station props and materials against the official screenshots and in-game captures.
5. Validate first-person collision, sightlines, touch controls and performance on iPhone Safari.
