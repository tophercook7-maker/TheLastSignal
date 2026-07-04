# THE LAST SIGNAL

## What It Is
- **Genre:** Multiplayer text-based suspense adventure
- **Tone:** Clean, atmospheric, technical. No horror, no blood, no profanity.
- **Premise:** 5 research stations receive an identical signal. Satellite links die hours later. You must cooperate across stations before a global deadline.
- **Sessions:** ~6 hours in-game, playable in 20-45 minute real chunks
- **Endings:** Multiple outcomes based on collective choices
- **Style:** Warm dark terminal. Mobile-first.

## How to Play
1. Open `live/index.html` in browser
2. Pick a station
3. Share your callsign with teammates
4. Coordinate through BroadcastChannel (same network)
5. Each station has private intel + public actions
6. Some puzzles require 2+ stations active simultaneously

## Stations
- **AURORA-7** — Arctic research base, communications specialist
- **PINNACLE** — Mountain observatory, signal analyst
- **MERIDIAN** — Desert geophysics lab, data decryptor
- **TRIDENT** — Oceanic platform, systems engineer
- **HELIX** — Orbital relay, mission coordinator

## Tech Stack
- Vanilla JS, no build tools
- BroadcastChannel for multiplayer sync
- localStorage for save/load
- Responsive CSS for mobile/desktop

## File Structure
```
index.html            <- Main entry
live/
  game.js            <- Game engine + station content
  css/main.css       <- Theme
  assets/            <- Audio, icons
```

## Future Expansion
- Add TRIDENT, HELIX stations
- New signal types, corrupted data events
- Voice/text inter-station comms
- Standalone desktop build with Tauri
- Mobile app wrapper
