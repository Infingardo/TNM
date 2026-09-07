// Test runner riproducibile per il motore di staging TNM.
// Esecuzione:  node tests/run.mjs    (oppure: npm test)
// Exit code 0 = tutti i test passano; 1 = almeno un fallimento.
import { loadEngine, readFile } from './harness.mjs';

const eng = loadEngine();
const {
  SITES, STAGE_ORD, getStagingRules, getVariants,
  computeBestStage, resolveNX, resolveNonEvaluable, validateCase, getPfx,
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

// ── 5d. TX blocca sempre lo staging ───────────────────────────────────
// Regressione del bug "con TX viene comunque dato Stadio IV": il pannello di
// validazione diceva «lo stadio non può essere assegnato» mentre il box
// risultato stampava «Stadio IVA (assegnato)», perché le righe "Any T" facevano
// match. T non valutabile ⇒ nessuno stadio, senza eccezioni.
section('TX blocca sempre lo staging (nessuna eccezione per le righe "Any T")');
const tiroide = SITES.find(s => s.id === 'tiroide');
const bare = c => c.replace(/^(yp|yc|rp|p|c|r|y)/, '');
const resolveIn = (site, T, N, M, variant = null) =>
  resolveNonEvaluable(getStagingRules(site, variant), site, T, N, M, {});

// Casi in cui la tabella da sola produrrebbe uno stadio: deve comunque bloccare.
const txCases = [
  [colon, 'TX', 'NX', 'M1a', null, 'IVA', 'riga Any T/Any N con M1a'],
  [colon, 'TX', 'N0', 'M1b', null, 'IVB', 'M1b documentato'],
  [prostata, 'TX', 'N1', 'M0', 'path', 'IVA', 'riga Any T, N1, M0'],
  [tiroide, 'TX', 'NX', 'M0', 'diff_young', 'I', 'riga Any T, Any N, M0'],
];
for (const [site, T, N, M, variant, tableStage, why] of txCases) {
  const tag = `${site.id}${variant ? '/' + variant : ''} ${T}/${N}/${M}`;
  ok(`${tag}: la tabella da sola darebbe ${tableStage} (${why})`,
     computeBestStage(getStagingRules(site, variant), T, N, M, {}).stage === tableStage);
  const r = resolveIn(site, T, N, M, variant);
  ok(`${tag}: non assegnabile`, r.resolved === false && r.stage === null,
     'stage=' + r.stage);
  ok(`${tag}: la validazione blocca`,
     blocks(validateCase(site, T, N, M, {}, '', '', pfx, variant)));
}

// Nessun impatto sui casi ordinari.
{
  const rules = getStagingRules(colon, null);
  ok('T3/N1a/M0 invariato rispetto a computeBestStage',
     resolveNonEvaluable(rules, colon, 'T3', 'N1a', 'M0', {}).stage ===
     computeBestStage(rules, 'T3', 'N1a', 'M0', {}).stage);
}

// Invarianti globali su tutte le sedi/varianti:
//  a) nessun TX produce mai uno stadio;
//  b) messaggio e stadio non si contraddicono mai.
let txWithStage = [], neBad = [], nxResolvedCount = 0;
for (const s of SITES) {
  for (const variant of variantsOf(s)) {
    const rules = getStagingRules(s, variant);
    if (!rules.length) continue;
    for (const t of s.T) for (const n of s.N) for (const mm of s.M) {
      const tX = bare(t.c) === 'TX', nX = bare(n.c) === 'NX';
      if (!tX && !nX) continue;
      const r = resolveNonEvaluable(rules, s, t.c, n.c, mm.c, {});
      const tag = `${s.id}/${variant ?? '-'} ${t.c}/${n.c}/${mm.c}`;
      if (tX && (r.stage != null || r.resolved)) txWithStage.push(tag + ' → ' + r.stage);
      if (r.resolved) {
        nxResolvedCount++;
        if (r.stage == null) neBad.push(tag + ': resolved ma senza stadio');
      } else if (r.stage != null) {
        neBad.push(tag + ': non resolved ma con stadio');
      }
    }
  }
}
ok('nessun TX produce uno stadio, in nessuna sede', txWithStage.length === 0,
   txWithStage.slice(0, 6).join(' | ') + (txWithStage.length > 6 ? ` …(+${txWithStage.length - 6})` : ''));
ok('nessuna combinazione TX/NX contraddittoria', neBad.length === 0,
   neBad.slice(0, 6).join(' | ') + (neBad.length > 6 ? ` …(+${neBad.length - 6})` : ''));
ok('NX resta assegnabile quando non è discriminante (PR #1 invariato)',
   nxResolvedCount > 0, 'trovati ' + nxResolvedCount);

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
section('Soglia pN0 e tipo di campione linfonodale');
{
  const { PN0_MIN, SN_SITES, LN_DIM_RULES, N_AUTO_RULES } = eng;
  const pfx = { T:'p', N:'p', M:'c' };
  const S = id => SITES.find(x => x.id === id);
  const warn = (id, T, N, tot, pos, opts={}) => {
    const s = S(id);
    return validateCase(s, T, N, 'M0', {}, tot, pos, pfx, s.variants ? s.variants[0].id : null, opts)
      .warnings.filter(w => /inadegua|sentinella|minimo/i.test(w));
  };

  // L'INVARIANTE che avrebbe pescato il difetto: dove il campione nodale standard e'
  // il sentinella, la soglia — se esiste — vale per lo svuotamento, e il sentinella
  // negativo non puo' mai uscire come campionamento inadeguato.
  for (const id of Object.keys(SN_SITES)) {
    const s = SITES.find(x => x.id === id);
    const w = validateCase(s, s.T[4].c, 'N0', 'M0', {}, 1, 0, pfx,
                           s.variants ? s.variants[0].id : null, { lnType: 'sn' });
    ok(`${id}: un sentinella negativo non e mai "campionamento inadeguato"`,
       !w.warnings.some(x => /inadegua/i.test(x)), w.warnings.join(' | '));
  }
  ok('melanoma non ha piu una soglia pN0', PN0_MIN.melanoma === undefined,
     'PN0_MIN.melanoma = ' + PN0_MIN.melanoma);
  ok('merkel non ha piu una soglia pN0', PN0_MIN.merkel === undefined,
     'PN0_MIN.merkel = ' + PN0_MIN.merkel);
  ok('mammella, melanoma e merkel sono dichiarate sedi a sentinella',
     ['mammella','melanoma','merkel'].every(id => !!SN_SITES[id]));

  // Comportamento: il sentinella negativo non viene messo in riserva.
  for (const id of ['melanoma','merkel','mammella']) {
    const w = warn(id, id==='mammella'?'T1c':(id==='merkel'?'T1':'T3a'), 'N0', 2, 0, { lnType:'sn' });
    ok(`${id}: sentinella negativo → nessuna riserva sul numero`,
       w.length === 1 && /adeguato per definizione/.test(w[0]), w[0] || '(nessun warning)');
  }
  // Con lo svuotamento la soglia resta dov'e' prevista.
  ok('mammella: svuotamento con 2 LN → riserva mantenuta',
     /inadeguato/.test(warn('mammella','T1c','N0',2,0,{ lnType:'dissezione' })[0] || ''));
  ok('mammella: svuotamento con 12 LN → nessuna riserva',
     warn('mammella','T1c','N0',12,0,{ lnType:'dissezione' }).length === 0);
  // Sede senza pratica del sentinella: comportamento invariato.
  ok('colon: 8 LN → riserva (soglia 12, invariata)',
     /inadeguato/.test(warn('colon_retto','T3','N0',8,0,{})[0] || ''));
  ok('colon: 14 LN → nessuna riserva', warn('colon_retto','T3','N0',14,0,{}).length === 0);
  // Tipo non specificato: si chiede il dato, non si accusa il campione.
  ok('melanoma senza tipo di campione: chiede il tipo, non dichiara inadeguatezza',
     !/inadeguato/.test(warn('melanoma','T3a','N0',2,0,{})[0] || ''),
     warn('melanoma','T3a','N0',2,0,{})[0]);

  // La dimensione arriva come parametro: validateCase non legge piu il DOM.
  const vDim = validateCase(S('mammella'),'T1c','N0','M0',{},2,0,pfx,null,{ lnDim:'0.15' });
  ok('mammella: ITC segnalata dalla dimensione passata come parametro',
     vDim.warnings.some(w => /ITC/.test(w)));
  ok('validateCase non legge il DOM',
     !/getElementById/.test(readFile('index.html').split('function validateCase')[1].split('\nfunction ')[0]));
}

section('Congruenza N: solo dove il conteggio la determina');
{
  const { LN_DIM_RULES, N_AUTO_RULES } = eng;
  const pfx = { T:'p', N:'p', M:'c' };
  const S = id => SITES.find(x => x.id === id);
  // Dove la categoria dipende da dimensione o ENE, il conteggio da solo non decide.
  ok('nessuna sede ha insieme LN_DIM_RULES e il controllo per conteggio attivo',
     Object.keys(LN_DIM_RULES).every(id => {
       const v = validateCase(S(id), S(id).T[3].c, S(id).N[2].c, 'M0', {}, 10, 3, pfx,
                              S(id).variants ? S(id).variants[0].id : null, {});
       return !v.errors.some(e => /Categoria N incongruente/.test(e));
     }));
  // Ghiandole salivari: la rete esiste ed e' ENE-aware.
  const gs = S('gh_salivari');
  const err = (n, pos, ene) => validateCase(gs,'T2',n,'M0',{},12,pos,pfx,'path',{ lnEne:ene })
                                 .errors.filter(e => /incongruente/.test(e));
  ok('pENE+ con 2 LN+ → pN2 accettato', err('pN2',2,'pos').length === 0);
  ok('pENE+ con 2 LN+ → pN1 respinto',  err('pN1',2,'pos').length === 1);
  ok('pENE− con 5 LN+ → pN2 accettato', err('pN2',5,'neg').length === 0);
  ok('pENE− con 5 LN+ → pN1 respinto',  err('pN1',5,'neg').length === 1);
  ok('pENE− con 2 LN+ → pN1 accettato', err('pN1',2,'neg').length === 0);
  ok('senza ENE non si accusa nulla',   err('pN2',2,'').length === 0);
}

section('Etichetta di edizione: dalla sede, non dal renderer');
{
  const html = readFile('index.html');
  const { editionLabel, editionRef } = eng;
  ok('editionLabel esiste', typeof editionLabel === 'function');
  ok('il canale anale non e attribuito a UICC', editionLabel('canale_anale') !== eng.EDITION_DEFAULT
     && /^AJCC/.test(editionLabel('canale_anale')), editionLabel('canale_anale'));
  ok('e dichiara la divergenza nel cartello', /divergenza/i.test(editionLabel('canale_anale')));
  ok('il riferimento del referto del canale anale dichiara la divergenza',
     /divergenza|esclusi/i.test(editionRef('canale_anale')));
  ok('il melanoma dichiara i criteri invariati', /invariat/i.test(editionLabel('melanoma')));
  ok('le altre sedi restano sulla 9ª ed. UICC', /UICC/.test(editionLabel('colon_retto')));
  // niente etichetta cablata nel renderer
  const codice = html.replace(/^\s*\/\/.*$/gm, '');
  ok("nessuna etichetta di edizione cablata in stage-label",
     !/stage-label'\)\.textContent='TNM/.test(codice));
  ok('il referto prende il riferimento dalla sede', /editionRef\(s\.id\)/.test(codice));
}

section('Metadati di completezza coerenti con i dati');
{
  const contraddizioni = SITES.filter(s =>
    s.completeness === 'complete' &&
    Object.values(s.coverage || {}).some(v => v === 'missing'));
  ok("nessuna sede 'complete' con una copertura dichiarata mancante",
     contraddizioni.length === 0, contraddizioni.map(s => s.id).join(', '));
  const { PN0_MIN } = eng;
  const incoerenti = SITES.filter(s => s.coverage?.soglia_pN0 === 'na' && PN0_MIN[s.id]);
  ok("nessuna sede dichiara 'soglia non definita' e poi ne applica una",
     incoerenti.length === 0, incoerenti.map(s => s.id + '=' + PN0_MIN[s.id]).join(', '));
  const mancanti = SITES.filter(s => s.coverage?.soglia_pN0 === 'ok'
    && !PN0_MIN[s.id] && !eng.PN0_MIN_SPECIAL?.[s.id] && !eng.SN_SITES[s.id]);
  ok("nessuna sede dichiara 'soglia documentata' senza averla",
     mancanti.length === 0, mancanti.map(s => s.id).join(', '));
}

section('Versione: una sola, in tutti i punti');
{
  const html = readFile('index.html');
  const pkg = JSON.parse(readFile('package.json'));
  const meta = (html.match(/version:'([\d.]+)'/) || [])[1];
  ok('TOOL_META.version === package.json', meta === pkg.version, `${meta} vs ${pkg.version}`);
  ok('la versione compare nel titolo', html.includes(`v${pkg.version} —`), pkg.version);
  ok('la versione compare nel disclaimer', html.includes(`casi borderline · v${pkg.version}`));
  const vecchie = [...html.matchAll(/v(\d+\.\d+\.\d+)/g)].map(m => m[1]).filter(v => v !== pkg.version);
  ok('nessuna versione vecchia rimasta in pagina', vecchie.length === 0, [...new Set(vecchie)].join(', '));
  // Il README dichiara la versione corrente in tre punti: e' la prima cosa che
  // resta indietro, e nessun test la guardava.
  const readme = readFile('README.md');
  ok('il README dichiara la versione corrente', readme.includes('v' + pkg.version));
  const vecchieRm = [...readme.matchAll(/\*\*Versione:\*\* v(\d+\.\d+\.\d+)/g)].map(m => m[1]);
  ok('l intestazione del README e allineata', vecchieRm.every(v => v === pkg.version),
     vecchieRm.join(', '));
}

section('Parità struttura/logica — index-en.html');
let engEn = null, enExists = true, enErr = '';
try { engEn = loadEngine('index-en.html'); }
catch (e) { enErr = e.message; try { readFile('index-en.html'); } catch { enExists = false; } }
// v1.1.0: prima questa sezione veniva saltata in silenzio se il build EN non si
// caricava — cioe' proprio quando era rimasto indietro rispetto a index.html.
ok('index-en.html si carica (o e assente del tutto)', !!engEn || !enExists,
   'index-en.html presente ma non caricabile: ' + enErr);
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
        // Il meccanismo TX/NX deve risolvere allo stesso modo nei due build.
        if (t.c === 'TX' || n.c === 'NX') {
          const ra = resolveNonEvaluable(rIt, s, t.c, n.c, mm.c, {});
          const rb = engEn.resolveNonEvaluable(rEn, sEn, t.c, n.c, mm.c, {});
          if (ra.stage !== rb.stage || ra.resolved !== rb.resolved)
            mismatch.push(`${s.id}/${variant ?? '-'} ${t.c}/${n.c}/${mm.c}: TX/NX IT ${ra.stage}/${ra.resolved} ≠ EN ${rb.stage}/${rb.resolved}`);
        }
      }
    }
  }
  ok('IT ed EN producono lo stesso stadio per ogni T/N/M', mismatch.length === 0,
     mismatch.slice(0, 6).join(' | ') + (mismatch.length > 6 ? ` …(+${mismatch.length - 6})` : ''));
  // PSG prostata (codici non tradotti)
  ok('EN: PSG prostata cM1/N0 → IVB',
     engEn.computePrognosticStage_prostata('T2', 'N0', 'cM1', '<10 ng/mL', 1) === 'IVB');

  // I messaggi che l'utente legge devono essere davvero tradotti. La parita'
  // strutturale non lo vede: le tabelle possono essere identiche e i testi italiani.
  const enHtml = readFile('index-en.html');
  const SPIE = ['linfonodi','sentinella','esaminati','selezionata','inadeguato','incongruente',
                'campione','raccomandato','soglia','stadio non','non valutabile'];
  const messaggi = [...enHtml.matchAll(/(?:warnings|errors|incomplete)\.push\('((?:[^'\\]|\\.)*)'/g)]
    .map(m => m[1]);
  const nonTradotti = messaggi.filter(t => SPIE.some(w => t.toLowerCase().includes(w)));
  ok(`EN: nessun messaggio rimasto in italiano (${messaggi.length} messaggi)`,
     nonTradotti.length === 0,
     nonTradotti.slice(0, 3).map(t => t.slice(0, 70)).join(' | '));
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
