import os
import datetime
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import json

def top_n(data, labels, n=6):
    # Retorna os top N, soma o resto como "outros"
    pairs = sorted(zip(data, labels), reverse=True)
    if len(pairs) <= n:
        return list(data), list(labels)
    top = pairs[:n]
    others = sum([v for v, _ in pairs[n:]])
    if others:
        top.append((others, "outros"))
    data, labels = zip(*top)
    return list(data), list(labels)

def plot_pie(data, labels, title="", colors=None):
    buf = BytesIO()
    total = sum(data)
    if not data or (len(data) == 1 and (labels[0].lower() in ["nenhum", "sem dados", "sem engine detectada", "outros"] or data[0] == 0)):
        plt.figure(figsize=(3.2, 3.2))
        wedges, texts, autotexts = plt.pie(
            [1], labels=["Sem dados"], colors=["#444"], startangle=90,
            textprops=dict(color='white', fontsize=16, fontweight='bold')
        )
        plt.tight_layout()
        plt.axis('equal')
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode()

    plt.figure(figsize=(3.2, 3.2))
    def my_labels(pct, allvals):
        absolute = int(round(pct / 100. * total))
        return f"{int(pct)}%" if pct >= 8 else ""
    wedges, texts, autotexts = plt.pie(
        data,
        labels=labels,
        startangle=90,
        autopct=lambda pct: my_labels(pct, data),
        colors=colors,
        textprops=dict(color='white', fontsize=16, fontweight='bold')
    )
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')
    for txt in texts:
        txt.set_fontsize(14)
        txt.set_fontweight('bold')
    plt.tight_layout()
    plt.axis('equal')
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode()

def export_html_report(result_json, file_path):
    result = json.loads(result_json)
    now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    # Contadores
    lang_counter = {}
    for langs in result.get('lang_map', {}).values():
        for l in langs:
            lang_counter[l] = lang_counter.get(l, 0) + 1
    engine_counter = {}
    for engs in result.get('engine_map', {}).values():
        for e in engs:
            engine_counter[e] = engine_counter.get(e, 0) + 1
    mid_counter = {}
    for mids in result.get('middleware_map', {}).values():
        for m in mids:
            mid_counter[m] = mid_counter.get(m, 0) + 1
    prot_counter = {}
    for prots in result.get('prot_map', {}).values():
        for p in prots:
            prot_counter[p] = prot_counter.get(p, 0) + 1
    crypto_counter = {}
    for crypts in result.get('crypto_map', {}).values():
        for c in crypts:
            crypto_counter[c] = crypto_counter.get(c, 0) + 1

    # Gráficos pizza: só top N + "outros"
    lang_data, lang_labels = top_n(list(lang_counter.values()), list(lang_counter.keys()), 6)
    pie_lang = plot_pie(lang_data, lang_labels, colors=["#f5b042","#90ee90","#5fcfff","#bb86fc","#f77","#f9c","#aaa"])
    engine_data, engine_labels = top_n(list(engine_counter.values()), list(engine_counter.keys()), 6)
    pie_engine = plot_pie(engine_data, engine_labels, colors=["#ffd700","#2196f3","#33dd99","#ccc","#888","#fff"])
    mid_data, mid_labels = top_n(list(mid_counter.values()), list(mid_counter.keys()), 6)
    pie_mid = plot_pie(mid_data, mid_labels, colors=["#ff4c99","#ffa","#1cc","#b9c","#fc0","#0cf","#888"])
    prot_data, prot_labels = top_n(list(prot_counter.values()), list(prot_counter.keys()), 6)
    pie_prot = plot_pie(prot_data, prot_labels, colors=["#ff8c8c","#c62828","#ffbdbd","#f99","#fcc","#ddd"])
    crypto_data, crypto_labels = top_n(list(crypto_counter.values()), list(crypto_counter.keys()), 6)
    pie_crypto = plot_pie(crypto_data, crypto_labels, colors=["#bb86fc","#fb8","#bdb","#6af","#f5b042","#888"])

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Loki Analyzer - Relatório HTML</title>
    <link href="https://fonts.googleapis.com/css?family=Montserrat:700,400&display=swap" rel="stylesheet">
    <style>
        body {{
            background: #202225;
            color: #e0e0e0;
            font-family: 'Montserrat', Arial, sans-serif;
            margin: 0; padding: 0;
        }}
        h1 {{
            color: #f5b042;
            text-align: center;
            margin-top: 24px;
            font-size: 2.7em;
        }}
        .sec {{
            margin: 0 4vw 36px 4vw;
        }}
        h2.section {{
            color: #33cfff;
            margin-top: 40px;
            margin-bottom: 8px;
            font-size: 2.2em;
        }}
        .sumbox {{
            margin-bottom: 24px;
        }}
        .b {{
            font-weight: bold;
            color: #f5b042;
        }}
        .l {{ color: #90ee90; font-weight: bold; }}
        .p {{ color: #ff8c8c; font-weight: bold; }}
        .c {{ color: #bb86fc; font-weight: bold; }}
        .e {{ color: #5fcfff; font-weight: bold; }}
        .m {{ color: #ff4c99; font-weight: bold; }}
        code {{
            font-family: 'Consolas', 'Courier New', monospace;
            background: #181a1b;
            color: #f5b042;
            padding: 2px 8px; border-radius: 4px;
            font-size: 1em;
        }}
        .kv {{ color: #f5b042; font-weight:bold; }}
        .vlist {{ color: #90ee90; }}
        .details-table {{
            background: #232629; color: #fff;
            width: 99%; margin: 0 auto; border-collapse: collapse; border-radius: 7px;
            margin-bottom: 44px;
        }}
        .details-table th {{
            background: #181a1b; color: #ffd700; font-size: 1.13em;
        }}
        .details-table th, .details-table td {{
            border: 1px solid #444;
            padding: 7px 15px;
            text-align: left;
        }}
        .details-table tr:nth-child(even) {{ background: #232629; }}
        .details-table tr:nth-child(odd) {{ background: #202225; }}
        .chartrow {{
            display: flex;
            flex-wrap: wrap;
            margin-bottom: 18px;
            justify-content: left;
        }}
        .chartbox {{
            min-width: 260px;
            margin: 0 20px;
            text-align: center;
        }}
        .chartbox img {{ background: #232629; border-radius: 14px; width: 230px; height: 230px; }}
        .chartbox label {{
            display: block;
            color: #e0e0e0;
            margin-top: 6px;
            font-size: 1.22em;
            font-weight: bold;
        }}
        .warn {{ color: #ff7575; font-weight:bold; }}
        .footer {{
            color: #aaa; font-size: 0.98em; text-align: right; margin-top: 28px; margin-right: 32px;
        }}
        @media (max-width: 1200px) {{
            .chartrow {{ flex-direction: column; align-items:center; }}
        }}
    </style>
</head>
<body>
<h1>Loki Analyzer - Relatório HTML</h1>
<div class="sec">
    <div class="sumbox">
        <span class="b">Pasta analisada:</span> <code>{result.get('game_path','')}</code><br>
        <span class="b">Arquivos analisados:</span> <span class="e">{result.get('analyzed_files','')}</span><br>
        <span class="b">Data/Hora:</span> {now}
    </div>
    <hr>
    <h2 class="section">Resumo</h2>
    <div style="margin-left:13px;">
        <span class="l"><b>Linguagens:</b></span>
        <span class="vlist">{", ".join(result.get("languages_detected",[])) or "-"}</span><br>
        <span class="e"><b>Engines:</b></span>
        <span class="vlist">{", ".join(set(e for engs in result.get("engine_map",{}).values() for e in engs)) or "-"}</span><br>
        <span class="m"><b>Middlewares:</b></span>
        <span class="vlist">{", ".join(set(m for mids in result.get("middleware_map",{}).values() for m in mids)) or "-"}</span><br>
        <span class="p"><b>Proteções:</b></span> {", ".join(result.get("protections",[])) or "-"}<br>
        <span class="c"><b>Criptografia:</b></span> {", ".join(result.get("crypto_signals",[])) or "-"}<br>
        <span class="b" style="color:#ffd700;"><b>Heurísticas Lua:</b></span> {", ".join(str(x) for x in result.get("lua_heuristics",[])) or "-"}
    </div>
    <br>
    <h2 class="section">Resumo Visual</h2>
    <div class="chartrow">
        <div class="chartbox">
            <img src="data:image/png;base64,{pie_lang}" width="230" height="230"><label>Linguagens</label>
            <div style="font-size:10.5pt;color:#ccc;">{"<br>".join([f"{k}: {lang_counter[k]}" for k in lang_counter])}</div>
        </div>
        <div class="chartbox">
            <img src="data:image/png;base64,{pie_engine}" width="230" height="230"><label>Engines</label>
            <div style="font-size:10.5pt;color:#ccc;">{"<br>".join([f"{k}: {engine_counter[k]}" for k in engine_counter])}</div>
        </div>
        <div class="chartbox">
            <img src="data:image/png;base64,{pie_mid}" width="230" height="230"><label>Middlewares</label>
            <div style="font-size:10.5pt;color:#ccc;">{"<br>".join([f"{k}: {mid_counter[k]}" for k in mid_counter])}</div>
        </div>
        <div class="chartbox">
            <img src="data:image/png;base64,{pie_prot}" width="230" height="230"><label>Proteções</label>
            <div style="font-size:10.5pt;color:#ccc;">{"<br>".join([f"{k}: {prot_counter[k]}" for k in prot_counter])}</div>
        </div>
        <div class="chartbox">
            <img src="data:image/png;base64,{pie_crypto}" width="230" height="230"><label>Criptografia</label>
            <div style="font-size:10.5pt;color:#ccc;">{"<br>".join([f"{k}: {crypto_counter[k]}" for k in crypto_counter])}</div>
        </div>
    </div>
</div>

<div class="sec">
    <h2 class="section">Detalhamento de Executáveis/DLLs</h2>
    <table class="details-table">
        <tr>
            <th>Arquivo</th>
            <th>Tipo</th>
            <th>Linguagens</th>
            <th>Engine</th>
            <th>Middlewares</th>
            <th>Proteções</th>
            <th>Criptografia</th>
            <th>Entropia</th>
            <th>Heurística Lua</th>
        </tr>
"""
    for f in result.get("executables",[]):
        html += "<tr>"
        html += f"<td><code>{os.path.basename(f)}</code></td>"
        # Tipo (magic)
        html += f"<td>{result.get('magic_map', {}).get(f, '-') or '-'}</td>"
        # Linguagem
        langs = result.get("lang_map", {}).get(f, [])
        html += f"<td>{', '.join(langs) if langs else '-'}</td>"
        # Engine
        engines = result.get("engine_map", {}).get(f, [])
        html += f"<td>{', '.join(engines) if engines else '-'}</td>"
        # Middlewares
        mids = result.get("middleware_map", {}).get(f, [])
        html += f"<td>{', '.join(mids) if mids else '-'}</td>"
        # Proteções
        prots = result.get("prot_map", {}).get(f, [])
        html += f"<td>{', '.join(prots) if prots else '-'}</td>"
        # Criptografia
        crypts = result.get("crypto_map", {}).get(f, [])
        html += f"<td>{', '.join(crypts) if crypts else '-'}</td>"
        # Entropia
        ent = result.get("entropy_map", {}).get(f, '-')
        html += f"<td>{ent}</td>"
        # Heurística Lua (a implementar por arquivo se quiser)
        html += "<td>-</td>"
        html += "</tr>"
    html += "</table>"

    # Agrupamentos
    html += '<h2 class="section">Arquivos por Linguagem</h2>'
    lang_map = result.get("lang_map", {})
    if lang_map:
        for path, langs in lang_map.items():
            html += f"<b>{', '.join(langs)}:</b> <code>{os.path.basename(path)}</code><br>"
    else:
        html += '<span class="l">- Nenhum arquivo identificado por linguagem -</span><br>'

    html += '<h2 class="section">Arquivos por Proteção</h2>'
    prot_map = result.get("prot_map", {})
    if prot_map:
        for path, prots in prot_map.items():
            html += f"<b>{', '.join(prots)}:</b> <code>{os.path.basename(path)}</code><br>"
    else:
        html += '<span class="p">- Nenhum arquivo identificado por proteção/ofuscação -</span><br>'

    html += '<h2 class="section">Arquivos por Criptografia</h2>'
    crypto_map = result.get("crypto_map", {})
    if crypto_map:
        for path, crypts in crypto_map.items():
            html += f"<b>{', '.join(crypts)}:</b> <code>{os.path.basename(path)}</code><br>"
    else:
        html += '<span class="c">- Nenhum arquivo identificado por criptografia -</span><br>'

    html += '<h2 class="section">Arquivos por Middleware</h2>'
    mid_map = result.get("middleware_map", {})
    if mid_map:
        for path, mids in mid_map.items():
            html += f"<b>{', '.join(mids)}:</b> <code>{os.path.basename(path)}</code><br>"
    else:
        html += '<span class="m">- Nenhum arquivo identificado por middleware -</span><br>'

    html += f"""
<hr>
<div class="footer">
Copyright (c) 2025 Lyrien<br>
Relatório gerado automaticamente pelo Loki Analyzer.
</div>
</div>
</body></html>
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
