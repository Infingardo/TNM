// Runner dei CASI-ANCORA (verifica contro fonte primaria).
// Esecuzione:  node tests/anchors.run.mjs   (oppure: npm run test:anchors)
//
// Regola di fallimento:
//   - confidence 'alta'  → mismatch = FAIL (CI rossa): probabile errore di tabella.
//   - confidence 'media' → mismatch = ADJUDICARE (warning, exit 0): l'atteso o la
//     tabella vanno confrontati con la fonte primaria dall'utente.
import { loadEngine } from './harness.mjs';
import { ANCHORS, ANCHORS_PSG_BREAST } from './anchors.mjs';

const eng = loadEngine();
const { SITES, getStagingRules, computeBestStage, computePrognosticStage_mammella } = eng;

let fail = 0, adjudicate = 0, pass = 0;
const fails = [], adj = [];

function check(label, got, exp, confidence, src) {
  if (got === exp) { pass++; return; }
  const line = `${label}: atteso ${exp}, motore ${got}  [${src}]`;
  if (confidence === 'alta') { fail++; fails.push(line); }
  else { adjudicate++; adj.push(line); }
}

console.log('• Casi-ancora stadio anatomico (vs fonte primaria)');
for (const a of ANCHORS) {
  const s = SITES.find(x => x.id === a.site);
  const got = computeBestStage(getStagingRules(s, null), a.T, a.N, a.M, {}).stage;
  check(`${a.site} ${a.T}/${a.N}/${a.M}`, got, a.expect, a.confidence, a.src);
}

console.log('• Casi-ancora PSG mammella (AJCC 8ª — confidenza media)');
for (const a of ANCHORS_PSG_BREAST) {
  const got = computePrognosticStage_mammella(a.T, a.N, a.extra);
  check(`PSG ${a.T}/${a.N} ${a.extra.G}`, got, a.expect, a.confidence, a.src);
}

console.log('\n' + '─'.repeat(60));
console.log(`PASS ${pass}  ·  FAIL(alta) ${fail}  ·  DA ADJUDICARE(media) ${adjudicate}`);
if (adj.length) {
  console.log('\n⚖  DA ADJUDICARE contro la fonte primaria (non bloccante):');
  adj.forEach(l => console.log('  ? ' + l));
}
if (fails.length) {
  console.log('\n✗ MISMATCH AD ALTA CONFIDENZA (probabile errore di tabella):');
  fails.forEach(l => console.log('  ✗ ' + l));
  process.exit(1);
}
console.log('\nNessun mismatch ad alta confidenza.');
