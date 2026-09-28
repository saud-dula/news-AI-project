# BLOCK 1: Build a single standalone HTML file with the trained model embedded inside it.
import json
from pathlib import Path

base = Path(__file__).parent
model = json.loads((base / "model" / "model.json").read_text(encoding="utf-8"))
metrics = json.loads((base / "model" / "metrics.json").read_text(encoding="utf-8"))

html = r'''<!doctype html>
<html lang="en">
<head>
  <!-- BLOCK 1: This is a standalone file. The design, code, and trained model are embedded. -->
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="Beginner offline AI news classification project">
  <title>NewsCheck AI — Fake News Detector</title>
  <style>
    /* BLOCK 2: Shared colors and dimensions. */
    :root{--navy:#132238;--ink:#1e293b;--muted:#64748b;--canvas:#f7f9fc;--card:#fff;--line:#dfe5ee;--blue:#2563eb;--blue2:#dbeafe;--green:#16734a;--green-bg:#e9f7ef;--red:#b42318;--red-bg:#fff0ee;--amber:#8a4b08;--amber-bg:#fff6df;--shadow:0 12px 32px rgba(20,36,56,.08)}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--canvas);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}button,textarea{font:inherit}button{cursor:pointer}.wrap{width:min(1080px,calc(100% - 32px));margin:auto}
    /* BLOCK 3: Navigation and model status. */
    header{background:rgba(247,249,252,.94);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5;backdrop-filter:blur(10px)}nav{min-height:70px;display:flex;align-items:center;justify-content:space-between;gap:18px}.brand{display:flex;align-items:center;gap:10px;color:var(--navy);font-weight:850;font-size:20px}.mark{display:grid;place-items:center;width:36px;height:36px;border-radius:10px;background:var(--blue);color:white}.status{display:flex;align-items:center;gap:8px;padding:7px 11px;border:1px solid #b9dfca;border-radius:999px;background:var(--green-bg);color:var(--green);font-size:13px;font-weight:750}.dot{width:8px;height:8px;border-radius:50%;background:#22a565}
    /* BLOCK 4: Hero and model information. */
    .hero{display:grid;grid-template-columns:1.08fr .92fr;gap:40px;align-items:center;padding:64px 0 38px}.kicker{color:var(--blue);font-size:13px;font-weight:850;letter-spacing:.13em}.hero h1{margin:10px 0 18px;color:var(--navy);font-size:clamp(42px,6.2vw,74px);line-height:1.02;letter-spacing:-.05em}.hero h1 span{color:var(--blue)}.lead{max-width:650px;margin:0;color:var(--muted);font-size:18px}.model-card{padding:22px;border:1px solid var(--line);border-radius:14px;background:var(--card);box-shadow:var(--shadow)}.model-card h2{font-size:17px;margin:0 0 14px}.model-row{display:flex;justify-content:space-between;gap:16px;padding:10px 0;border-top:1px solid var(--line);font-size:14px}.model-row span{color:var(--muted)}.model-row strong{text-align:right}.ready{color:var(--green)}
    /* BLOCK 5: News input card. */
    .checker{padding:28px;border:1px solid var(--line);border-radius:16px;background:var(--card);box-shadow:var(--shadow)}.checker-head{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;margin-bottom:16px}.checker h2{margin:0;color:var(--navy);font-size:24px}.checker-head p{margin:3px 0 0;color:var(--muted)}.clear{border:0;background:transparent;color:var(--blue);font-weight:750;padding:8px}.clear:hover{text-decoration:underline}label{display:block;margin-bottom:8px;font-weight:750}textarea{display:block;width:100%;min-height:210px;padding:17px;border:1px solid #cbd5e1;border-radius:10px;resize:vertical;background:#fbfdff;color:var(--ink)}textarea:focus{outline:3px solid rgba(37,99,235,.17);border-color:var(--blue)}.under{display:flex;justify-content:space-between;align-items:center;gap:18px;margin-top:12px}.count{color:var(--muted);font-size:14px}.check{min-height:48px;padding:0 24px;border:0;border-radius:10px;background:var(--blue);color:white;font-weight:800;box-shadow:0 5px 12px rgba(37,99,235,.22)}.check:hover{background:#1d4ed8}
    /* BLOCK 6: Prediction result. */
    .result{display:none;margin-top:22px;padding:22px;border:1px solid var(--line);border-radius:12px}.result.show{display:block}.result.real{background:var(--green-bg);border-color:#a9d9bd}.result.fake{background:var(--red-bg);border-color:#f0b7b1}.result.error{background:var(--amber-bg);border-color:#eed18b}.result-main{display:flex;align-items:center;gap:15px}.icon{display:grid;place-items:center;width:50px;height:50px;border-radius:50%;background:var(--amber);color:white;font-size:24px;font-weight:900}.real .icon{background:var(--green)}.fake .icon{background:var(--red)}.result small{color:var(--muted);font-weight:750;letter-spacing:.08em}.result h3{margin:2px 0 0;font-size:28px}.bar{height:9px;margin:18px 0 8px;border-radius:99px;overflow:hidden;background:rgba(30,41,59,.12)}.bar span{display:block;width:0;height:100%;background:var(--blue);transition:width .3s ease}.confidence{margin:0;font-weight:800}.explain{margin:10px 0 0;color:var(--muted)}
    /* BLOCK 7: Samples, verification guidance, and benchmark warning. */
    .section{padding:44px 0 8px}.section h2{margin:0 0 5px;color:var(--navy);font-size:28px}.sub{margin:0 0 18px;color:var(--muted)}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}.sample{padding:18px;border:1px solid var(--line);border-radius:12px;background:var(--card);text-align:left;color:var(--ink)}.sample:hover{border-color:#91b4f7;background:#f8fbff}.sample b{display:block;margin-bottom:5px;color:var(--blue)}.sample span{color:var(--muted);font-size:14px}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.grid3 article{padding:20px;border:1px solid var(--line);border-radius:12px;background:var(--card)}.number{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;background:var(--blue2);color:var(--blue);font-weight:850}.grid3 h3{margin:14px 0 5px}.grid3 p{margin:0;color:var(--muted)}.note{margin:36px 0 58px;padding:18px 20px;border-left:4px solid #e19b2d;border-radius:8px;background:var(--amber-bg);color:#663b08}.note strong{display:block;margin-bottom:3px}footer{padding:24px;border-top:1px solid var(--line);color:var(--muted);font-size:13px;text-align:center}
    @media(max-width:760px){nav{min-height:62px}.status{font-size:12px}.hero{grid-template-columns:1fr;padding-top:42px}.model-card{margin-top:-10px}.checker{padding:18px}.checker-head{align-items:flex-start}.under{align-items:stretch;flex-direction:column}.check{width:100%}.grid2,.grid3{grid-template-columns:1fr}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
  </style>
</head>
<body>
  <!-- BLOCK 8: Visible application interface. -->
  <header><nav class="wrap"><div class="brand"><span class="mark">N</span>NewsCheck AI</div><div class="status"><span class="dot"></span>Pre-trained model ready</div></nav></header>
  <main class="wrap">
    <section class="hero"><div><div class="kicker">OFFLINE • BEGINNER FRIENDLY</div><h1>Check news<br><span>more carefully.</span></h1><p class="lead">Paste a headline and article text. The embedded model compares its language patterns with labeled training examples and returns a REAL NEWS or FAKE NEWS prediction.</p></div><aside class="model-card"><h2>Model information</h2><div class="model-row"><span>Algorithm</span><strong>Multinomial Naive Bayes</strong></div><div class="model-row"><span>Training dataset</span><strong>1,000 labeled samples</strong></div><div class="model-row"><span>Internet</span><strong>Not required</strong></div><div class="model-row"><span>Status</span><strong class="ready">Pre-trained and ready</strong></div></aside></section>

    <section class="checker"><div class="checker-head"><div><h2>News analyzer</h2><p>Use a headline plus two or three complete sentences for a more useful result.</p></div><button class="clear" id="clearButton" type="button">Clear</button></div><label for="newsInput">News text</label><textarea id="newsInput" maxlength="8000" placeholder="Example: The health department published its weekly report on the official website..."></textarea><div class="under"><span class="count" id="charCount">0 / 8000 characters</span><button class="check" id="checkButton" type="button">Analyze news</button></div><div class="result" id="result" role="status" aria-live="polite"><div class="result-main"><span class="icon" id="resultIcon">?</span><div><small>MODEL PREDICTION</small><h3 id="resultLabel">Result</h3></div></div><div class="bar"><span id="barFill"></span></div><p class="confidence" id="confidenceText"></p><p class="explain" id="explanation"></p></div></section>

    <section class="section"><h2>Try a sample</h2><p class="sub">Select a sample to test the model immediately.</p><div class="grid2"><button class="sample" data-example="The city health department published its weekly vaccination report on the official government website after a scheduled meeting. The figures are available in the linked public record."><b>Real-style sample</b><span>Contains an official source and verifiable report.</span></button><button class="sample" data-example="Shocking secret fruit cures every disease overnight! Doctors do not want you to know. Share this message immediately with twenty friends before it is deleted."><b>Fake-style sample</b><span>Contains a miracle claim and urgent sharing pressure.</span></button></div></section>

    <section class="section"><h2>Verify before sharing</h2><p class="sub">A model prediction is only a starting point.</p><div class="grid3"><article><span class="number">1</span><h3>Check the source</h3><p>Look for a named reporter, official document, or reputable publisher.</p></article><article><span class="number">2</span><h3>Check the date</h3><p>Old events and images are often presented as new information.</p></article><article><span class="number">3</span><h3>Compare reports</h3><p>Confirm the claim with at least two independent trusted sources.</p></article></div></section>
    <div class="note"><strong>Important benchmark warning</strong>The included holdout test scored 100% because the supplied dataset is synthetic and template-generated. This is not proof of 100% accuracy on real news, and real-world 90% accuracy is not guaranteed.</div>
  </main>
  <footer>NewsCheck AI • Standalone offline educational project • Your text is not uploaded</footer>

  <script>
    // BLOCK 9: The model below was trained before this file was built.
    const model = __MODEL_JSON__;

    // BLOCK 10: Convert input text into lowercase word tokens.
    function tokens(text){return text.toLowerCase().match(/[a-z0-9]+/g)||[]}

    // BLOCK 11: Calculate REAL and FAKE log-probability scores.
    function predict(text){const words=tokens(text),v=model.vocabulary.length,scores={};['REAL','FAKE'].forEach(label=>{const info=model.classes[label];let score=Math.log(info.documents/model.document_count);const denominator=info.total_words+v;words.forEach(word=>{score+=Math.log(((info.words[word]||0)+1)/denominator)});scores[label]=score});const max=Math.max(scores.REAL,scores.FAKE),real=Math.exp(scores.REAL-max),fake=Math.exp(scores.FAKE-max),realChance=real/(real+fake);return{label:realChance>=.5?'REAL':'FAKE',confidence:Math.round(Math.max(realChance,1-realChance)*100),matched:words.filter(word=>model.vocabulary.includes(word)).length,total:words.length}}

    // BLOCK 12: Connect controls to the interface.
    const input=document.querySelector('#newsInput'),count=document.querySelector('#charCount'),result=document.querySelector('#result'),resultLabel=document.querySelector('#resultLabel'),resultIcon=document.querySelector('#resultIcon'),confidence=document.querySelector('#confidenceText'),explanation=document.querySelector('#explanation'),bar=document.querySelector('#barFill');
    input.addEventListener('input',()=>count.textContent=`${input.value.length} / 8000 characters`);
    document.querySelector('#clearButton').addEventListener('click',()=>{input.value='';count.textContent='0 / 8000 characters';result.className='result';input.focus()});
    document.querySelectorAll('.sample').forEach(button=>button.addEventListener('click',()=>{input.value=button.dataset.example;input.dispatchEvent(new Event('input'));input.scrollIntoView({behavior:'smooth',block:'center'});setTimeout(analyze,250)}));
    document.querySelector('#checkButton').addEventListener('click',analyze);

    // BLOCK 13: Validate the text and display the prediction.
    function analyze(){const text=input.value.trim();if(text.length<40){show('error','MORE TEXT NEEDED','!',0,'Enter at least 40 characters and one or two complete sentences.');return}const answer=predict(text),isReal=answer.label==='REAL',coverage=answer.total?Math.round(answer.matched/answer.total*100):0,safeConfidence=Math.min(answer.confidence,97);show(isReal?'real':'fake',isReal?'REAL NEWS':'FAKE NEWS',isReal?'✓':'!',safeConfidence,`The model recognized ${answer.matched} trained vocabulary words (${coverage}% word coverage). Treat this as a hint and verify the source, date, and evidence.`)}
    function show(type,label,icon,pct,message){result.className=`result show ${type}`;resultLabel.textContent=label;resultIcon.textContent=icon;confidence.textContent=pct?`Model confidence: ${pct}%`:'';bar.style.width=`${pct}%`;explanation.textContent=message;result.scrollIntoView({behavior:'smooth',block:'nearest'})}
  </script>
</body></html>'''

html = html.replace("__MODEL_JSON__", json.dumps(model, separators=(",", ":")))
(base / "NewsCheck_AI.html").write_text(html, encoding="utf-8")
print("Built", base / "NewsCheck_AI.html")
