# MW4 DMZ — FOB Tactical Explorer

A separate browser-based 3D reconstruction in `/fob/`. The existing X-01 Tactical Explorer at the repository root is kept separate.

## Open

GitHub Pages URL (deployment must be checked independently):
https://adamjd-bit.github.io/-x01-tactical-explorer/fob/

## Current reconstruction

- Procedural 3D woodland encampment with an autumn woodland palette and mountain/rock perimeter.
- Rough central access track with uneven flagstone and cracked-concrete ground details.
- Open-sided vehicle maintenance shelter with two tactical vehicle blockouts, based on official environment imagery.
- Field huts, tents, workstations, storage crates, screens, satellite dishes, solar panels, antennae, field lights and utility props.
- Firing-range lane with targets arranged at increasing distances.
- Razor-wire deployment threshold and transport-helicopter silhouette.
- Thirteen physical FOB station entries, matching the official guide's enumerated station list.
- Orbit, first-person and third-person camera modes.
- WASD / arrow movement, drag-to-look, orbit zoom and mobile touch movement controls.
- Station directory and proximity-based interaction panels.

## Official reference basis

- [Official Call of Duty FOB Intel Guide](https://www.callofduty.com/blog/2026/10/call-of-duty-modern-warfare-4-dmz-how-to-play-forward-operating-base-guide)
- [Official COD POD DMZ First Look](https://www.youtube.com/watch?v=qmkmQ1AWPVE)
- [FOB overview image — MW4-DMZ-FOB-002](https://imgs.callofduty.com/content/dam/atvi/callofduty/cod-touchui/blog/body/mw4/dmz-fob/MW4-DMZ-FOB-002.webp)
- [FOB field environment — MW4-DMZ-FOB-003](https://imgs.callofduty.com/content/dam/atvi/callofduty/cod-touchui/blog/body/mw4/dmz-fob/MW4-DMZ-FOB-003.webp)
- [FOB station examples — MW4-DMZ-FOB-004](https://imgs.callofduty.com/content/dam/atvi/callofduty/cod-touchui/blog/body/mw4/dmz-fob/MW4-DMZ-FOB-004.webp)

## Accuracy status

The official sources establish the overall woodland clearing, small field structures, station types, vehicle shelter, firing range and deployment threshold. They do not publish a measured site plan. Therefore, the current scene is a reference-led navigable blockout, not a verified 1:1 replica. Exact dimensions, station positions, paths and prop placement still need to be measured from a continuous in-game walkthrough.

## Next reconstruction pass

1. Capture a continuous slow walkthrough from the FOB entry, covering all paths, turns, stations, vehicle shelter, firing range and deploy threshold.
2. Extract reference frames and construct a measured top-down site plan.
3. Replace provisional station coordinates and structure dimensions with measured geometry.
4. Rebuild each station's specific furniture, screens, racks and equipment against the in-game captures.
5. Validate collision, sightlines, camera modes, touch controls and performance in iPhone Safari.
