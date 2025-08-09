# Army Command Simulator (Prototype)

This is the first-iteration prototype of a battalion-scale army command simulator built with **Python + Pygame**.

- **Map:** 100×100 grid (each cell is one battalion’s footprint).  
- **Window:** 800×800 (8 px per cell).  
- **Turn length:** constant defined as 30s, but this build runs continuously; use **Space** to pause/resume.  
- **Forces:** Two opposing armies spawn within 30 cells of their starting edges with 50 random battalions + 1 HQ each.  
- **Unit types:** infantry, mech_infantry, tank, artillery, air_defense, drone (each with speed/range/attack/defense/HP).  
- **HQs:** Marked in yellow; behave like infantry for now (no C2 buffs yet).  
- **Behavior:** Each battalion automatically moves toward or fires at the nearest enemy. Damage is `attack - defense` (min 0).  
- **Victory conditions, fog-of-war, doctrinal OOB, formations, NATO symbology:** not implemented yet (roadmap below).

## Controls
- **Space** — Pause/Resume
- **Close window** — Quit

## Requirements
- Python 3.9+
- Pygame

Install dependencies:
```bash
pip install -r requirements.txt
```

## Run
```bash
python army_command_sim.py
```

## Current Rules/Model
- Movement and range are Euclidean in grid cells.
- No stacking/occupancy limits or pathfinding; units can overlap.
- Artillery and air defense use the same direct-fire model (to be expanded).
- Units are removed upon HP ≤ 0.

## Roadmap (next steps)
1. **30-second turn gating** with an on-screen **Continue** button that advances the simulation one turn at a time.
2. **Recon/fog-of-war:** Observer has omniscience; sides get delayed/periodic misidentification and partial visibility only.
3. **Victory conditions:** Implement the win rule—at least 20% of winners reach the opposite edge and either enemy HQ is destroyed or >50% of enemy units destroyed.
4. **Doctrinal OOBs & formations:** Chinese Group Army vs Russian Combined Arms Army (or US Corps) with brigade/division/army HQs, frontage/depth, and realistic unit mixes.
5. **Role-based AI:** Artillery holds standoff positions, AD covers high-value nodes, drones scout, counter-battery behavior, etc.
6. **NATO/wargame symbology** and unit labels/health indicators.
7. **Logistics/morale/command delay** and stacking/ZOC.
8. **Scenario files** for quick setup of different force structures and starting layouts.

## License
MIT
