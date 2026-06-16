// ─────────────────────────────────────────────────────────────────────
// CASI-ANCORA — verifica del motore contro la FONTE PRIMARIA.
//
// A differenza degli altri test (che controllano la coerenza INTERNA del
// dataset), questi casi codificano lo stadio atteso preso dal manuale
// UICC TNM 9ª / AJCC 8ª. Servono a intercettare errori di TRASCRIZIONE
// delle tabelle (tabella coerente ma sbagliata).
//
// ⚠ I valori `expect` vanno CONFERMATI dall'utente contro la fonte primaria.
//   `confidence`: 'alta'  = schema canonico stabile (colon/mammella anatomico)
//                 'media' = da verificare cella per cella (PSG mammella)
//   `src`: riferimento alla tabella di origine.
// ─────────────────────────────────────────────────────────────────────

// Helper extra per mammella PSG (HR+ / HER2− / Gx)
const HR_HER2neg = g => ({ ER: 'ER+ (≥1%)', PR: 'PR+ (≥1%)', HER2_IHC: '0', HER2_ISH: '—', G: g });

export const ANCHORS = [
  // ── COLON E RETTO — stadio anatomico (AJCC 8ª, invariato in 9ª) ──────
  // src: AJCC Cancer Staging Manual 8th ed., Colon and Rectum, Stage table
  { site: 'colon_retto', T: 'Tis', N: 'N0',  M: 'M0',  expect: '0',   confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T1',  N: 'N0',  M: 'M0',  expect: 'I',   confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T2',  N: 'N0',  M: 'M0',  expect: 'I',   confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T3',  N: 'N0',  M: 'M0',  expect: 'IIA', confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T4a', N: 'N0',  M: 'M0',  expect: 'IIB', confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T4b', N: 'N0',  M: 'M0',  expect: 'IIC', confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T1',  N: 'N1a', M: 'M0',  expect: 'IIIA',confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T1',  N: 'N2a', M: 'M0',  expect: 'IIIA',confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T3',  N: 'N1a', M: 'M0',  expect: 'IIIB',confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T2',  N: 'N2b', M: 'M0',  expect: 'IIIB',confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T4a', N: 'N2a', M: 'M0',  expect: 'IIIC',confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T4b', N: 'N1b', M: 'M0',  expect: 'IIIC',confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T2',  N: 'N0',  M: 'M1a', expect: 'IVA', confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T2',  N: 'N0',  M: 'M1b', expect: 'IVB', confidence: 'alta', src: 'AJCC8 colon' },
  { site: 'colon_retto', T: 'T2',  N: 'N0',  M: 'M1c', expect: 'IVC', confidence: 'alta', src: 'AJCC8 colon' },

  // ── MAMMELLA — stadio ANATOMICO (UICC 9ª ≡ TNM 8) ───────────────────
  // src: UICC TNM 9th / AJCC8 Breast anatomic stage table
  { site: 'mammella', T: 'Tis (DCIS)', N: 'N0',   M: 'M0', expect: '0',    confidence: 'alta', src: 'UICC9 breast anat' },
  { site: 'mammella', T: 'T1c',        N: 'N0',   M: 'M0', expect: 'IA',   confidence: 'alta', src: 'UICC9 breast anat' },
  { site: 'mammella', T: 'T1c',        N: 'N1mi', M: 'M0', expect: 'IB',   confidence: 'alta', src: 'UICC9 breast anat' },
  { site: 'mammella', T: 'T1c',        N: 'N1a',  M: 'M0', expect: 'IIA',  confidence: 'alta', src: 'UICC9 breast anat' },
  { site: 'mammella', T: 'T2',         N: 'N0',   M: 'M0', expect: 'IIA',  confidence: 'alta', src: 'UICC9 breast anat' },
  { site: 'mammella', T: 'T2',         N: 'N1a',  M: 'M0', expect: 'IIB',  confidence: 'alta', src: 'UICC9 breast anat' },
  { site: 'mammella', T: 'T3',         N: 'N0',   M: 'M0', expect: 'IIB',  confidence: 'alta', src: 'UICC9 breast anat' },
  { site: 'mammella', T: 'T2',         N: 'N2a',  M: 'M0', expect: 'IIIA', confidence: 'alta', src: 'UICC9 breast anat' },
  { site: 'mammella', T: 'T3',         N: 'N1a',  M: 'M0', expect: 'IIIA', confidence: 'alta', src: 'UICC9 breast anat' },
  { site: 'mammella', T: 'T4b',        N: 'N0',   M: 'M0', expect: 'IIIB', confidence: 'alta', src: 'UICC9 breast anat' },
  { site: 'mammella', T: 'T2',         N: 'N3a',  M: 'M0', expect: 'IIIC', confidence: 'alta', src: 'UICC9 breast anat' },
  { site: 'mammella', T: 'T2',         N: 'N0',   M: 'M1', expect: 'IV',   confidence: 'alta', src: 'UICC9 breast anat' },
];

// PSG mammella (AJCC 8ª Prognostic Stage Group). Confidenza MEDIA: i valori
// vanno confermati cella per cella sul manuale. Un mismatch qui NON è
// necessariamente un bug del motore — può essere l'atteso da correggere.
export const ANCHORS_PSG_BREAST = [
  // Esempio canonico AJCC8: T2N0M0 con biologia favorevole scende da IIA(anat) a IB.
  { T: 'T1c', N: 'N0', M: 'M0', extra: HR_HER2neg('G1'), expect: 'IA', confidence: 'media', src: 'AJCC8 breast PSG' },
  { T: 'T2',  N: 'N0', M: 'M0', extra: HR_HER2neg('G1'), expect: 'IB', confidence: 'media', src: 'AJCC8 breast PSG (downstage canonico)' },
];
