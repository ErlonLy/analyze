(function() {
  const data = window.LOKI_DATA;

  // Função auxiliar para links
  function createSearchLinks(fname, sha) {
    const links = [];
    if (sha) {
      links.push(`<a href="https://www.virustotal.com/gui/file/${sha}" target="_blank">🔍 VirusTotal</a>`);
      links.push(`<a href="https://www.hybrid-analysis.com/search?query=${sha}" target="_blank">HybridAnalysis</a>`);
      links.push(`<a href="https://malshare.com/search.php?query=${sha}" target="_blank">MalShare</a>`);
      links.push(`<a href="https://malpedia.caad.fkie.fraunhofer.de/search/?query=${sha}" target="_blank">Malpedia</a>`);
      links.push(`<a href="https://any.run/search?q=${sha}" target="_blank">ANY.RUN</a>`);
    } else {
      links.push("<span style='color:#ff8c8c'>❌ Não foi possível gerar hash.</span>");
    }
    links.push(`<a href="https://www.google.com/search?q=${encodeURIComponent(fname)}+cheat+exploit+site:unknowncheats.me" target="_blank">Google Cheats/Exploits</a>`);
    links.push(`<a href="https://www.reddit.com/search/?q=${encodeURIComponent(fname)}" target="_blank">Reddit</a>`);
    return links.join(' | ');
  }

  // Resumo e gráficos
  document.getElementById("summary").innerHTML = `
      <span class="b">Pasta analisada:</span> <code>${data.game_path||""}</code><br>
      <span class="b">Arquivos analisados:</span> <span class="e">${data.analyzed_files||""}</span><br>
      <span class="l"><b>Linguagens:</b></span> ${(data.languages_detected||[]).join(', ')||"-"}<br>
      <span class="p"><b>Proteções:</b></span> ${(data.protections||[]).join(', ')||"-"}<br>
      <span class="c"><b>Criptografia:</b></span> ${(data.crypto_signals||[]).join(', ')||"-"}<br>
    `;
  function countMap(mapObj) {
      let counter = {};
      for (const v of Object.values(mapObj || {})) {
          for (const x of v) counter[x] = (counter[x]||0)+1;
      }
      return counter;
  }
  const chartCfgs = [
    {id:"pieLang", map:data.lang_map, colors:["#f5b042","#90ee90","#5fcfff","#bb86fc","#f77","#f9c","#aaa"]},
    {id:"pieEngine", map:data.engine_map, colors:["#ffd700","#2196f3","#33dd99","#ccc","#888","#fff"]},
    {id:"pieMid", map:data.middleware_map, colors:["#ff4c99","#ffa","#1cc","#b9c","#fc0","#0cf","#888"]},
    {id:"pieProt", map:data.prot_map, colors:["#ff8c8c","#c62828","#ffbdbd","#f99","#fcc","#ddd"]},
    {id:"pieCrypto", map:data.crypto_map, colors:["#bb86fc","#fb8","#bdb","#6af","#f5b042","#888"]}
  ];
  function topN(dataArr, labels, n) {
      let pairs = [];
      for (let i = 0; i < dataArr.length; i++) pairs.push({val: dataArr[i], label: labels[i]});
      pairs.sort((a, b) => b.val - a.val);
      if (pairs.length <= n) return [dataArr, labels];
      let top = pairs.slice(0, n);
      let others = pairs.slice(n).reduce((acc, x) => acc + x.val, 0);
      if (others) top.push({val: others, label: "outros"});
      return [top.map(x=>x.val), top.map(x=>x.label)];
  }
  chartCfgs.forEach(cfg=>{
    const counts = countMap(cfg.map);
    let vals = Object.values(counts), labels = Object.keys(counts);
    [vals, labels] = topN(vals, labels, 6);
    new Chart(document.getElementById(cfg.id), {
      type: 'pie',
      data: {
        labels, datasets: [{data:vals, backgroundColor:cfg.colors}]
      },
      options: {
        plugins: {legend:{labels:{color:'#fff', font:{size:15}}}},
        animation: { animateScale:true },
      }
    });
  });

  // Tabela de detalhes
  let table = `
    <h2 class="section">Detalhamento de Executáveis/DLLs</h2>
    <table class="details-table">
    <tr>
      <th>Arquivo</th><th>Tipo</th><th>Linguagens</th><th>Engine</th><th>Middlewares</th>
      <th>Proteções</th><th>Criptografia</th><th>Entropia</th>
    </tr>
  `;
  for (const f of (data.executables||[])) {
    let fname = f.split(/[\\/]/).pop();
    table += `<tr>
      <td><code>${fname}</code></td>
      <td>${data.magic_map && data.magic_map[f] || '-'}</td>
      <td>${data.lang_map && data.lang_map[f] ? data.lang_map[f].join(", ") : '-'}</td>
      <td>${data.engine_map && data.engine_map[f] ? data.engine_map[f].join(", ") : '-'}</td>
      <td>${data.middleware_map && data.middleware_map[f] ? data.middleware_map[f].join(", ") : '-'}</td>
      <td>${data.prot_map && data.prot_map[f] ? data.prot_map[f].join(", ") : '-'}</td>
      <td>${data.crypto_map && data.crypto_map[f] ? data.crypto_map[f].join(", ") : '-'}</td>
      <td>${data.entropy_map && data.entropy_map[f] !== undefined ? data.entropy_map[f] : '-'}</td>
    </tr>`;
  }
  table += "</table>";
  document.getElementById("details").innerHTML = table;

  // Busca em bancos públicos
  let hashDiv = '<h2 class="section">Busca em bancos públicos de malware/cheats/exploits</h2>';
  const hashes = data.file_hashes || {};
  if (Object.keys(hashes).length === 0) {
    hashDiv += "<span style='color:#ff8c8c'>⚠️ Nenhum arquivo encontrado para gerar hashes ou realizar buscas.</span>";
  } else {
    for (const [filepath, sha] of Object.entries(hashes)) {
      const fname = filepath.split(/[\\/]/).pop();
      hashDiv += `<div style='margin-bottom: 16px;'><b>${fname}</b><br>`;
      hashDiv += createSearchLinks(fname, sha);
      hashDiv += "</div>";
    }
  }
  hashDiv += `
    <hr>
    <div style='margin-top: 12px; font-size: 0.92em; color:#bbb;'>
      🔍 <b>Onde foi pesquisado:</b><br>
      - <a href='https://www.virustotal.com/' target='_blank'>VirusTotal</a>: Análise de malware e hashes conhecidos.<br>
      - <a href='https://www.hybrid-analysis.com/' target='_blank'>HybridAnalysis</a>: Relatórios de sandbox e comportamento.<br>
      - <a href='https://malshare.com/' target='_blank'>MalShare</a>: Banco de dados de hashes maliciosos.<br>
      - <a href='https://malpedia.caad.fkie.fraunhofer.de/' target='_blank'>Malpedia</a>: Enciclopédia de famílias de malware.<br>
      - <a href='https://any.run/' target='_blank'>ANY.RUN</a>: Sandbox interativo e relatórios detalhados.<br>
      - <b>Google e Reddit:</b> Fóruns e sites públicos de cheats/exploits.
    </div>`;
  document.getElementById("hashes").innerHTML = hashDiv;

  // Animações
  anime({
    targets: '.chartbox canvas',
    opacity: [0,1],
    scale: [0.85,1],
    delay: anime.stagger(200)
  });
  anime({
    targets: 'h1, .section',
    translateY: [-40,0],
    opacity: [0,1],
    duration: 1100,
    delay: anime.stagger(120)
  });
})();
