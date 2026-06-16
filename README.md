# TNM 9ª Edizione — Tool per Anatomia Patologica

Strumento HTML/JS autonomo per la classificazione TNM dei tumori maligni secondo la **9ª edizione UICC (2025)**, con mapping AJCC Cancer Staging Manual Version 9 per sede dove applicabile.

> *"Tu non stai automatizzando la diagnosi. Stai automatizzando la prudenza."*

**Versione:** v1.0.1 · Dataset: UICC TNM 9ª ed. 2025 · Test automatici riproducibili: **60 PASS** (coerenza motore + casi-ancora) · Verifica vs fonte primaria: **colon + mammella**

---

## Novità — v1.0.1 (2026-06-16)

**Correzioni**
- **Prostata PSG (clinicamente rilevante):** `M1` non veniva riconosciuto (confronto con `cM1/pM1` dopo `stripPfx`, irraggiungibile) → una prostata metastatica con N0 poteva essere sottostadiata fino a Stadio I. Ora `M1 → IVB`.
- **Prostata stadio anatomico:** sdoppiato `IV` in `IVA` (N1, M0) e `IVB` (M1).
- **Fonte M = MX** nel referto: forza `stadio = null` con nota "non assegnabile".
- **Mammella PSG:** etichetta resa esplicita **Pathologic PSG (pPSG)** (per `T2N0M0/HR+/HER2−/G1` il pathologic è IA, il clinical sarebbe IB — confermato vs fonte primaria).
- **PWA portabile:** service worker, `manifest.json` e cache list resi con path **relativi** (`./`) → installabile anche in locale o sottocartelle diverse, non solo su GitHub Pages. Precache di manifest e icone → offline completo dal primo avvio.
- Corretta una virgola orfana in `SITES` e una variabile CSS (`--bg2`) non definita.

**Test (nuovi)**
- Suite Node riproducibile (`tests/`, nessuna dipendenza): integrità dataset, assenza di ambiguità su tutte le combinazioni T×N×M, round-trip regole, casi TX/NX, parità logica IT/EN, PSG prostata/mammella, path PWA.
- **Casi-ancora** vs fonte primaria per **colon** (15) e **mammella** (12 anatomici + 2 pPSG): verificano la *correttezza* delle tabelle, non solo la coerenza interna.
- CI GitHub Actions (`.github/workflows/test.yml`) ad ogni push. `npm test` / `npm run test:all`.

> ⚠ **Ambito di validazione onesto:** la verifica contro la fonte primaria è completata per **colon e mammella**. Le altre 27 sedi sono coperte dal solo livello di *coerenza interna* (nessuna garanzia di correttezza di trascrizione). Usare sempre come strumento **assistito**, verificando i casi non banali contro il manuale.

---

## File

| File | Funzione |
|------|----------|
| `index.html` | Tool principale — 29 sedi, staging interattivo, referto strutturato |
| `audit.html` | Tabella di audit — validazione manuale sede per sede con manuale in mano |
| `tests/` | **Suite di test riproducibile (Node)** — 60 asserzioni, eseguita in CI ad ogni push |
| `test.html` | Suite di test in-browser (storica) — 153 casi su 17 sedi |

---

## Caratteristiche principali

### Tre modalità integrate
| Tab | Funzione |
|-----|----------|
| **📋 Definizioni** | Lookup rapido di tutte le categorie T, N, M con descrizione completa in italiano |
| **🎯 Stadiazione** | Calcolo interattivo dello stadio con validazione in tempo reale |
| **📄 Referto** | Generazione di testo strutturato pronto per il LIS / copia-incolla |

### Sedi coperte (29 totali)

**Apparato digerente**
Colon e Retto · Stomaco · Esofago/GEJ · Intestino Tenue · Appendice · Canale Anale · Fegato (HCC) · Dotti biliari intraepatici (CCA) · Dotti biliari peribiliari (Klatskin) · Via biliare distale · Colecisti · Ampolla di Vater · Pancreas (adenocarcinoma)

**NET Gastrointestinali** (WHO 2022, AJCC v9)
NET GI — Stomaco · NET GI — Colon-Retto · NET GI — Pancreas

**Testa e Collo**
Tiroide (4 varianti: PTC/FTC <55aa, PTC/FTC ≥55aa, midollare, anaplastico) · Ghiandole salivari

**Mammella · Urologico**
Mammella · Prostata · Vescica · Rene (RCC) · Testicolo (con marcatori S) · Pelvi Renale · Uretere · Uretra (maschile e femminile)

**Cute / Melanoma**
Melanoma cutaneo (staging clinico e patologico) · Carcinoma della cute (SCC/BCC) · Carcinoma di Merkel

---

## Funzionalità del motore

### Stadiazione
- Gerarchia T/N/M: `T1a` matcha regole `T1`, `N2b` matcha regole `N2`, ecc.
- Varianti per sede: staging clinico vs patologico (Stomaco, Esofago SCC/Adeno, Prostata), per età (Tiroide), per istotipo (Melanoma, Merkel, Uretra M/F)
- Categorie speciali autonome: **N1mi** e **N1a(sn)** non vengono assorbite dalla gerarchia N1
- Campi extra obbligatori: grado istologico per Appendice (M1b → IVA vs IVB), marcatori S per Testicolo
- **PSG AJCC 8ª ed.** per Mammella (ER/PR/HER2/Nottingham/Ki67) e Prostata (PSA/Grade Group ISUP): calcolato in parallelo allo staging UICC. Toggle per mostrare solo staging anatomico.
- **LDH suffix** per Melanoma: M1a(0)/M1a(1) ecc. nel referto
- **IGCCCG prognosis** per Testicolo: soglie S1/S2/S3 e sopravvivenza 5a nel referto
- Ambiguità dataset → `stage: null` (mai lo stadio più alto di default)

### Validazione in tempo reale
| Tipo | Esempi |
|------|--------|
| **Errore bloccante** | pM0 (non esiste), N0 + LN positivi, LN positivi > totale esaminati, TX o NX (stadio non assegnabile), Tis + N positivo |
| **Dato incompleto** | M1b appendice senza grado, staging fuori modello |
| **Warning clinico** | pN0 con campionamento sotto soglia, S=SX testicolo, staging anatomico prostata |

### Blocco TX / NX
Se T o N non sono valutabili (**TX** o **NX**), lo staging non viene assegnato. Il referto segnala esplicitamente il parametro non valutabile e blocca la generazione del testo.

### Prefisso TNM obbligatorio
Dropdown indipendente nel tab Referto: `p` (patologico) · `yp` (post-neoadiuvante) · `r` (recidiva) · `c` (clinico). Il prefisso si applica separatamente a T, N e M.

### Fonte M
Campo separato per la fonte della classificazione M:
- `cM` — clinico/radiologico (default)
- `pM` — patologico (biopsia metastasi)
- `ycM` — post-trattamento, clinico/radiologico
- `ypM` — post-trattamento, patologico
- `MX` — non documentato → produce "M non assegnabile" nel referto

### Referto strutturato — tre sezioni distinte
```
── CLASSIFICAZIONE TNM ──────────────────────────────────
ypT3  ypN1 (3/24)  cM0

ypT3 — Tumore che invade...
ypN1 (3 LN+ su 24 esaminati) — Metastasi in 1-3 linfonodi...
cM0 — Nessuna metastasi a distanza [fonte: clinico/radiologico]

── RAGGRUPPAMENTO DI STADIO ─────────────────────────────
Stadio IIIB (assegnato)

── FATTORI PROGNOSTICI / PREDITTIVI ────────────────────
(Non inclusi nel raggruppamento TNM — riportati a fini clinici)
- LVI presente
- Budding Bd3 (alto)
```

### Auto-calcolo N da LN positivi
Per le sedi con N numerico puro, inserendo il numero di linfonodi positivi il campo N si compila automaticamente come **suggerimento** (badge "⟵ suggerito da LN+").

| Sede | Logica |
|------|--------|
| Colon-Retto | 0→N0, 1→N1a, 2-3→N1b, 4-6→N2a, ≥7→N2b |
| Stomaco | 0→N0, 1-2→N1, 3-6→N2, 7-15→N3a, ≥16→N3b |
| Esofago | 0→N0, 1-2→N1, 3-6→N2, ≥7→N3 |
| Pancreas / Ampolla / Vie biliari | 0→N0, 1-3→N1, ≥4→N2 |
| Appendice | 0→N0, 1→N1a, 2-3→N1b, ≥4→N2 |
| Mammella | 0→N0, 1-3→N1a, 4-9→N2a, ≥10→N3a |

### Badge di completezza per sede
Ogni sede mostra un badge obbligatorio:
- ✓ **Completo** — staging completo implementato
- ◑ **Parziale** — staging incompleto per alcune varianti (es. esofago PPG patologico)

---

## Suite di test e audit

### Test riproducibili (`tests/`, Node — autorevoli)
60 asserzioni senza dipendenze esterne, eseguite in CI ad ogni push:
- **Coerenza motore** (`tests/run.mjs`, 31): integrità `SITES`, etichette stadio in `STAGE_ORD`, **assenza di ambiguità su tutte le combinazioni T×N×M**, round-trip regole, blocco TX/NX, cross-check LN, parità logica IT/EN, path PWA.
- **Casi-ancora vs fonte primaria** (`tests/anchors.mjs`, 29): colon e mammella confrontati con lo schema UICC9/AJCC8 — verificano la *correttezza* delle tabelle.

```
npm test          # coerenza motore
npm run test:all  # coerenza + casi-ancora
```

### Test in-browser (`test.html`, storico)
153 casi su 17 sedi. Eseguibili nel browser, risultato immediato PASS/FAIL/SKIP. Export CSV.

### Tabella di audit (`audit.html`)
Strumento per la validazione manuale riga per riga con il manuale UICC in mano.
- Checkbox a tre stati (non verificato / OK / Errore) per ogni definizione T, N, M e regola di staging
- Campo per sede: verificato da, data, fonte consultata, esito (validata / con riserva / non validata), note
- Badge stato sede aggiornato live
- Stato salvato in localStorage (persistente tra sessioni)
- Export CSV ricco (site_id, section, code, definition, audit_status, reviewer, date, source_ref, esito, note)

**Stato attuale: v1.0.1 — 60 test riproducibili PASS (CI verde); verifica vs fonte primaria: colon + mammella**

---

## Limitazioni dichiarate

| Sede | Limitazione |
|------|-------------|
| Esofago | Staging anatomico — i **Pathological Prognostic Groups** (PPG, con grado e sede, AJCC) non sono implementati. |
| Testicolo S=SX | Stadio I generico senza sottostadio (IA/IB/IS) — richiede nadir AFP/hCG/LDH. |
| UICC vs AJCC | Divergenze dichiarate per sede (es. mammella Tis(LCIS): UICC sì, AJCC no). |
| Sedi non incluse | Faringe, Laringe, Cavo orale, Sedi ginecologiche, Linfomi, SNC, Osso, Tessuti molli. |

---

## Utilizzo

Nessuna installazione, nessuna connessione a internet. File HTML autonomi:

```
index.html   →  tool principale (aprire in qualsiasi browser moderno)
audit.html   →  validazione manuale (usare sempre dallo stesso URL per preservare lo stato)
test.html    →  suite di test automatici
```

**Flusso tipico**
1. Seleziona la sede dal pannello sinistro
2. Tab **Definizioni** — verifica le categorie T/N/M
3. Tab **Stadiazione** — inserisci LN esaminati/positivi, seleziona T/N/M, calcola
4. Tab **Referto** — scegli prefisso TNM e fonte M, aggiungi fattori prognostici, genera e copia
5. **🆕 Nuovo caso** per azzerare tutti i campi

---

## Architettura tecnica

```
index.html
├── CSS (theme off-white, badge completeness, validation colors)
├── HTML (sidebar · topbar · 3 tab panels)
└── JS (~1900 righe, no dipendenze esterne)
    ├── PARENTS{}           Gerarchia T/N/M
    ├── TOOL_META{}         Versione, dataset, responsabile, stato validazione
    ├── SITES[]             Dataset 29 sedi con T/N/M + staging rules + completeness
    ├── N_AUTO_RULES{}      Auto-calcolo N da LN+
    ├── stripPfx()          Stripping prefisso
    ├── codeMatch()         Matching con gerarchia PARENTS
    ├── computeBestStage()  → {stage, ambiguous, allStages}
    ├── validateCase()      Validazione centralizzata (TX/NX block, Tis+N+, LN cross-check)
    ├── generateReferto()   Referto a tre sezioni (TNM / Stadio / Fattori prognostici)
    └── sync*()             Sincronizzazione unidirezionale Stadiazione→Referto
```

---

## Riferimenti

- **UICC TNM Classification of Malignant Tumours, 9ª Edizione** — Brierley, Giuliani, O'Sullivan, Rous, Van Eycken (eds.) — John Wiley & Sons, 2025
- **AJCC Cancer Staging Manual, Version 9** — dove applicabile e verificato per sede
- **WHO Classification of Tumours** (5ª ed., varie sedi) — per grading NET GI
- **ITBCC 2016** — per grading budding tumorale

> Questo tool è sviluppato per uso esclusivo in anatomia patologica da personale medico qualificato. Non sostituisce la valutazione clinico-patologica né la consultazione della fonte primaria. La v1.0.1 supera 60 test automatici riproducibili (CI verde); la verifica contro la fonte primaria è completata per **colon e mammella**, mentre per le altre sedi è garantita la sola coerenza interna. La validazione manuale riga per riga prosegue tramite `audit.html`.

---

## Sviluppo

Progetto sviluppato con metodologia **multi-AI supervisionata**:

| Ruolo | Strumento |
|-------|-----------|
| Architettura, coding, debug, patch | Claude (Anthropic) |
| Avvocato del diavolo, review critica del motore | ChatGPT (OpenAI) |
| Audit dataset contro fonte primaria (UICC TNM 9ª ed. + AJCC v9) | Perplexity / Comet |
| Supervisione clinica, decisioni editoriali, coordinamento | F.M.D. Bianchi |

Ogni sistema ha fatto quello per cui è più adatto. La validazione finale è comunque contro la fonte primaria — gli strumenti sono stati mezzi, non oracoli.

Segnalare bug o divergenze con la fonte primaria aprendo una Issue con: sede, combinazione T/N/M, stadio atteso vs stadio ottenuto.

---

*Filippo Maria Domenico Bianchi — SC Anatomia Patologica, ASST Fatebenefratelli-Sacco, Milano*
