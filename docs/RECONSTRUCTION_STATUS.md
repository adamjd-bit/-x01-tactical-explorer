# X01 Black Site reconstruction notes

## Scope

This is a reference-led, original 3D reconstruction of the X01 Black Site. It is not extracted game geometry and does not claim to contain Activision's proprietary models or textures.

## Verified environment brief

The official Call of Duty Season 1 announcement describes X01 as a former GRANIT Arms weapons facility with dimly lit labyrinthine passageways, tunnels, linking chambers, a weapons assembly line, cargo bays, vehicle depots, underground labs, production lines and a sealed Deep Vault.

Official source:
- https://www.callofduty.com/blog/2026/10/call-of-duty-modern-warfare-4-warzone-season-1-announcement

## Map references

- COD Central X01 floor map (updated 12 November 2026): https://codcentral.net/blog/mw4-dmz-map/
- DMZ Codex X01 interactive map: https://dmzcodex.com/map/x01-black-site/
- DMZMap X01 Tac-Map reference: https://dmzmap.com/x01/map
- DMZHUB X01 key-room and location reference: https://dmzhub.gg/maps/x01-black-site

Grid squares are reference anchors, not measured room footprints. Community sources disagree on some area and key-room sectors. Conflicts are recorded in data/x01-map-data.json and must be resolved against in-game screenshots or footage before geometry is described as exact.

## Material pipeline

The Blender build attempts to download real photographic PBR maps from Poly Haven for concrete, concrete floor, rusty painted metal and corrugated iron. Poly Haven assets are CC0. If the API or download is unavailable, the builder falls back to procedural Blender shader materials.

Poly Haven asset library:
- https://polyhaven.com/a/concrete
- https://polyhaven.com/a/concrete_floor_01
- https://polyhaven.com/a/rusty_painted_metal
- https://polyhaven.com/a/corrugated_iron
- https://polyhaven.com/our-api

The web viewer credits Poly Haven. Downloaded textures are embedded in the exported GLB and packed into the Blender project.

## Reconstruction principles

1. Preserve confirmed sector anchors and source provenance.
2. Do not infer exact wall runs, room dimensions, door locations or corridor routes from a sector grid.
3. Use in-game screenshots and continuous walkthrough footage to measure room proportions, materials, fixtures, lighting and adjacency.
4. Use original manually modelled geometry and licensed photographic materials; do not substitute AI-generated environment textures.
5. Keep the web viewer's floor switching, orbit view and first-person controls working as the Blender environment improves.

## Current status

The current Blender builder is an architectural blockout with room-specific set dressing, structural bulkheads, corridor runs, service details and a procedural/photographic PBR material pipeline. It is a first reconstruction pass, not yet a one-to-one recreation. The next geometry pass requires direct interior gameplay references to calibrate dimensions and layout.
