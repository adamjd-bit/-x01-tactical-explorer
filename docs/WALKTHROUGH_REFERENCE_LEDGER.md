# X01 walkthrough reference ledger

This ledger records public gameplay references used to guide the Blender reconstruction. It separates observed/guide-confirmed features from geometry that still needs direct frame-by-frame measurement.

## Primary gameplay video references

- **Deep Vault full run:** The Based Otaku, embedded YouTube video ID `b5e-8V1M3f0`, starting at approximately 5:57 in the article player. Direct video: https://www.youtube.com/watch?v=b5e-8V1M3f0
  - Walkthrough documents the vault entrance keypad, central elevator, multiple vault levels, numbered keycard rooms, top-level Core Room, Blix encounter, Argonaut armour rack and emergency escape shaft/zipline.
  - Companion guide: https://thebasedotaku.com/guides/mw4-dmz-x01-deep-vault-full-walkthrough/
- **X01 launch / full map guide:** MrDalekJD, *MW4 DMZ "X01" ULTIMATE GUIDE: EVERYTHING EXPLAINED!* (18:04). The video is listed in the creator's public video catalogue; use it as a broad traversal reference, not as a measured floor plan.
  - Creator video catalogue: https://trari.com/en/c/mrdalekjd/
- **X01 launch gameplay:** MrDalekJD, *NEW MW4 DMZ SEASON 1 MAP "X01" GAMEPLAY LIVE!* (3:38:55). Long-form footage is useful for repeated room approaches and environmental context.
  - Creator video catalogue: https://trari.com/en/c/mrdalekjd/

## Written/map cross-checks

- Activision Season 1 environment brief: https://www.callofduty.com/blog/2026/10/call-of-duty-modern-warfare-4-warzone-season-1-announcement
- COD Central X01 map and floor labels: https://codcentral.net/blog/mw4-dmz-map/
- DMZ Codex X01 interactive map: https://dmzcodex.com/map/x01-black-site/
- DMZMap X01 tactical map: https://dmzmap.com/x01/map
- MetaRadar X01 guide, updated 10 November 2026: https://metaradar.gg/modernwarfare4/dmz/x01

## Geometry implications now represented in Blender

- Deep Vault: a central elevator, three visible gallery tiers, numbered compartment doors, a central core feature and a separate emergency escape/zipline shaft. This is a visual interpretation of the walkthrough sequence; exact dimensions and tier elevations remain unmeasured.
- Production Assembly: weapons conveyor/gantry plus the distinctive X01 3D printer and build chamber.
- Motor Pool: armoured vehicle silhouettes in marked vehicle bays.
- Cargo / Main Warehouse: stacked ribbed freight containers and storage lanes.
- Data Center / Control Room: server racks and operator consoles.

## Confidence and limitations

The guides establish the presence and functional relationships of named spaces and distinctive props. They do **not** provide reliable measured dimensions, exact wall coordinates, ceiling heights, or a complete continuous survey of every corridor. Current grid positions are sector anchors only. Do not label the reconstruction as a pixel-perfect or dimensionally exact game extraction.

Next validation pass: inspect the long-form X01 walkthrough at room entrances and transitions, then record approximate room width/depth, doorway offsets, ceiling height, corridor bends, stairs/landings, lighting placement and landmark prop locations. Update the model in coherent sector batches rather than adding isolated decorative objects.
