// Minimal DOM harness; no claim of visual browser or Pine execution validation.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const page=fs.readFileSync('analysis/top500/optimization/index.html','utf8');
const raw=page.match(/<script id="optimization-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const data=JSON.parse(raw),script=page.match(/<script>\n([\s\S]*?)<\/script>/)[1];
class Element{constructor(){this.children=[];this.value='';this.textContent='';this.events={};this.hidden=false}append(...x){this.children.push(...x)}replaceChildren(...x){this.children=x}addEventListener(t,f){this.events[t]=f}}
const els={};for(const id of ['optimization-data','query','status','rows','summary','empty'])els[id]=new Element();
els['optimization-data'].textContent=raw;els.status.value='candidate';
vm.runInNewContext(script,{document:{getElementById:id=>els[id],createElement:()=>new Element()},console});
function input(id,v){els[id].value=v;els[id].events.input()}
assert.equal(data.length,500);assert.equal(els.rows.children.length,data.filter(r=>r.status==='candidate').length);
for(const row of els.rows.children)assert.ok(fs.existsSync('analysis/top500/optimization/'+row.children[0].children[0].href));
input('query','735');assert.equal(els.rows.children.length,1);assert.match(els.rows.children[0].children[0].children[0].textContent,/RSI50/);
input('query','ZZZ-does-not-exist');assert.equal(els.rows.children.length,0);assert.equal(els.empty.hidden,false);
input('query','');input('status','');assert.equal(els.rows.children.length,500);assert.equal(els.empty.hidden,true);
for(const status of ['needs_design','needs_review','reviewed']){input('status',status);assert.equal(els.rows.children.length,data.filter(r=>r.status===status).length)}
console.log('PASS: 500 records, default approved candidates, links, SID search, empty state, and status filters. DOM harness only.');
