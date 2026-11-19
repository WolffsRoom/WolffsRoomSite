/* Vita-only Wolff's Room voting endpoint.
 * Cloudflare Durable Object: atomic per-device dedup, retries GitHub audit.
 * No GitHub secrets or device OpenPSID must appear in the VPK or repository.
 */
const BASE="https://wolffsroom.github.io/WolffsRoomSite/polls.json";
const HDR={"Content-Type":"application/json","Cache-Control":"no-store"};
const send=(obj,status=200)=>new Response(JSON.stringify(obj),{status,headers:HDR});
const validId=id=>typeof id==="string" && /^[a-z0-9][a-z0-9-]{1,46}$/.test(id);
const validHash=id=>typeof id==="string" && /^[a-f0-9]{64}$/.test(id);
const asUtc=v=>Date.parse(v.replace(" ","T")+(String(v).endsWith("Z")?"":"-03:00"));

async function pollInfo(id){
  const r=await fetch(BASE,{headers:{Accept:"application/json"},cf:{cacheTtl:60}});
  if(!r.ok)throw new Error("Poll catalog unavailable");
  const j=await r.json();
  return (j.polls||[]).find(p=>p.id===id);
}
async function voterKey(device,poll,salt){
  const key=await crypto.subtle.importKey("raw",new TextEncoder().encode(salt),
                    {name:"HMAC",hash:"SHA-256"},false,["sign"]);
  const bytes=await crypto.subtle.sign("HMAC",key,
                                     new TextEncoder().encode(poll+":"+device));
  return Array.from(new Uint8Array(bytes),x=>x.toString(16).padStart(2,"0")).join("");
}
export default {
 async fetch(req,env){
  const path=new URL(req.url).pathname;
  if(path==="/health")return send({ok:true});
  const results=path.startsWith("/api/v1/results/");
  const vote=path==="/api/v1/vote",status=path==="/api/v1/status";
  if(!results&&!vote&&!status)return send({error:"not_found"},404);
  if((results&&req.method!=="GET")||(!results&&req.method!=="POST"))
    return send({error:"method"},405);
  if(!env.POLL_STATE||!env.VOTER_SALT||!env.GITHUB_TOKEN)
    return send({error:"not_configured"},503);
  let body={};
  if(!results){
    if(Number(req.headers.get("content-length")||0)>2048)return send({error:"too_large"},413);
    try{body=await req.json();}catch{return send({error:"json"},400);}
  }
  const id=results?path.split("/").pop():body.poll;
  if(!validId(id))return send({error:"poll"},400);
  let poll;
  try{poll=await pollInfo(id);}catch{return send({error:"catalog"},503);}
  if(!poll||!Array.isArray(poll.options)||poll.options.length<2||poll.options.length>8)
    return send({error:"not_found"},404);
  const start=asUtc(poll.starts_at),end=asUtc(poll.ends_at),now=Date.now();
  if(!Number.isFinite(start)||!Number.isFinite(end)||end<=start)
    return send({error:"dates"},503);
  if(results&&now<end)return send({error:"not_finished",ends_at:poll.ends_at},403);
  if(vote&&(now<start||now>=end))return send({error:"closed"},403);
  if(!results&&!validHash(body.device))return send({error:"device_hash"},400);
  if(vote&&(!Number.isInteger(body.choice)||body.choice<0||body.choice>=poll.options.length))
    return send({error:"choice"},400);
  const name=env.POLL_STATE.idFromName(id);
  const service=env.POLL_STATE.get(name);
  const payload={mode:results?"results":vote?"vote":"status",id,
    count:poll.options.length,choice:body.choice,closed:now>=end,
    ends_at:poll.ends_at,
    voter:results?null:await voterKey(body.device,id,env.VOTER_SALT)};
  return service.fetch("https://durable.internal/",{method:"POST",headers:HDR,body:JSON.stringify(payload)});
 }
};
export class PollRoom {
 constructor(state,env){this.state=state;this.env=env;}
 async fetch(req){
  const q=await req.json();
  const key="voter/"+q.voter;
  if(q.mode==="status"){
    const found=await this.state.storage.get(key);
    return send({answered:found!==undefined,choice:q.closed&&found?found.choice:null,closed:q.closed,ends_at:q.ends_at});
  }
  if(q.mode==="results"){
    const counts=await Promise.all(Array.from({length:q.count},(_,i)=>this.state.storage.get("count/"+i)));
    const items=counts.map(n=>Number(n||0)),total=items.reduce((a,b)=>a+b,0);
    return send({poll:q.id,closed:true,total,counts:items,
      percentages:items.map(n=>total?Math.round(n/total*10000)/100:0)});
  }
  if(q.mode!=="vote")return send({error:"mode"},400);
  let duplicated=false;
  const auditId=crypto.randomUUID();
  await this.state.storage.transaction(async t=>{
    if((await t.get(key))!==undefined){duplicated=true;return;}
    await t.put(key,{choice:q.choice,created:Date.now()});
    const counter="count/"+q.choice;
    await t.put(counter,Number((await t.get(counter))||0)+1);
    await t.put("audit/"+auditId,{poll:q.id,choice:q.choice,time:Date.now()});
  });
  if(duplicated)return send({answered:true,duplicate:true},409);
  await this.state.storage.setAlarm(Date.now()+1000);
  return send({answered:true,accepted:true,ends_at:q.ends_at},201);
 }
 async alarm(){
  const votes=await this.state.storage.list({prefix:"audit/",limit:32});
  if(!votes.size)return;
  const gh=async(path,body)=>{
    const resp=await fetch("https://api.github.com/repos/"+
          (this.env.GITHUB_REPO||"WolffsRoom/WolffsRoomSite")+path,{
      method:body?"POST":"GET",
      headers:{Authorization:"Bearer "+this.env.GITHUB_TOKEN,
               Accept:"application/vnd.github+json",
               "Content-Type":"application/json",
               "User-Agent":"WolffsRoom-Polls"},
      body:body?JSON.stringify(body):undefined
    });
    if(!resp.ok)throw new Error("GitHub "+resp.status);
    return resp.json();
  };
  try{
    for(const [key,vote] of votes){
      const issueKey="issue/"+vote.poll;
      let issue=await this.state.storage.get(issueKey);
      if(!issue){
        const created=await gh("/issues",{title:"Poll: "+vote.poll,
             body:"Vote log generated by Wolff's Room. Only option and timestamp, no console identifiers."});
        issue=created.number;
        await this.state.storage.put(issueKey,issue);
      }
      await gh("/issues/"+issue+"/comments",
        {body:"Vote: option "+(vote.choice+1)+" at "+new Date(vote.time).toISOString()});
      await this.state.storage.delete(key);
    }
  }catch(e){console.error("Poll audit retry:",String(e));}
  if((await this.state.storage.list({prefix:"audit/",limit:1})).size)
    await this.state.storage.setAlarm(Date.now()+60000);
 }
}
