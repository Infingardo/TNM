// Carica index.html, estrae i blocchi <script> e li esegue in una sandbox VM
// con uno stub minimale del DOM, esponendo il motore di staging per i test.
// Nessuna dipendenza esterna: solo Node core (fs, vm, url).
import fs from 'node:fs';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
export const ROOT = join(__dirname, '..');

// Simboli del motore che vogliamo testare (devono esistere in index.html).
const EXPORTS = [
  'SITES', 'STAGE_ORD', 'PARENTS',
  'stripPfx', 'codeMatch', 'ruleMatches', 'computeBestStage',
  'getStagingRules', 'getVariants', 'validateCase', 'getPfx',
  'computePrognosticStage_prostata', 'computePrognosticStage_mammella',
];

// Proxy "assorbente": qualsiasi accesso/chiamata/property-set non rompe l'init.
function makeFake() {
  const fake = new Proxy(function () {}, {
    get: () => fake,
    set: () => true,
    apply: () => fake,
    construct: () => fake,
  });
  return fake;
}

export function loadEngine() {
  const html = fs.readFileSync(join(ROOT, 'index.html'), 'utf8');
  const re = /<script>([\s\S]*?)<\/script>/g;
  let m, code = '';
  while ((m = re.exec(html))) code += m[1] + '\n';

  // Esponi i simboli del motore sul globalThis della sandbox.
  code += '\n;globalThis.__engine={' +
    EXPORTS.map(n => `${n}: (typeof ${n}!=="undefined"?${n}:undefined)`).join(',') +
    '};';

  const fake = makeFake();
  const documentStub = new Proxy({}, {
    get: (_t, p) => {
      if (p === 'querySelectorAll') return () => [];
      if (p === 'getElementById' || p === 'querySelector' || p === 'createElement') return () => fake;
      if (p === 'addEventListener') return () => {};
      return fake;
    },
  });
  const sandbox = {
    document: documentStub,
    window: new Proxy({}, { get: () => () => {} }),
    navigator: {},
    localStorage: { getItem: () => null, setItem: () => {} },
    console,
    setTimeout: () => 0,
    clearTimeout: () => {},
  };
  sandbox.globalThis = sandbox;
  vm.createContext(sandbox);
  try {
    vm.runInContext(code, sandbox, { filename: 'index.html<script>' });
  } catch (e) {
    // L'init UI può lanciare contro lo stub DOM: lo ignoriamo, il motore è già definito.
    if (!sandbox.__engine) throw e;
  }
  const eng = sandbox.__engine;
  const missing = EXPORTS.filter(n => eng[n] === undefined);
  if (missing.length) throw new Error('Simboli motore mancanti in index.html: ' + missing.join(', '));
  return eng;
}

export function readFile(rel) {
  return fs.readFileSync(join(ROOT, rel), 'utf8');
}
