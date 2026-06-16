// Test runner riproducibile per il motore di staging TNM.
// Esecuzione:  node tests/run.mjs    (oppure: npm test)
// Exit code 0 = tutti i test passano; 1 = almeno un fallimento.
import { loadEngine, readFile } from './harness.mjs';

const eng = loadEngine();
const {
  SITES, STAGE_ORD, getStagingRules, getVariants,
  computeBestStage, validateCase, getPfx,
  computePrognosticStage_prostata, computePrognosticStage_mammella,
} = eng;

let pass = 0, fail = 0;
const failures = [];
function ok(name, cond, detail = '') {
  if (cond) { pass++; }
  else { fail++; failures.push(name + (detail ? ' — ' + detail : '')); }
}
function section(t) { console.log('\n• ' + t); }

// Codici concreti rappresentativi per i campi 'any'/array.
function firstConcrete(list, skip = ['TX', 'T0', 'NX', 'N0', 'MX']) {
  const c = list.map(x => x.c).find(c => !skip.includes(c));
  return c || list[0]?.c;
}
function variantsOf(s) {
  const v = getVariants(s);
  return v ? v.map(x => x.id) : [null];
}

// ── 1. Integrità SITES ────────────────────────────────────────────────
section('Integrità dataset SITES');
ok('SITES è un array', Array.isArray(SITES));
ok('SITES = 29 sedi', SITES.length === 29, 'trovate ' + SITES.length);
ok('nessun elemento undefined/null', SITES.every(Boolean));
const ids = SITES.map(s => s.id);
ok('id univoci', new Set(ids).size === ids.length,
   'duplicati: ' + ids.filter((x, i) => ids.indexOf(x) !== i).join(','));
ok('ogni sede ha T/N/M array', SITES.every(s => Array.isArray(s.T) && Array.isArray(s.N) && Array.isArray(s.M)));

// ── 2. Ogni stage usato è noto in STAGE_ORD ──────────────────────────
section('Coerenza etichette di stadio (STAGE_ORD)');
const unknownStages = new Set();
for (const s of SITES) {
  for (const variant of variantsOf(s)) {
    for (const r of getStagingRules(s, variant)) {
      if (!(r.stage in STAGE_ORD)) unknownStages.add(s.id + ':' + r.stage);
    }
  }
}
ok('tutti gli stage sono in STAGE_ORD', unknownStages.size === 0,
   'sconosciuti: ' + [...unknownStages].join(', '));

// ── 3. Nessuna ambiguità: nessuna combinazione T×N×M mappa a 2 stadi ──
section('Assenza di ambiguità nelle tabelle di staging (cross-product T×N×M)');
let ambig = [];
let evals = 0;
for (const s of SITES) {
  for (const variant of variantsOf(s)) {
    const rules = getStagingRules(s, variant);
    if (!rules.length) continue;
    for (const t of s.T) for (const n of s.N) for (const mm of s.M) {
      evals++;
      const res = computeBestStage(rules, t.c, n.c, mm.c, {});
      if (res.ambiguous) {
        ambig.push(`${s.id}/${variant ?? '-'}: ${t.c}/${n.c}/${mm.c} → ${res.allStages.join(' / ')}`);
      }
    }
  }
}
ok(`nessuna ambiguità su ${evals} combinazioni`, ambig.length === 0,
   ambig.slice(0, 8).join(' | ') + (ambig.length > 8 ? ` …(+${ambig.length - 8})` : ''));

// ── 4. Round-trip: gli input rappresentativi di ogni regola restano coerenti ──
section('Round-trip regole (input della regola → stesso stadio, non ambiguo)');
let rtBad = [];
for (const s of SITES) {
  for (const variant of variantsOf(s)) {
    const rules = getStagingRules(s, variant);
    for (const r of rules) {
      const T = r.T === 'any' ? firstConcrete(s.T) : (Array.isArray(r.T) ? r.T[0] : r.T);
      const N = r.N === 'any' ? firstConcrete(s.N) : (Array.isArray(r.N) ? r.N[0] : r.N);
      const M = r.M === 'any' ? firstConcrete(s.M) : (Array.isArray(r.M) ? r.M[0] : r.M);
      const extra = {};
      if (r.extra) for (const k in r.extra) extra[k] = Array.isArray(r.extra[k]) ? r.extra[k][0] : r.extra[k];
      const res = computeBestStage(rules, T, N, M, extra);
      if (res.ambiguous) rtBad.push(`${s.id}/${variant ?? '-'} [${T}/${N}/${M}] ambiguo ${res.allStages.join('/')}`);
      else if (res.stage == null) rtBad.push(`${s.id}/${variant ?? '-'} [${T}/${N}/${M}] nessun match (regola ${r.stage})`);
    }
  }
}
ok('ogni regola produce uno stadio non ambiguo', rtBad.length === 0,
   rtBad.slice(0, 8).join(' | ') + (rtBad.length > 8 ? ` …(+${rtBad.length - 8})` : ''));

// ── 5. TX / NX → staging non assegnabile (incomplete o error) ─────────
section('Casi non valutabili TX / NX');
const pfx = getPfx ? { T: 'p', N: 'p', M: '' } : { T: '', N: '', M: '' };
function blocks(v) { return (v.errors?.length || v.incomplete?.length) > 0; }
const colon = SITES.find(s => s.id === 'colon_retto');
ok('TX blocca lo staging',
   blocks(validateCase(colon, 'TX', 'N0', 'M0', {}, '', '', pfx, null)));
ok('NX blocca lo staging',
   blocks(validateCase(colon, 'T2', 'NX', 'M0', {}, '', '', pfx, null)));
ok('T2/N0/M0 valido NON è bloccato',
   !blocks(validateCase(colon, 'T2', 'N0', 'M0', {}, '12', '0', pfx, null)));

// ── 6. N0 incompatibile con LN positivi dichiarati ───────────────────
section('Cross-check linfonodi');
ok('N0 con LN+ > 0 genera errore',
   validateCase(colon, 'T2', 'N0', 'M0', {}, '12', '3', pfx, null).errors.length > 0);

// ── 7. PSG Prostata (bug regressione M1) ─────────────────────────────
section('Prognostic Stage Group — Prostata');
const PSA = '<10 ng/mL';
ok('cM1/N0 → IVB', computePrognosticStage_prostata('T2', 'N0', 'cM1', PSA, 1) === 'IVB');
ok('pM1/N0 → IVB', computePrognosticStage_prostata('T2', 'N0', 'pM1', PSA, 1) === 'IVB');
ok('M1 nudo/N0 → IVB', computePrognosticStage_prostata('T2', 'N0', 'M1', PSA, 1) === 'IVB');
ok('N1/M0 → IVA', computePrognosticStage_prostata('T2', 'N1', 'M0', PSA, 1) === 'IVA');
ok('cM0(i+) non è trattato come M1', computePrognosticStage_prostata('T1c', 'N0', 'cM0(i+)', PSA, 1) !== 'IVB');
ok('M0/N0/GG5 → IIIC', computePrognosticStage_prostata('T2', 'N0', 'M0', PSA, 5) === 'IIIC');
ok('dati mancanti (PSA) → null', computePrognosticStage_prostata('T2', 'N0', 'M0', '—', 1) === null);

// ── 8. PSG Mammella (invariante strutturale) ─────────────────────────
section('Prognostic Stage Group — Mammella');
const breastExtra = { ER: 'ER+ (≥1%)', PR: 'PR+ (≥1%)', HER2_IHC: '0', HER2_ISH: '—', G: 'G1' };
const psgB = computePrognosticStage_mammella('T1', 'N0', breastExtra);
ok('ritorna uno stadio noto o null (no crash/typo)', psgB === null || (psgB in STAGE_ORD),
   'valore: ' + psgB);

// ── 9. Service worker: path relativi (punto 3) ───────────────────────
section('Service worker path');
const indexHtml = readFile('index.html');
const swJs = readFile('sw.js');
ok('index.html registra ./sw.js', indexHtml.includes('register("./sw.js")'));
ok('index.html non usa più /TNM/sw.js', !indexHtml.includes('/TNM/sw.js'));
ok('sw.js non contiene path assoluti /TNM/', !swJs.includes('/TNM/'));

// ── Riepilogo ────────────────────────────────────────────────────────
console.log('\n' + '─'.repeat(60));
console.log(`PASS ${pass}  ·  FAIL ${fail}`);
if (fail) {
  console.log('\nFALLIMENTI:');
  failures.forEach(f => console.log('  ✗ ' + f));
  process.exit(1);
}
console.log('Tutti i test superati.');
