const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const page=fs.readFileSync('analysis/top500/index.html','utf8');
const raw=page.match(/<script id="ranking-data" type="application\/json">([\s\S]*?)<\/script>/)[1],data=JSON.parse(raw);
const script=page.match(/<script>\n([\s\S]*?)<\/script>/)[1];
class Element{constructor(){this.children=[];this.value='';this.textContent='';this.events={};this.disabled=false;this.hidden=false}append(...x){this.children.push(...x)}replaceChildren(...x){this.children=x}addEventListener(t,f){this.events[t]=f}}
const els={};for(const id of ['ranking-data','query','category','cohort','positive','detail','sort','rows','summary','empty','page','prev','next'])els[id]=new Element();
els['ranking-data'].textContent=raw;els.sort.value='rank';
vm.runInNewContext(script,{document:{getElementById:id=>els[id],createElement:()=>new Element()},console});
function input(id,v){els[id].value=v;els[id].events.input()}
assert.equal(data.length,500);assert.equal(els.rows.children.length,50);
const first=els.rows.children[0].children[0].children[0];assert.ok(fs.existsSync('analysis/top500/'+first.href));
els.next.events.click();assert.equal(els.page.textContent,'2 / 10');
input('query','ZZZ-nonexistent-xyz');assert.equal(els.rows.children.length,0);assert.equal(els.empty.hidden,false);
input('query','');input('cohort','screening50');assert.equal(els.rows.children.length,49);assert.ok(els.rows.children.every(tr=>tr.children[1].textContent.endsWith('补充')));
input('cohort','full_daily');assert.match(els.summary.textContent,/匹配 451 /);
input('positive','yes');assert.match(els.summary.textContent,new RegExp('匹配 '+data.filter(r=>r.cohort==='full_daily'&&r.cagr>0).length+' '));
input('positive','');input('cohort','');input('detail','reviewed');assert.equal(els.rows.children.length,data.filter(r=>r.detail_level.includes('源码精读')).length);
assert.ok(data.slice(0,20).every(r=>r.detail_level.includes('源码精读')));
input('detail','');input('sort','cagr');assert.ok(els.rows.children.every(tr=>tr.children[2].textContent.endsWith('全市场日线')));
input('category',data[0].category);assert.ok(els.rows.children.every(tr=>tr.children[2].textContent.startsWith(data[0].category+' / ')));
console.log('PASS: ranking data, links, pagination, search, cohort, positive return, review/category filters, and evidence-tier sorting. DOM harness only.');
