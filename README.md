# THE LAST SIGNAL
### An ops game of first contact, done right. (v0.1 — Act I playable)

You are **Deepwatch**, humanity's deep-space mission control. Four billion km out, your
survey vessel **AURORA** picks up a clean, patterned signal from a stretch of charted-empty
space *where nothing should be*. It isn't noise. It isn't a weapon. Something has been waiting
a very long time — and it just noticed us. Answer it **right**.

**Tone:** hopeful & wondrous. No violence, no gore, no profanity. The tension is *don't blow
the most important hello in human history.* See **[STORY_BIBLE.md](STORY_BIBLE.md)** for the full arc.

## Play
Open **`live/index.html`** in a browser (or launch via `~/Games` → Play Games.app once wired), then:
- **▸ SOLO** — you're Flight Director; your made-up crew (Sparrow/Comms, Compass/Nav, Amp/Power,
  Halo/Science) staffs the consoles, feeds you readings, and looks to you for the call.
- **▸ HOST** — get a 5-letter share-code; up to 4 friends join and each own a console.
- **▸ JOIN** — type a code to take an open console.

Everyone sees the same **mission feed** and gauges (Understanding · Ship Power · Crew Morale);
each console owns a different piece of the puzzle, so you win by *talking to each other*.

## Gameplay gears (the op feels different each act)
- **Act I — Contact** *(DISCOVER → DECODE → DEDUCE)* — **playable now.** Hear it, decode it
  (primes!), triangulate the impossible source, prove it's alive, survive a gift of power you
  can't hold, and decide: run, or hold and say hello.
- **Act II — The Long Listen** *(coordinate under pressure)* — *in development.*
- **Act III — The Answer** *(compose & decide together)* — *in development.*

## Multiplayer: join from anywhere (share-code relay)
Same-device / same-browser multiplayer works with **zero setup** (BroadcastChannel).
For **join-from-anywhere**, run the tiny relay and point the client at it:
```bash
cd server && npm install && npm start      # ws://localhost:8790
```
Then set `MC.RELAY_URL = "ws://localhost:8790"` (or your deployed `wss://…` URL) before the
game scripts load. Deploy `server/relay.js` anywhere that gives a public `wss://` URL
(Fly.io / Render / a VPS / a Cloudflare tunnel) for true play-from-anywhere.

## File structure
```
STORY_BIBLE.md          <- the full story + design (our collaboration doc)
live/
  index.html            <- Deepwatch mission-control shell
  css/mc.css            <- mission-control theme
  mc/
    net.js              <- transport (solo / local / share-code relay)
    crew.js             <- the made-up crew personalities
    act1.js             <- ACT I content (beats, puzzles, choices)
    engine.js           <- runtime (lobby, beats, gauges, sync)
  legacy/               <- the original 5-stations game (preserved, still playable)
server/
  relay.js              <- share-code WebSocket relay (join from anywhere)
```

## Next
Share-code relay deploy → Acts II & III → art/sound/music beds → package in the Tauri shell.
Open questions for the story are at the bottom of STORY_BIBLE.md.
