/* THE LAST SIGNAL — relay.js
   Tiny WebSocket relay so crewmates can join a mission by share-code from
   ANYWHERE. It just fans messages out to everyone else in the same room and
   keeps a live roster. No game logic lives here — the clients are authoritative.

   Run locally:      node server/relay.js         (ws://localhost:8790)
   Then in the game: set  MC.RELAY_URL = "ws://localhost:8790"  (see index note)
   Deploy anywhere that gives you a public wss:// URL (Fly.io, Render, a VPS,
   a Cloudflare tunnel to this process) and point MC.RELAY_URL at it.
   Only dependency: `ws`  →  cd server && npm install
*/
"use strict";
const http = require("http");
const fs = require("fs");
const { WebSocketServer } = require("ws");
const PORT = process.env.PORT || 8790;

let DEMO_VIDEO = null;
try { DEMO_VIDEO = fs.readFileSync(__dirname + "/demo.mp4"); } catch (e) {}

const PAGE = (title, body) => `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title>
<style>body{background:#05070d;color:#c9d6ee;font-family:-apple-system,system-ui,sans-serif;
max-width:720px;margin:0 auto;padding:40px 22px;line-height:1.6}h1,h2{color:#8be9ff}
a{color:#8be9ff}code{color:#a78bfa}hr{border:0;border-top:1px solid #1e2b45;margin:24px 0}
.sub{color:#6b7d9e}</style></head><body>${body}</body></html>`;

const PRIVACY_HTML = PAGE("Privacy Policy — Answering the Dark", `
<h1>Privacy Policy — Answering the Dark</h1><p class="sub">Last updated: 2026-07-10</p>
<p><b>Answering the Dark</b> is a single-player and cooperative game by Topher Cook, built to collect as little as possible.</p>
<h2>What we collect</h2><p><b>Nothing personal.</b> No accounts, no logins, no ads, no analytics or tracking SDKs.</p>
<ul><li><b>Solo play</b> happens entirely on your device. No data leaves it.</li>
<li><b>Multiplayer</b> uses a share-code. When you host or join a mission, the app connects to our relay and exchanges only <i>gameplay messages</i> (a chosen callsign, the room code, in-game actions) so crewmates see the same mission. These are relayed in real time to others in your room and are <b>not stored, logged, sold, or used to identify you.</b> When the mission ends or you disconnect, they're gone.</li></ul>
<h2>What we do NOT collect</h2><p>No name, email, phone number, contacts, location, photos, advertising identifiers, or usage analytics.</p>
<h2>Children</h2><p>Safe for a general/teen audience: no violence, no profanity, no objectionable content, and no data collection.</p>
<h2>Third parties</h2><p>The multiplayer relay is hosted on Fly.io purely to pass messages between players in the same room. No data is shared with advertisers or data brokers.</p>
<h2>Contact</h2><p>Questions? Email <a href="mailto:topher.cook7@gmail.com">topher.cook7@gmail.com</a>.</p>
<hr><p class="sub"><a href="/">← Answering the Dark</a></p>`);

const LANDING_HTML = PAGE("Answering the Dark", `
<h1>Answering the Dark</h1>
<p>A first-contact ops game. You are Deepwatch — humanity's deep-space mission control.
Your vessel AURORA hears a signal from where nothing should be. Decode it, understand it,
and decide what to say back.</p>
<p class="sub">This server is the game's multiplayer share-code relay.</p>
<hr><p><a href="/privacy">Privacy Policy</a></p>`);

const server = http.createServer((req, res) => {
  const url = (req.url || "/").split("?")[0];
  if (url === "/privacy") { res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" }); return res.end(PRIVACY_HTML); }
  if (url === "/health")  { res.writeHead(200, { "Content-Type": "text/plain" }); return res.end("ok"); }
  if (url === "/demo.mp4" && DEMO_VIDEO) {
    res.writeHead(200, { "Content-Type": "video/mp4", "Content-Length": DEMO_VIDEO.length });
    return res.end(DEMO_VIDEO);
  }
  res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" }); res.end(LANDING_HTML);
});
const wss = new WebSocketServer({ server });
const rooms = new Map(); // room -> Set<ws>

const roster = (room) =>
  [...(rooms.get(room) || [])].filter(c => c.meta).map(c => ({ role: c.meta.role, name: c.meta.name }));
const broadcast = (room, obj, except) => {
  const msg = JSON.stringify(obj);
  for (const c of rooms.get(room) || []) if (c !== except && c.readyState === 1) c.send(msg);
};
const sendRoster = (room) => broadcast(room, { type: "roster", roster: roster(room) });

wss.on("connection", (ws) => {
  ws.on("message", (raw) => {
    let m; try { m = JSON.parse(raw); } catch { return; }
    if (m.type === "join") {
      ws.meta = { room: m.room, role: m.role, name: m.name, from: m.from };
      if (!rooms.has(m.room)) rooms.set(m.room, new Set());
      rooms.get(m.room).add(ws);
      sendRoster(m.room);
      broadcast(m.room, { type: "log", who: "SYS", text: `${m.name || m.role} joined as ${m.role}.` }, ws);
      return;
    }
    if (ws.meta) broadcast(ws.meta.room, m, ws); // relay everything else to the room
  });
  ws.on("close", () => {
    const r = ws.meta && ws.meta.room;
    if (r && rooms.has(r)) { rooms.get(r).delete(ws);
      if (!rooms.get(r).size) rooms.delete(r); else sendRoster(r); }
  });
});
server.listen(PORT, () => console.log(`[Deepwatch relay] http + ws on :${PORT}`));
