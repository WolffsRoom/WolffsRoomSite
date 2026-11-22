// Site-only anonymous aggregate visitor statistics for Wolff's Room.
// Does not store IP addresses, user agents, cookies, or account identifiers.
const ORIGIN = "https://wolffsroom.github.io";
const JSON_HEADERS = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store, max-age=0",
  "Access-Control-Allow-Origin": ORIGIN,
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Vary": "Origin"
};
const reply = (data, status=200) => new Response(JSON.stringify(data), {status,headers:JSON_HEADERS});
const token = (v) => typeof v === "string" && /^[0-9a-f-]{36}$/.test(v) &&
  /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(v);
const dayKey = (ms) => new Date(ms - 3*3600000).toISOString().slice(0,10);
export default {
  async fetch(request, env) {
    const path = new URL(request.url).pathname;
    const origin = request.headers.get("Origin");
    if (path !== "/api/visitors" && path !== "/api/visitors/visit") return reply({error:"not_found"},404);
    if (request.method === "OPTIONS") return origin === ORIGIN
      ? new Response(null,{status:204,headers:JSON_HEADERS})
      : reply({error:"origin"},403);
    if (origin && origin !== ORIGIN) return reply({error:"origin"},403);
    if (path.endsWith("/visit") && (request.method !== "POST" || origin !== ORIGIN))
      return reply({error:"method_or_origin"},403);
    if (!path.endsWith("/visit") && request.method !== "GET") return reply({error:"method"},405);
    let body = {};
    if (request.method === "POST") {
      if (Number(request.headers.get("content-length") || 0)>500) return reply({error:"too_large"},413);
      try { body = await request.json(); } catch { return reply({error:"invalid_json"},400); }
      if (!token(body.visitor) || !token(body.session)) return reply({error:"invalid_id"},400);
    }
    const id=env.VISITORS.idFromName("site");
    return env.VISITORS.get(id).fetch("https://internal.local/", {
      method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({mode:request.method==="POST"?"visit":"read", ...body})
    });
  }
};
export class VisitorStats {
  constructor(ctx) { this.ctx=ctx; }
  async fetch(request) {
    const q=await request.json();
    const store=this.ctx.storage;
    const now=Date.now(), day=dayKey(now), cutoff=now-5*60000;
    if(q.mode==="visit"){
      await store.transaction(async t => {
        const visitor="unique/"+q.visitor, session="session/"+q.session, daily="day/"+day+"/"+q.visitor;
        if(await t.get(visitor)===undefined){
          await t.put(visitor,now);
          await t.put("total_unique",Number(await t.get("total_unique")||0)+1);
        }
        if(await t.get(session)===undefined) {
          await t.put(session,now);
          await t.put("total_visits",Number(await t.get("total_visits")||0)+1);
          await t.put("visits/"+day,Number(await t.get("visits/"+day)||0)+1);
        }
        if(await t.get(daily)===undefined) {
          await t.put(daily,now);
          await t.put("unique/"+day,Number(await t.get("unique/"+day)||0)+1);
        }
        await t.put("active/"+q.visitor, now);
      });
    }
    // "Online" means anonymous browser IDs that pinged in the last 5 minutes.
    const active=await store.list({prefix:"active/"});
    let online=0;
    for(const [key,last] of active){
      if(Number(last)>=cutoff) online++;
      else await store.delete(key);
    }
    return reply({
      visits:Number(await store.get("total_visits")||0),
      unique:Number(await store.get("total_unique")||0),
      today:Number(await store.get("visits/"+day)||0),
      todayUnique:Number(await store.get("unique/"+day)||0),
      online, day, onlineWindowMinutes:5,
      started:"2026-11-22"
    });
  }
}
