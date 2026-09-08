import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseCalendar, validateDays, routeFor, renderRacer, renderStats, collect } from './github-visuals.mjs';

// Synthetic cases only; published SVGs are generated from fetched GitHub data.
const days=Array.from({length:365},(_,i)=>({date:new Date(Date.UTC(2025,8,9+i)).toISOString().slice(0,10),count:i%11===0?2:0,level:i%11===0?1:0}));
const snapshot={login:'test-user',updated:'2026-09-08',days,publicOriginalRepos:3,stars:2,languages:{Python:2,TypeScript:1}};

test('calendar parser associates tooltips by ID, including commas and zero',()=>{
  const html='<td id="b" data-level="4" data-date="2026-09-08"></td><td data-date="2026-09-07" id="a" data-level="0"></td><tool-tip for="a">No contributions on September 7th.</tool-tip><tool-tip for="b">1,234 contributions on September 8th.</tool-tip>';
  assert.deepEqual(parseCalendar(html),[{date:'2026-09-07',count:0,level:0},{date:'2026-09-08',count:1234,level:4}]);
});
test('markup changes and incomplete data fail instead of fabricating zeros',()=>{
  assert.throws(()=>parseCalendar('<td data-date="2026-09-08" data-level="0"></td>'));
  assert.throws(()=>validateDays([days[0],days[2]]));
  assert.throws(()=>validateDays([days[0],days[0]]));
  assert.throws(()=>validateDays([{date:'2026-02-30',count:0,level:0}]));
  assert.throws(()=>validateDays([]));
});
test('route visits every actual cell once and closes outside the grid',()=>{
  const {cells,points,length}=routeFor(days);
  assert.equal(cells.length,365);
  assert.equal(new Set(points.slice(0,cells.length).map(p=>p.date)).size,365);
  assert.equal(points.at(-1).x,points[0].x);
  assert.equal(points.at(-1).y,points[0].y);
  assert.ok(length>0);
  assert.ok(points.every(p=>p.x>=0&&p.x<1000&&p.y>50&&p.y<250));
  for(let i=1;i<cells.length;i++)assert.ok(Math.abs(points[i].x-points[i-1].x)<.01 || Math.abs(points[i].y-points[i-1].y)<.01,'Route edges must stay orthogonal');
});
test('racer retains counts, adds real motion and supports reduced motion in both themes',()=>{
  for(const theme of ['dark','light']){
    const svg=renderRacer(snapshot,theme);
    assert.equal((svg.match(/class="day"/g)||[]).length,days.length);
    assert.equal((svg.match(/class="hit hit/g)||[]).length,days.filter(d=>d.count>0).length);
    assert.match(svg,/@keyframes drive/);
    assert.match(svg,/prefers-reduced-motion:reduce/);
    assert.match(svg,/animation:none!important/);
    assert.doesNotMatch(svg,/<script|foreignObject/);
    assert.match(svg,/data-count="2"/);
  }
});
test('stats disclose language measurement and escape GitHub values',()=>{
  const svg=renderStats({...snapshot,languages:{'<unsafe>':2}},'dark');
  assert.match(svg,/public non-fork repo count/);
  assert.match(svg,/&lt;unsafe&gt;/);
  assert.doesNotMatch(svg,/<unsafe>/);
});

test('workflow API path paginates and excludes private, forked, or unrelated repos',async t=>{
  let repoPages=0;
  t.mock.method(globalThis,'fetch',async (url,options)=>{
    assert.equal(options.headers.Authorization,'Bearer test-token');
    if(url.endsWith('/graphql'))return new Response(JSON.stringify({data:{user:{contributionsCollection:{contributionCalendar:{weeks:[{contributionDays:days.map(d=>({date:d.date,contributionCount:d.count,contributionLevel:d.level?'FIRST_QUARTILE':'NONE'}))}]}}}}}));
    repoPages++;
    const repo={owner:{login:'test-user'},private:false,fork:false,language:'Python',stargazers_count:1};
    const batch=repoPages===1?Array.from({length:100},()=>({...repo})):[{...repo,private:true},{...repo,fork:true},{...repo,owner:{login:'another-user'}},{...repo,language:'TypeScript'}];
    return new Response(JSON.stringify(batch));
  });
  const data=await collect('test-user','test-token');
  assert.equal(repoPages,2);
  assert.equal(data.publicOriginalRepos,101);
  assert.equal(data.stars,101);
  assert.deepEqual(data.languages,{Python:100,TypeScript:1});
  assert.deepEqual(data.days,days);
});
