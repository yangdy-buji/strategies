// Execute the generated offline page script against a minimal DOM to test
// filtering/paging/link behavior without any browser or third-party dependency.
const fs=require('node:fs');const vm=require('node:vm');const assert=require('node:assert/strict');
const page=fs.readFileSync('analysis/index.html','utf8');
const dataText=page.match(/<script id="catalog-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const data=JSON.parse(dataText);const script=page.match(/<script>\n([\s\S]*?)<\/script>/)[1];
class Element{constructor(){this.children=[];this.value='';this.textContent='';this.events={};this.disabled=false;this.hidden=false}append(...x){this.children.push(...x)}replaceChildren(...x){this.children=x}addEventListener(type,fn){this.events[type]=fn}}
const elements={};for(const id of ['catalog-data','query','category','review','kind','minimum','sort','dedup','rows','summary','empty','page','prev','next'])elements[id]=new Element();
elements['catalog-data'].textContent=dataText;
Object.assign(elements.review,{value:'源码复核'});elements.kind.value='strategy';elements.minimum.value='0';elements.sort.value='score';elements.dedup.value='yes';
const context=vm.createContext({document:{getElementById:id=>elements[id],createElement:()=>new Element()},console});
vm.runInContext(script,context);
const reviewed=data.filter(r=>r.review_status==='源码复核'&&r.kind==='strategy');
assert.equal(elements.rows.children.length,reviewed.length);assert.equal(reviewed.length,23);
const first=elements.rows.children[0].children[0].children[0];assert.match(first.href,/^cards\/[a-f0-9]{12}\.html$/);assert.ok(fs.existsSync('analysis/'+first.href));
function input(id,value){elements[id].value=value;elements[id].events.input()}
input('query','ZZZ-no-such-strategy-xyz');assert.equal(elements.rows.children.length,0);assert.equal(elements.empty.hidden,false);assert.equal(elements.next.disabled,true);
input('query','');input('minimum','65');assert.ok(elements.rows.children.length>0);for(const tr of elements.rows.children)assert.ok(Number(tr.children[2].textContent.split(' / ')[0])>=65);
input('minimum','0');input('review','自动初审');assert.equal(elements.rows.children.length,50);assert.equal(elements.next.disabled,false);
const initial=elements.rows.children[0].children[0].children[0].href;elements.next.events.click();assert.notEqual(elements.rows.children[0].children[0].children[0].href,initial);assert.equal(elements.prev.disabled,false);
input('category','均值回归');for(const tr of elements.rows.children)assert.ok(tr.children[1].textContent.startsWith('均值回归 / '));assert.ok(elements.page.textContent.startsWith('1 / '));
input('category','');input('query','RSI');assert.ok(elements.rows.children.length>0);
input('query','');input('review','');input('kind','tool');assert.ok(elements.rows.children.length>0);for(const tr of elements.rows.children)assert.equal(tr.children[2].textContent,'不评分');
console.log('PASS: default reviewed view, safe links, empty state, score/category/search/type filters, pagination and reset. DOM harness only; no browser visual inspection.');
