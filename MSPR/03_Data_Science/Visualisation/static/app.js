// Configuration Tailwind Typography : Outfit & Inter fonts included via CDN
// Logic script for GouvData ML predictions

document.addEventListener('DOMContentLoaded', () => {

    const API_URL = '/api/results';
    let globalLevelsData = {};

    // Charger les données de l'API
    fetch(API_URL)
        .then(response => response.json())
        .then(data => {
            updateKPIs(data.summary);
            globalLevelsData = data.levels;

            // Rendre par défaut le niveau Région
            renderTable('region', 'Région');

            // Rendre les diagrammes
            renderPolarChart('chartReal', data.political_real);
            renderPolarChart('chartPred', data.political_predicted);

            setupTabs();
        })
        .catch(err => console.error("API Error: ", err));

    function setupTabs() {
        const tabs = document.querySelectorAll('.level-tab');

        tabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                // Remove active styling from all tabs
                tabs.forEach(t => {
                    t.classList.remove('active', 'text-cyan-400', 'bg-cyan-900/30', 'border-cyan-500/50', 'shadow-[0_0_10px_rgba(6,182,212,0.2)]');
                    t.classList.add('text-gray-500', 'hover:text-gray-300', 'hover:bg-gray-800/50', 'border-transparent');
                    
                    // Remove neon span wrap
                    if(t.querySelector('span.neon-text-cyan')) {
                        t.innerHTML = t.querySelector('span.neon-text-cyan').innerHTML;
                    }
                });

                // Add active styling to clicked tab
                const target = e.currentTarget;
                target.classList.add('active', 'text-cyan-400', 'bg-cyan-900/30', 'border-cyan-500/50', 'shadow-[0_0_10px_rgba(6,182,212,0.2)]');
                target.classList.remove('text-gray-500', 'hover:text-gray-300', 'hover:bg-gray-800/50', 'border-transparent');
                
                // Add neon span wrap
                target.innerHTML = `<span class="neon-text-cyan">${target.innerHTML.trim()}</span>`;

                // Fetch level ID and text name
                const levelId = target.getAttribute('data-level');
                const levelName = target.innerText.trim().substring(3); // Remove emoji

                // Opacity animation transition
                const tableCont = document.getElementById('table-container');
                tableCont.style.opacity = '0.3';
                setTimeout(() => {
                    renderTable(levelId, levelName);
                    tableCont.style.opacity = '1';
                }, 200);
            });
        });
    }

    function updateKPIs(summary) {
        document.getElementById('kpi-records').textContent = summary.total_records;
        document.getElementById('kpi-model-acc').textContent = summary.model_accuracy + '%';
        document.getElementById('kpi-dept-acc').textContent = summary.dept_accuracy + '%';
        document.getElementById('kpi-noise').textContent = "σ = 0.45";
        document.getElementById('kpi-flip').textContent = "15%";

        // Animate Progress Bars
        setTimeout(() => {
            document.getElementById('pb-model-acc').style.width = summary.model_accuracy + '%';
            document.getElementById('pb-dept-acc').style.width = summary.dept_accuracy + '%';
        }, 300);
    }

    function renderTable(levelId, levelName) {
        if (!globalLevelsData || !globalLevelsData[levelId]) return;

        const entities = globalLevelsData[levelId];
        const tbody = document.getElementById('table-body');
        tbody.innerHTML = ''; // clear table

        // Update Table Headers
        document.getElementById('table-title').textContent = "Cartographie Réseau Neural vs Réalité";
        document.getElementById('table-badge').textContent = 'NIVEAU : ' + levelName.toUpperCase();
        document.getElementById('th-entity').textContent = 'Zone Télémétrique (' + levelName + ')';

        // Footnote dynamically updated
        const footerNote = document.getElementById('table-footer-note');
        if (levelId === 'region' || levelId === 'departement') {
            footerNote.textContent = "Note: Le modèle a intentionnellement 83% d'accuracy. Il se trompe donc sur certains de ces niveaux macro.";
        } else {
            footerNote.textContent = "Note : Sur les cantons et communes, le modèle prédit la tendance locale à l'aide des moyennes, l'accuracy peut beaucoup y varier.";
        }

        entities.forEach((item, index) => {
            const tr = document.createElement('tr');

            // Zebra striping for neon theme
            tr.className = index % 2 === 0 ? "bg-[#131b2c] hover:bg-cyan-900/40 border-b border-slate-800/80 transition-colors" : "bg-[#0f1725] hover:bg-cyan-900/40 border-b border-slate-800/80 transition-colors";

            // Badge style for predictions with glowing effects
            const getBadge = (val, cand) => {
                if (!val || val === "N/A" || val === "Unknown") return `<span class="text-slate-600 font-mono text-xs italic">OFFLINE</span>`;

                let badge = '';
                const candName = cand && cand !== "N/A" ? cand : "UNK";

                if (val.includes('Ensemble')) badge = `<span class="px-3 py-1 bg-cyan-950/40 text-cyan-400 font-bold rounded-md text-xs border border-cyan-500/50 shadow-[0_0_8px_rgba(6,182,212,0.3)] min-w-[120px] inline-block font-mono tracking-wide">[ ${candName} - ENS ] 🔵</span>`;
                else if (val.includes('NUPES')) badge = `<span class="px-3 py-1 bg-fuchsia-950/40 text-fuchsia-400 font-bold rounded-md text-xs border border-fuchsia-500/50 shadow-[0_0_8px_rgba(217,70,239,0.3)] min-w-[120px] inline-block font-mono tracking-wide">[ ${candName} - NUP ] 🔴</span>`;
                else if (val.includes('RN')) badge = `<span class="px-3 py-1 bg-slate-800/80 text-white font-bold rounded-md text-xs border border-slate-600 shadow-[0_0_8px_rgba(255,255,255,0.2)] min-w-[120px] inline-block font-mono tracking-wide">[ ${candName} - RN_ ] ⚫</span>`;
                else if (val.includes('LR')) badge = `<span class="px-3 py-1 bg-indigo-950/40 text-indigo-400 font-bold rounded-md text-xs border border-indigo-500/50 shadow-[0_0_8px_rgba(99,102,241,0.3)] min-w-[120px] inline-block font-mono tracking-wide">[ ${candName} - LR_ ] 🌀</span>`;
                else badge = `<span class="px-3 py-1 bg-gray-800/50 text-gray-300 font-bold rounded-md text-xs border border-gray-600 min-w-[120px] inline-block font-mono tracking-wide">[ ${candName} - ${val} ]</span>`;

                return `<div class="flex items-center min-w-max">${badge}</div>`;
            };

            // Status style (cyberpunk style)
            let statusBadge = '';
            if (item.is_correct === true) {
                statusBadge = `<span class="inline-flex justify-center items-center gap-1.5 px-3 py-1 bg-emerald-950/40 text-emerald-400 rounded-md font-bold shadow-[0_0_10px_rgba(16,185,129,0.2)] border border-emerald-500/50 w-28 text-xs font-mono tracking-widest"><svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.815a.75.75 0 011.05-.145z" clip-rule="evenodd"/></svg> VÉRIFIÉ</span>`;
            } else if (item.is_correct === false) {
                statusBadge = `<span class="inline-flex justify-center items-center gap-1.5 px-3 py-1 bg-rose-950/40 text-rose-400 rounded-md font-bold shadow-[0_0_10px_rgba(244,63,94,0.2)] border border-rose-500/50 w-28 text-xs font-mono tracking-widest"><svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg> ANOMALY</span>`;
            } else {
                statusBadge = `<span class="inline-flex justify-center items-center gap-1.5 px-3 py-1 bg-slate-800 text-slate-300 rounded-md font-bold shadow-sm w-28 text-xs border border-slate-600 font-mono tracking-widest">SIMULÉ._</span>`;
            }

            // Confidence rendering with neon bar
            const getConfHTML = (conf) => {
                if (!conf) return '-';
                const c = parseInt(conf);
                let colorClass = "from-cyan-400 to-blue-500 bg-gradient-to-r shadow-[0_0_8px_rgba(6,182,212,0.6)]";
                if (c > 85) colorClass = "from-emerald-400 to-teal-500 bg-gradient-to-r shadow-[0_0_8px_rgba(52,211,153,0.6)]";
                else if (c < 75) colorClass = "from-rose-400 to-pink-500 bg-gradient-to-r shadow-[0_0_8px_rgba(244,63,94,0.6)]";
                
                return `<div class="flex items-center justify-center gap-3"><span class="w-8 text-right font-black font-mono text-slate-200">${conf}</span><div class="w-20 h-1.5 bg-slate-800 justify-start rounded-full flex overflow-hidden border border-slate-700/50"><div class="${colorClass} h-1.5 rounded-full" style="width: ${conf}"></div></div></div>`;
            };

            tr.innerHTML = `
                <td class="px-6 py-4 font-black text-gray-200 truncate max-w-[200px] flex items-center gap-3">
                    <div class="w-2 h-2 rounded-full bg-cyan-400 shadow-[0_0_5px_#22d3ee] animate-pulse"></div> 
                    <span class="tracking-wider uppercase text-xs">${item.entity}</span>
                </td>
                <td class="px-6 py-4">${getBadge(item.predicted, item.pred_cand)}</td>
                <td class="px-6 py-4 text-center">${getConfHTML(item.conf)}</td>
                <td class="px-6 py-4">${getBadge(item.real, item.real_cand)}</td>
                <td class="px-6 py-4 text-center">${statusBadge}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    function renderPolarChart(canvasId, chartData) {
        const ctx = document.getElementById(canvasId).getContext('2d');

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: chartData.map(d => d.party),
                datasets: [{
                    data: chartData.map(d => d.count),
                    backgroundColor: chartData.map(d => d.color),
                    borderWidth: 2,
                    borderColor: '#0b0f19',
                    hoverOffset: 12
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#cbd5e1',
                            usePointStyle: true,
                            padding: 20,
                            font: { family: "'Space Grotesk', sans-serif", size: 14, weight: '500' }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        padding: 16,
                        cornerRadius: 8,
                        titleFont: { size: 14, family: "'Space Grotesk', sans-serif" },
                        bodyFont: { size: 16, weight: 'bold', family: "'Space Grotesk', sans-serif" }
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeOutQuart'
                }
            }
        });
    }
});