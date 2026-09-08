import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const DAY = 86400000;
const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const attr = (tag, name) => tag.match(new RegExp(`\\b${name}="([^"]*)"`))?.[1];
const number = n => Number(n.toFixed(3));

export function validateDays(days) {
  if (!days.length) throw new Error('No contribution days; refusing to publish an empty replacement.');
  const sorted = [...days].sort((a,b) => a.date.localeCompare(b.date));
  sorted.forEach((d,i) => {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(d.date) || !Number.isFinite(Date.parse(d.date)) || new Date(d.date).toISOString().slice(0,10)!==d.date || !Number.isInteger(d.count) || d.count < 0 || !Number.isInteger(d.level) || d.level < 0 || d.level > 4) throw new Error('Invalid contribution day');
    if (i && Date.parse(d.date)-Date.parse(sorted[i-1].date) !== DAY) throw new Error('Duplicate or missing contribution day');
  });
  return sorted;
}

export function parseCalendar(html) {
  const tips = new Map([...html.matchAll(/<tool-tip\b([^>]*)>([\s\S]*?)<\/tool-tip>/g)].map(m => [attr(m[1], 'for'), m[2].replace(/<[^>]*>/g,'').trim()]));
  const days = [];
  for (const match of html.matchAll(/<td\b[^>]*\bdata-date="[^"]+"[^>]*>/g)) {
    const tag=match[0], tip=tips.get(attr(tag,'id'));
    const count = tip?.match(/^(No|[\d,]+) contributions?\b/);
    if (!count) throw new Error('GitHub calendar markup changed: contribution count missing.');
    days.push({date:attr(tag,'data-date'),level:Number(attr(tag,'data-level')),count:count[1]==='No'?0:Number(count[1].replaceAll(',',''))});
  }
  return validateDays(days);
}

async function request(url, token, body) {
  const response = await fetch(url, {signal:AbortSignal.timeout(30000), headers:{'User-Agent':'AaditHire-profile-visuals', ...(token?{Authorization:`Bearer ${token}`} : {}), ...(body?{'Content-Type':'application/json'}:{})}, ...(body?{method:'POST',body:JSON.stringify(body)}:{})});
  if (!response.ok) throw new Error(`GitHub request failed (${response.status}) at ${new URL(url).pathname}`);
  return response;
}

export async function collect(login, token) {
  if (!/^[a-z\d](?:[a-z\d-]{0,37}[a-z\d])?$/i.test(login)) throw new Error('Invalid GitHub username');
  let days, calendarSource;
  if (token) {
    const result=await (await request('https://api.github.com/graphql',token,{query:'query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount contributionLevel}}}}}}',variables:{login}})).json();
    if (result.errors || !result.data?.user) throw new Error('GitHub GraphQL calendar request failed');
    const levels=['NONE','FIRST_QUARTILE','SECOND_QUARTILE','THIRD_QUARTILE','FOURTH_QUARTILE'];
    days=validateDays(result.data.user.contributionsCollection.contributionCalendar.weeks.flatMap(w=>w.contributionDays.map(d=>({date:d.date,count:d.contributionCount,level:levels.indexOf(d.contributionLevel)}))));
    calendarSource='GitHub GraphQL contributionCalendar';
  } else {
    days=parseCalendar(await (await request(`https://github.com/users/${login}/contributions`)).text());
    calendarSource=`https://github.com/users/${login}/contributions`;
  }
  if (days.length < 350 || days.length > 378) throw new Error('Unexpected annual calendar length');
  const repos=[];
  for (let page=1;;page++) {
    const batch=await (await request(`https://api.github.com/users/${login}/repos?type=owner&per_page=100&page=${page}`,token)).json();
    if (!Array.isArray(batch)) throw new Error('Invalid repository response');
    repos.push(...batch.filter(r=>!r.private && !r.fork && r.owner?.login.toLowerCase()===login.toLowerCase()));
    if (batch.length < 100) break;
  }
  const languages={};
  repos.forEach(r=>{if(r.language) languages[r.language]=(languages[r.language]??0)+1});
  return {schemaVersion:1,login,updated:new Date().toISOString().slice(0,10),calendarSource,repositorySource:`https://api.github.com/users/${login}/repos`,days,publicOriginalRepos:repos.length,stars:repos.reduce((n,r)=>n+r.stargazers_count,0),languages};
}

export function routeFor(days) {
  days=validateDays(days);
  const origin=Date.parse(days[0].date)-new Date(days[0].date).getUTCDay()*DAY;
  const cells=days.map(d=>{const day=Math.round((Date.parse(d.date)-origin)/DAY);return {...d,col:Math.floor(day/7),row:day%7}});
  const columns=Math.max(...cells.map(c=>c.col))+1;
  const pitch=Math.min(17,916/(columns-1 || 1));
  const positioned=cells.map(c=>({...c,x:number(42+c.col*pitch),y:94+c.row*18}));
  const route=[...positioned].sort((a,b)=>a.col-b.col || (a.col%2?b.row-a.row:a.row-b.row));
  // Return outside the calendar, so no contribution squares are erased or skipped.
  const first=route[0],last=route.at(-1);
  const points=[...route,{x:last.x+22,y:last.y},{x:last.x+22,y:230},{x:20,y:230},{x:20,y:first.y},{x:first.x,y:first.y}];
  let length=0;
  points.forEach((p,i)=>{if(i)length+=Math.hypot(p.x-points[i-1].x,p.y-points[i-1].y);p.distance=length});
  return {cells:positioned,points,length};
}

const palettes={dark:{bg:'#0B0D0D',panel:'#121616',fg:'#F4F4F2',muted:'#A3AAA7',line:'#293130',cyan:'#5DD6C7',yellow:'#F4CF55',levels:['#202827','#18483F','#237866','#38A991','#5DD6C7']},light:{bg:'#FAFCFB',panel:'#EDF4F1',fg:'#162521',muted:'#52655E',line:'#CFDDD7',cyan:'#087A68',yellow:'#A87800',levels:['#E5EEE9','#B7E6D8','#7ACCB4','#3BA68C','#087A68']}};
function wrap(title,desc,height,p,content,style='') {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="${height}" viewBox="0 0 1000 ${height}" role="img" aria-labelledby="title desc"><title id="title">${esc(title)}</title><desc id="desc">${esc(desc)}</desc><style>text{font-family:Arial,Helvetica,sans-serif}${style}</style><rect x=".5" y=".5" width="999" height="${height-1}" rx="14" fill="${p.bg}" stroke="${p.line}"/>${content}</svg>\n`;
}
const txt=(x,y,s,size,color,extra='')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" ${extra}>${esc(s)}</text>`;

export function renderRacer(snapshot,theme) {
  const p=palettes[theme],{cells,points,length}=routeFor(snapshot.days);
  const duration=80;
  const path=points.map((q,i)=>`${i?'L':'M'}${q.x} ${q.y}`).join(' ');
  const frames=points.map((q,i)=>{const next=points[i+1]??points[1];const angle=Math.atan2(next.y-q.y,next.x-q.x)*180/Math.PI;return `${number(q.distance/length*100)}%{transform:translate(${q.x}px,${q.y}px) rotate(${number(angle)}deg)}`}).join('');
  let css=`@keyframes drive{${frames}}.car{animation:drive ${duration}s linear infinite}.trail{stroke-dasharray:55 ${number(length-55)};animation:trail ${duration}s linear infinite}@keyframes trail{from{stroke-dashoffset:55}to{stroke-dashoffset:${number(55-length)}}}`;
  const hits=new Map(points.slice(0,cells.length).map(q=>[q.date,q.distance/length*100]));
  let grid='';
  cells.forEach((c,i)=>{
    grid+=`<rect class="day" data-date="${c.date}" data-count="${c.count}" x="${c.x-6}" y="${c.y-6}" width="12" height="12" rx="2" fill="${p.levels[c.level]}"><title>${c.date}: ${c.count} contributions</title></rect>`;
    if(c.count>0){
      const t=hits.get(c.date),before=Math.max(0,t-.015),end=Math.min(99.999,t+2);
      css+=`@keyframes hit${i}{0%{opacity:0}${number(before)}%{opacity:0}${number(t+.01)}%{opacity:.9}${number(end)}%,100%{opacity:0}}.hit${i}{animation:hit${i} ${duration}s linear infinite}`;
      grid+=`<rect class="hit hit${i}" x="${c.x-6}" y="${c.y-6}" width="12" height="12" rx="2" fill="${p.yellow}" opacity="0"/>`;
    }
  });
  css+='@media(prefers-reduced-motion:reduce){.car,.trail,.hit{animation:none!important}.trail,.hit{opacity:0}}';
  const first=points[0];
  const car=`<g class="car" style="transform:translate(${first.x}px,${first.y}px)"><path d="M-10-5H5L13 0L5 5H-10Z" fill="${p.cyan}" stroke="${p.bg}" stroke-width="1"/><path d="M-9-8V-3M-9 3V8M6-7V-3M6 3V7" stroke="${p.fg}" stroke-width="4"/><path d="M-12-6V6M11-6V6" stroke="${p.cyan}" stroke-width="2"/><rect x="-4" y="-2.5" width="6" height="5" rx="2" fill="${p.bg}"/></g>`;
  const range=`${snapshot.days[0].date} — ${snapshot.days.at(-1).date}`;
  const months=[]; let previous='';
  cells.forEach(c=>{const month=c.date.slice(0,7);if(month!==previous){months.push(txt(c.x-6,71,new Date(c.date).toLocaleString('en',{month:'short',timeZone:'UTC'}),11,p.muted));previous=month}});
  const legend=p.levels.map((color,i)=>`<rect x="${861+i*17}" y="258" width="12" height="12" rx="2" fill="${color}"/>`).join('');
  return wrap('Development lap — real GitHub contributions',`Original race car visits the contribution calendar for ${snapshot.login}. ${range}. Squares remain visible; active days flash yellow. Updated ${snapshot.updated}. Reduced-motion preferences stop the car.`,294,p,
    txt(32,33,'DEVELOPMENT LAP',17,p.cyan,'font-weight="700" letter-spacing="1.5"')+txt(968,33,range,13,p.muted,'text-anchor="end"')+months.join('')+grid+`<path class="trail" d="${path}" fill="none" stroke="${p.cyan}" stroke-width="3" opacity=".4" stroke-linecap="round"/>`+car+txt(32,268,`GitHub contributions · Updated ${snapshot.updated}`,13,p.muted)+txt(818,268,'Less',11,p.muted)+legend+txt(955,268,'More',11,p.muted),css);
}

export function renderStats(s,theme) {
  const p=palettes[theme],total=s.days.reduce((n,d)=>n+d.count,0);
  const languages=Object.entries(s.languages).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,4);
  const max=Math.max(1,...languages.map(([,n])=>n));
  let content=txt(32,33,'ON GITHUB',17,p.cyan,'font-weight="700" letter-spacing="1.5"')+txt(968,33,`Updated ${s.updated}`,12,p.muted,'text-anchor="end"');
  [[total,'Contributions'],[s.publicOriginalRepos,'Public repos'],[s.stars,'Stars received']].forEach(([n,label],i)=>{
    const x=32+i*171;
    content+=`<rect x="${x}" y="62" width="155" height="112" rx="10" fill="${p.panel}"/>`+txt(x+14,115,n,40,i===0?p.yellow:p.fg,'font-weight="700"')+txt(x+14,146,label,14,p.muted);
  });
  content+=txt(580,75,'TOP LANGUAGES',16,p.fg,'font-weight="700"')+txt(580,97,'Primary language · public non-fork repo count',12,p.muted);
  languages.forEach(([name,n],i)=>{const y=126+i*27;content+=txt(580,y,name,14,p.fg)+`<rect x="706" y="${y-10}" width="205" height="8" rx="4" fill="${p.panel}"/><rect x="706" y="${y-10}" width="${number(205*n/max)}" height="8" rx="4" fill="${i===0?p.cyan:p.yellow}"/>`+txt(938,y,n,13,p.muted)});
  if(!languages.length)content+=txt(580,134,'No primary language data yet',14,p.muted);
  content+=txt(32,204,`${s.days[0].date} → ${s.days.at(-1).date}`,12,p.muted)+txt(32,227,'Repos and stars: public, owned, non-fork repositories.',11,p.muted);
  return wrap('GitHub stats and top languages',`Real GitHub snapshot for ${s.login}: ${total} contributions in the displayed period, ${s.publicOriginalRepos} public owned non-fork repositories, ${s.stars} stars. Top languages are measured by repository primary-language count, not code bytes or skill.`,250,p,content);
}

export async function generate(snapshot,output='output') {
  snapshot.days=validateDays(snapshot.days);
  await mkdir(output,{recursive:true});
  const files={'github-activity.json':JSON.stringify(snapshot,null,2)+'\n'};
  for(const theme of ['dark','light']) {
    const suffix=theme==='dark'?'-dark':'';
    files[`contribution-racer${suffix}.svg`]=renderRacer(snapshot,theme);
    files[`github-stats${suffix}.svg`]=renderStats(snapshot,theme);
  }
  // Render everything first; API/parser failures never replace last-known-good assets.
  for(const [file,content] of Object.entries(files))await writeFile(resolve(output,file),content);
}

if(process.argv[1] && import.meta.url===pathToFileURL(resolve(process.argv[1])).href) {
  const args=process.argv.slice(2),value=key=>args[args.indexOf(key)+1];
  try {
    const snapshot=args.includes('--snapshot')?JSON.parse(await readFile(value('--snapshot'),'utf8')):await collect(process.env.GITHUB_USER||'AaditHire',process.env.GITHUB_TOKEN);
    await generate(snapshot,args.includes('--out')?value('--out'):'output');
    console.log(`Generated stats and animated racer: ${snapshot.days.length} days, ${snapshot.publicOriginalRepos} public original repos.`);
  }catch(error){console.error(error.message);process.exitCode=1}
}
