# Changelog — TNM 9ª Ed. · Anatomia Patologica

## v1.1.0 (7 settembre 2026) — la soglia pN0 non si applica al sentinella

Revisione mirata su tre cose che i test di coerenza interna non potevano vedere:
una soglia numerica applicata dove non esiste, un'etichetta di edizione cablata nel
renderer, e una rete di sicurezza che copriva la sede sbagliata.

Prima, quello che è stato verificato e **non** è stato toccato: 1422 combinazioni
T×N×M su 29 sedi e tutte le varianti — zero ambiguità, zero regole irraggiungibili,
zero codici del menu scoperti da una regola. Delle 47 combinazioni senza stadio, 44
sono `Tis` con N+ o M1 (biologicamente impossibili, giustamente assenti dalle tabelle)
e 3 sono `Ta N1–N3 M0` della vescica, che la classificazione davvero non assegna.
I mapping LN+ → categoria N di colon, stomaco, esofago, pancreas, vie biliari,
ampolla, colecisti e mammella sono corretti.

### 1. La soglia pN0 scattava sul linfonodo sentinella

`PN0_MIN` conteneva `melanoma:6` e `merkel:6` e la soglia veniva applicata a
prescindere dal tipo di campione. Misurato sulla v1.0.1:

```
melanoma  pN0 con 2 LN → "campionamento potenzialmente inadeguato (minimo: 6)"
merkel    pN0 con 1 LN → "campionamento potenzialmente inadeguato (minimo: 6)"
```

**AJCC 8ª ed. non definisce alcun numero minimo di linfonodi per il pN0 del melanoma**,
e il campione nodale standard è il sentinella: uno o due linfonodi negativi *sono* un
pN0 valido. Il tool metteva in riserva il referto sul campione nodale più frequente
che esista per quella sede. Idem Merkel. Per la mammella il ≥6 è la cifra della
dissezione ascellare di livello I–II, non del sentinella — e la lista N della mammella
non offre codici `(sn)` benché la nota di sede dica di usare sempre il modificatore.

Il tool si contraddiceva già da solo: `coverage.soglia_pN0` del melanoma era
`'missing'` mentre `PN0_MIN.melanoma` valeva 6 e veniva applicato.

**Correzione.** Nuovo campo nell'interfaccia: *tipo di campione linfonodale*
(sentinella / svuotamento / non specificato), mostrato per le sedi in cui il
sentinella è il campione standard (`SN_SITES`: mammella, melanoma, Merkel).

| campione | comportamento |
|---|---|
| sentinella negativo | pN0 adeguato per definizione; ricorda di riportare `pN0(sn)` |
| svuotamento | soglia applicata dove è prevista (mammella 6, colon 12, …) |
| non specificato | chiede il dato invece di accusare il campione |

`melanoma` e `merkel` escono da `PN0_MIN`: AJCC non definisce un minimo, e per la
dissezione il numero atteso dipende dal bacino (ascella, inguine, collo) — un valore
unico sarebbe inventato.

### 2. L'edizione era cablata nel renderer

```js
document.getElementById('stage-label').textContent = 'TNM 9ª Ed. · UICC 2025' + ...
```

Stampato per tutte e 29 le sedi, e lo stesso nel referto. Ma i dati dicevano altro:
melanoma era etichettato `UICC 8ª ed.`, mammella e prostata portano PSG AJCC 8ª ed., e
soprattutto per il **canale anale** questo strumento implementa *deliberatamente*
AJCC v9 (Tis/Stadio 0 esclusi) **contro** UICC V9 che li mantiene — con tanto di nota
che lo motiva. Poi il risultato usciva firmato «UICC 2025»: uno stadio prodotto con le
regole AJCC, attribuito a UICC. È l'unica riga che finisce nel referto e attribuisce
il risultato a una fonte da cui non viene.

Ora l'etichetta e il riferimento del referto vengono dalla sede (`editionLabel`,
`editionRef`). Canale anale: *«AJCC Cancer Staging Manual v9 — divergenza da UICC V9»*.
Melanoma: *«TNM 9ª Ed. · UICC 2025 (criteri melanoma invariati dalla 8ª ed.)»* — la 9ª
edizione UICC rivede un sottoinsieme di capitoli (orofaringe HPV, salivari, rinofaringe,
polmone, timo, mesotelioma, canale anale) e per il melanoma riporta i criteri della 8ª.

### 3. La rete di congruenza N non copriva la sede che ne aveva bisogno

Il controllo «N incongruente rispetto al numero di LN+» confrontava `nCode` già
passato per `stripPfx` con l'output grezzo della regola. Le ghiandole salivari
restituiscono `pN1`/`pN2`: il confronto era sempre falso e il controllo **non scattava
mai** — proprio nell'unica sede in cui la V9 ha riscritto il pN.

Attivandolo così com'era, però, respingeva come incongruente un `pN2` corretto con 1–3
linfonodi e pENE, cioè il caso che la V9 ha introdotto e che la nota di sede descrive.
Il conteggio da solo non determina la categoria dove contano dimensione o ENE
(`LN_DIM_RULES`): lì il controllo generico è disattivato, e per le salivari c'è una
verifica dedicata che legge l'ENE dallo stesso selettore che alimenta l'auto-calcolo.

```
pENE+ con 2 LN+ → pN2 accettato, pN1 respinto
pENE− con 5 LN+ → pN2 accettato, pN1 respinto
pENE− con 2 LN+ → pN1 accettato
```

### 4. Minori

- `validateCase` **leggeva il DOM** (`stg-ln-dim`): non era pura e quel ramo — ITC
  ≤0,2 mm e N1mi per dimensione — non era testabile; sotto lo stub del harness lanciava.
  I dati di campionamento arrivano ora in un oggetto `opts {lnType, lnDim, lnEne}`.
- `completeness:'complete'` conviveva con `coverage.soglia_pN0:'missing'` su 8 sedi.
  Per rene, prostata, testicolo, vescica, melanoma, NET e carcinoma cutaneo quella
  soglia **non esiste in TNM**: nuovo stato `n/d — non definita dalla classificazione`,
  distinto da «non documentato». Il canale anale, che ha due soglie per bacino, è
  documentato in `PN0_MIN_SPECIAL`.
- `validazione_automatica` dichiarava «60 test»: erano 54 + 29 casi-ancora. Ora la
  dicitura riporta le due suite separatamente.
- Vescica `Ta N1–N3 M0` usciva «Non determinabile (caso fuori modello)», che fa pensare
  a un limite dello strumento: ora «Nessuno stadio previsto dalla tabella per questa
  combinazione», che è quello che succede davvero.
- Il messaggio di incongruenza N citava il codice spogliato del prefisso (`N2`) invece
  di quello selezionato (`pN2`).

### 5. Il build inglese era rimasto indietro — e i test non lo vedevano

La sezione di parità EN **veniva saltata in silenzio** quando `index-en.html` non si
caricava, cioè esattamente quando era disallineato. E la parità confrontava strutture e
stadi, non i testi: le tabelle potevano essere identiche e i messaggi in italiano.

Aggiunte due verifiche. La prima ha subito trovato **tre messaggi mai tradotti**, due
dei quali preesistenti alla v1.1.0: `Fonte M = MX…` (nessuna coppia di traduzione) e
`Categoria pN selezionata senza numero di linfonodi esaminati…` (coppia presente ma
inefficace, perché le sostituzioni di frase riscrivevano «linfonodi» prima che
l'ancoraggio esatto potesse agire). `translate_tnm.py` ha ora un blocco `R_PRE`
applicato *prima* delle sostituzioni di frase.

### Test

`npm test` **94** · `npm run test:anchors` **29**. Le invarianti nuove:

- un sentinella negativo non può mai produrre «campionamento inadeguato»;
- nessuna sede dichiara una soglia che non applica, né ne applica una che dichiara assente;
- nessuna sede combina `LN_DIM_RULES` con il controllo di congruenza per conteggio;
- l'etichetta di edizione non è cablata nel renderer e il canale anale non è attribuito a UICC;
- il build EN si carica davvero, e nessun messaggio utente resta in italiano;
- la versione è una sola in tutti i punti in cui compare.

### Aperto

La verifica riga per riga contro la fonte primaria resta completata per **colon e
mammella**. Per le altre 27 sedi questo lavoro ha aggiunto coerenza interna e ha
corretto quello che si poteva stabilire senza il manuale davanti: non sostituisce
l'audit. Le soglie `PN0_MIN` non rimosse (esofago 7, tiroide 6, HCC 3, salivari 10…)
non sono state ri-verificate una per una contro la fonte.
