import assert from 'node:assert/strict';
import {webcrypto} from 'node:crypto';
import worker, {PollRoom} from './worker.mjs';
globalThis.crypto ??= webcrypto;
const oldFetch=globalThis.fetch;
const now=new Date();
const recent=new Date(now.getTime()-86400000);
const future=new Date(now.getTime()+2*86400000);
let poll={id:'sample',starts_at:recent.toISOString().replace('Z',''),
          ends_at:future.toISOString().replace('Z',''),
          options:['A','B','C']};
// String with ISO time + no zone will be interpreted as Brazil time, so
// for deterministic tests supply explicit Z.
poll.starts_at=recent.toISOString();
poll.ends_at=future.toISOString();
let fetched=0;
globalThis.fetch=async url=>{
  fetched++;
  if(url==='https://wolffsroom.github.io/WolffsRoomSite/polls.json')
    return new Response(JSON.stringify({polls:[poll]}),{status:200});
  throw Error('unexpected network: '+url);
};
class Storage {
  constructor(){this.items=new Map();}
  async get(k){return this.items.get(k);}
  async put(k,v){this.items.set(k,v);}
  async delete(k){this.items.delete(k);}
  async transaction(fn){return fn(this);}
  async setAlarm(t){this.alarm=t;}
  async list({prefix='',limit=100}={}){
    return new Map([...this.items].filter(([k])=>k.startsWith(prefix)).slice(0,limit));
  }
}
const storage=new Storage();
const env={
  POLL_STATE:{idFromName:n=>n,get:n=>({fetch:async(url,init)=>{
    const room=new PollRoom({storage},env);
    return room.fetch(new Request(url,init));
  }})},
  VOTER_SALT:'test-only-secret-not-real',GITHUB_TOKEN:'not-used',
};
const device='a'.repeat(64);
const request=async(path,body,environment=env)=>{
  const req=new Request('https://worker.example'+path,{
    method:body?'POST':'GET',
    headers:{'Content-Type':'application/json'},
    body:body?JSON.stringify(body):undefined
  });
  const out=await worker.fetch(req,environment);
  return [out.status,await out.json()];
};
try{
  let [st,data]=await request('/health');
  assert.equal(st,200);
  assert.equal(data.ok,true);
  [st,data]=await request('/api/v1/vote',{poll:'sample',device,choice:0},
                          {...env,VOTER_SALT:undefined});
  assert.equal(st,503);
  [st,data]=await request('/api/v1/vote',{poll:'sample',device,choice:1});
  assert.equal(st,201);assert.equal(data.accepted,true);
  [st,data]=await request('/api/v1/vote',{poll:'sample',device,choice:2});
  assert.equal(st,409);assert.equal(data.duplicate,true);
  [st,data]=await request('/api/v1/status',{poll:'sample',device});
  assert.equal(st,200);assert.equal(data.answered,true);
  [st,data]=await request('/api/v1/results/sample');
  assert.equal(st,403);
  poll.ends_at=new Date(Date.now()-1000).toISOString();
  [st,data]=await request('/api/v1/results/sample');
  assert.equal(st,200);assert.deepEqual(data.counts,[0,1,0]);
  assert.equal(data.total,1);
  assert.equal(data.percentages[1],100);
  [st,data]=await request('/api/v1/vote',{poll:'sample',device:'b'.repeat(64),choice:1});
  assert.equal(st,403);
  assert.equal(storage.items.size,3); // HMAC voter + counter + audit
  assert.ok(fetched>=5);
  console.log('Poll Worker: 10 secure voting/dedup/results checks passed.');
}finally{globalThis.fetch=oldFetch;}
