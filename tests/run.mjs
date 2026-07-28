// Test runner riproducibile per il motore di staging TNM.
// Esecuzione:  node tests/run.mjs    (oppure: npm test)
// Exit code 0 = tutti i test passano; 1 = almeno un fallimento.
import { loadEngine, readFile } from './harness.mjs';

const eng = loadEngine();
const {
  SITES, STAGE_ORD, getStagingRules, getVariants,
  computeBestStage, resolveNX, validateCase, getPfx,
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

// ── 5b. NX blocca SOLO se N è realmente discriminante a parità di T/M ──
section('NX condizionato: blocca solo in caso di reale ambiguità di stadio residua');
const prostata = SITES.find(s => s.id === 'prostata');
const canaleAnale = SITES.find(s => s.id === 'canale_anale');

// pT3b NX M0 (prostata, stadio patologico): N0→III, N1→IVA — N è discriminante → blocca.
ok('pT3b NX M0 (prostata/path) blocca lo staging (N discriminante: N0→III vs N1→IVA)',
   blocks(validateCase(prostata, 'T3b', 'NX', 'M0', {}, '', '', pfx, 'path')));

// T2 NX M1 (canale anale): qualunque N con M1 → Stadio IV — N NON è discriminante → assegna.
const rulesCA = getStagingRules(canaleAnale, null);
const vT2NXM1 = validateCase(canaleAnale, 'T2', 'NX', 'M1', {}, '', '', pfx, null);
ok('T2 NX M1 (canale anale) NON blocca (M1 ⇒ Stadio IV indipendentemente da N)',
   !blocks(vT2NXM1));
ok('T2 NX M1 (canale anale) risolve a Stadio IV',
   resolveNX(rulesCA, canaleAnale, 'T2', 'NX', 'M1', {}).stage === 'IV');

// Tis NX M0 (colon): l'unica riga di tabella per Tis richiede N0 → Stadio 0 — N non discriminante.
const rulesColon = getStagingRules(colon, null);
const vTisNXM0 = validateCase(colon, 'Tis', 'NX', 'M0', {}, '', '', pfx, null);
ok('Tis NX M0 (colon) NON blocca (unica riga di tabella per Tis è N0 → Stadio 0)',
   !blocks(vTisNXM0));
ok('Tis NX M0 (colon) risolve a Stadio 0',
   resolveNX(rulesColon, colon, 'Tis', 'NX', 'M0', {}).stage === '0');

// ── 5c. Messaggio di validazione coerente con "0 linfonodi esaminati" ──
section('Messaggio NX coerente con LN esaminati = 0 (valore valido, non campo vuoto)');
const vNXNoCount = validateCase(prostata, 'T3b', 'NX', 'M0', {}, '', '', pfx, 'path');
ok('NX senza LN esaminati: il messaggio chiede il numero di linfonodi',
   vNXNoCount.incomplete.some(m => m.includes('numero di linfonodi esaminati')));
const vNXZeroCount = validateCase(prostata, 'T3b', 'NX', 'M0', {}, '0', '', pfx, 'path');
ok('NX con LN esaminati = 0: il messaggio NON richiede di nuovo il numero (già fornito)',
   vNXZeroCount.incomplete.length > 0 &&
   !vNXZeroCount.incomplete.some(m => m.includes('numero di linfonodi esaminati')));

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

// ── 8b. Parità motore su index-en.html (logica identica alla IT) ─────
section('Parità struttura/logica — index-en.html');
let engEn = null;
try { engEn = loadEngine('index-en.html'); } catch (e) { /* file assente: skip */ }
if (!engEn) {
  console.log('  (index-en.html non presente — sezione saltata)');
} else {
  ok('EN: stesso numero di sedi', engEn.SITES.length === SITES.length,
     `IT ${SITES.length} vs EN ${engEn.SITES.length}`);
  ok('EN: stessi id sede e stesso ordine',
     engEn.SITES.map(s => s.id).join(',') === SITES.map(s => s.id).join(','));
  // STAGE_ORD coerente
  const enUnknown = new Set();
  for (const s of engEn.SITES)
    for (const variant of (engEn.getVariants(s) ? engEn.getVariants(s).map(x => x.id) : [null]))
      for (const r of engEn.getStagingRules(s, variant))
        if (!(r.stage in engEn.STAGE_ORD)) enUnknown.add(s.id + ':' + r.stage);
  ok('EN: tutti gli stage in STAGE_ORD', enUnknown.size === 0, [...enUnknown].join(', '));
  // Anti-ambiguità EN
  let enAmbig = [];
  for (const s of engEn.SITES)
    for (const variant of (engEn.getVariants(s) ? engEn.getVariants(s).map(x => x.id) : [null])) {
      const rules = engEn.getStagingRules(s, variant);
      if (!rules.length) continue;
      for (const t of s.T) for (const n of s.N) for (const mm of s.M)
        if (engEn.computeBestStage(rules, t.c, n.c, mm.c, {}).ambiguous)
          enAmbig.push(`${s.id}/${variant ?? '-'}: ${t.c}/${n.c}/${mm.c}`);
    }
  ok('EN: nessuna ambiguità nelle tabelle', enAmbig.length === 0,
     enAmbig.slice(0, 6).join(' | '));
  // Coerenza stadio per ogni sede/regola: IT e EN devono dare lo stesso risultato
  let mismatch = [];
  for (const s of SITES) {
    const sEn = engEn.SITES.find(x => x.id === s.id);
    for (const variant of variantsOf(s)) {
      const rIt = getStagingRules(s, variant), rEn = engEn.getStagingRules(sEn, variant);
      for (const t of s.T) for (const n of s.N) for (const mm of s.M) {
        const a = computeBestStage(rIt, t.c, n.c, mm.c, {});
        const b = engEn.computeBestStage(rEn, t.c, n.c, mm.c, {});
        if (a.stage !== b.stage) mismatch.push(`${s.id}/${variant ?? '-'} ${t.c}/${n.c}/${mm.c}: IT ${a.stage} ≠ EN ${b.stage}`);
      }
    }
  }
  ok('IT ed EN producono lo stesso stadio per ogni T/N/M', mismatch.length === 0,
     mismatch.slice(0, 6).join(' | ') + (mismatch.length > 6 ? ` …(+${mismatch.length - 6})` : ''));
  // PSG prostata (codici non tradotti)
  ok('EN: PSG prostata cM1/N0 → IVB',
     engEn.computePrognosticStage_prostata('T2', 'N0', 'cM1', '<10 ng/mL', 1) === 'IVB');
}

// ── 9. Service worker: path relativi (punto 3) ───────────────────────
section('Service worker path');
const indexHtml = readFile('index.html');
const swJs = readFile('sw.js');
ok('index.html registra ./sw.js', indexHtml.includes('register("./sw.js")'));
ok('index.html non usa più /TNM/sw.js', !indexHtml.includes('/TNM/sw.js'));
ok('sw.js non contiene path assoluti /TNM/', !swJs.includes('/TNM/'));
const manifest = JSON.parse(readFile('manifest.json'));
ok('manifest start_url relativo (no /TNM/)', !manifest.start_url.startsWith('/'));
ok('manifest scope relativo (no /TNM/)', !manifest.scope.startsWith('/'));

// ── Riepilogo ────────────────────────────────────────────────────────
console.log('\n' + '─'.repeat(60));
console.log(`PASS ${pass}  ·  FAIL ${fail}`);
if (fail) {
  console.log('\nFALLIMENTI:');
  failures.forEach(f => console.log('  ✗ ' + f));
  process.exit(1);
}
console.log('Tutti i test superati.');
