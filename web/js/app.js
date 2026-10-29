/**
 * CaseZero - Master Front-End Controller
 * Connects UI tabs, corkboard, tree, binary search animator, and JSON API.
 */

class CaseZeroApp {
  constructor() {
    this.session = null;
    this.activeTab = 'suspects';
    this.selectedCulprit = null;
    this.selectedAccomplice = null;

    this.corkboard = null;
    this.treeUI = null;
    this.binSearchAnimator = null;

    this.init();
  }

  async init() {
    this.bindEvents();
    await this.fetchCasesCatalog();
  }

  // ---------------- API Calls ----------------
  async api(endpoint, method = 'GET', body = null) {
    try {
      const options = { method, headers: { 'Content-Type': 'application/json' } };
      if (body) options.body = JSON.stringify(body);
      const res = await fetch(endpoint, options);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.error('API Error:', err);
      return null;
    }
  }

  async fetchCasesCatalog() {
    const cases = await this.api('/api/cases');
    const grid = document.getElementById('caseCardsGrid');
    if (!grid || !cases) return;

    grid.innerHTML = cases.map(c => `
      <div class="case-card" data-case-id="${c.id}">
        <img src="${c.image}" alt="${c.title}" class="case-thumb" onerror="this.src='assets/img/scenes/vault_scene.svg'">
        <div class="case-card-body">
          <div class="case-meta-row">
            <span class="case-difficulty">${c.difficulty.toUpperCase()}</span>
            <span class="case-suspects-count">${c.suspect_count} SUSPECTS</span>
          </div>
          <h3 class="case-title">${c.title}</h3>
          <p class="case-briefing">${c.briefing}</p>
          <button class="btn-start-case">SELECT CASE FILE</button>
        </div>
      </div>
    `).join('');

    grid.querySelectorAll('.case-card').forEach(card => {
      card.addEventListener('click', (e) => {
        const caseId = card.dataset.caseId;
        this.startCase(caseId);
      });
    });
  }

  async startCase(caseId, seed = null) {
    const res = await this.api('/api/session/start', 'POST', { case_id: caseId, seed });
    if (!res) return;

    this.session = res;
    document.getElementById('titleScreen').classList.add('hidden');
    document.getElementById('gameScreen').classList.remove('hidden');

    this.initVisualizers();
    this.render();

    // Check onboarding preference
    if (!localStorage.getItem('casezero_onboarding_done')) {
      document.getElementById('onboardingOverlay').classList.remove('hidden');
    }
  }

  initVisualizers() {
    // 1. Corkboard Canvas
    const canvas = document.getElementById('corkboardCanvas');
    if (canvas && !this.corkboard) {
      this.corkboard = new CorkboardGraph(canvas, {
        onSelectSuspect: (id) => this.openDossier(id),
        onRequestPath: (u, v) => this.queryPath(u, v),
        onPathCleared: () => {
          document.getElementById('bfsPathBanner').classList.add('hidden');
        }
      });
    }

    // 2. Decision Tree UI
    const treeContainer = document.getElementById('treeContainer');
    if (treeContainer && !this.treeUI) {
      this.treeUI = new InvestigationTreeUI(treeContainer, {
        onExplore: (leadId) => this.exploreLead(leadId)
      });
    }

    // 3. Binary Search Animator
    const tbody = document.getElementById('logsTableBody');
    const traceBox = document.getElementById('alibiTraceBox');
    if (tbody && traceBox && !this.binSearchAnimator) {
      this.binSearchAnimator = new BinarySearchAnimator(tbody, traceBox);
    }
  }

  render() {
    if (!this.session) return;

    // Header & AP
    document.getElementById('topCaseName').textContent = this.session.case_title;
    this.renderAP(this.session.ap, this.session.max_ap);

    // Suspect Strip
    this.renderSuspectStrip();

    // Active Tab View
    this.renderSuspectsTab();
    this.renderConnectionsTab();
    this.renderLeadsTab();
    this.renderEvidenceTab();
    this.renderAlibiTab();
    this.renderAccuseTab();

    // Check Contradiction Siren
    if (this.session.contradiction_detected && this.session.status === 'PLAYING') {
      this.showSirenOverlay();
    } else {
      document.getElementById('sirenOverlay').classList.add('hidden');
    }
  }

  renderAP(ap, maxAp) {
    const row = document.getElementById('apPipsRow');
    const text = document.getElementById('apNumberText');
    if (!row || !text) return;

    text.textContent = `${ap}/${maxAp}`;
    row.innerHTML = '';
    for (let i = 0; i < maxAp; i++) {
      const pip = document.createElement('div');
      pip.className = `ap-pip ${i < ap ? 'filled' : ''}`;
      row.appendChild(pip);
    }
  }

  renderSuspectStrip() {
    const strip = document.getElementById('suspectStrip');
    const countEl = document.getElementById('stripViableCount');
    if (!strip || !this.session.suspects) return;

    const viable = this.session.suspects.filter(s => s.is_viable);
    if (countEl) countEl.textContent = `${viable.length} Viable / ${this.session.suspects.length} Total`;

    strip.innerHTML = this.session.suspects.map(s => `
      <div class="strip-card ${s.is_viable ? 'viable' : 'cleared'}" data-id="${s.id}">
        <div class="strip-thumb-wrap">
          <img src="${s.image}" alt="${s.name}" class="strip-thumb" onerror="this.src='assets/img/suspects/placeholder.svg'">
          ${s.is_eliminated ? '<div class="stamp-cleared">CLEARED</div>' : ''}
        </div>
        <span class="strip-name">${s.name.split(' ')[0]}</span>
      </div>
    `).join('');

    strip.querySelectorAll('.strip-card').forEach(card => {
      card.addEventListener('click', () => {
        this.openDossier(card.dataset.id);
      });
    });
  }

  renderSuspectsTab() {
    const grid = document.getElementById('suspectsGrid');
    if (!grid || !this.session.suspects) return;

    grid.innerHTML = this.session.suspects.map(s => `
      <div class="suspect-card ${s.is_viable ? 'viable' : 'cleared'}" data-id="${s.id}">
        <div class="suspect-card-img-wrap">
          <img src="${s.image}" alt="${s.name}" class="suspect-card-img" onerror="this.src='assets/img/suspects/placeholder.svg'">
          ${s.is_eliminated ? '<div class="stamp-cleared">CLEARED</div>' : ''}
        </div>
        <div class="suspect-card-info">
          <div class="suspect-card-name">${s.name} [${s.id}]</div>
          <div class="suspect-card-role">${s.role}</div>
          <div class="suspect-card-traits">${(s.traits || []).join(' • ')}</div>
        </div>
      </div>
    `).join('');

    grid.querySelectorAll('.suspect-card').forEach(card => {
      card.addEventListener('click', () => {
        this.openDossier(card.dataset.id);
      });
    });
  }

  renderConnectionsTab() {
    if (this.corkboard && this.session.suspects) {
      this.corkboard.setData(this.session.suspects, this.session.connections);
    }
  }

  async renderLeadsTab() {
    if (!this.treeUI || !this.session.tree) return;
    const hoodData = await this.api('/api/dsa/stats?tab=leads');
    const preOrder = (hoodData && hoodData.data && hoodData.data.pre_order_ids) || [];
    const lvlOrder = (hoodData && hoodData.data && hoodData.data.level_order_ids) || [];
    this.treeUI.setTree(this.session.tree, preOrder.map(id => ({ id })), lvlOrder.map(id => ({ id })));
  }

  renderEvidenceTab() {
    const grid = document.getElementById('cluesGrid');
    const badge = document.getElementById('activeCluesBadge');
    const stepsLog = document.getElementById('setStepsLog');
    if (!grid || !this.session.discovered_clues) return;

    const clues = this.session.discovered_clues;
    if (badge) badge.textContent = `${clues.length} Discovered Clues`;

    if (stepsLog && this.session.set_steps) {
      stepsLog.innerHTML = this.session.set_steps.map(s => `<div>${s}</div>`).join('');
    }

    if (clues.length === 0) {
      grid.innerHTML = '<div style="color: var(--text-muted); font-size: 13px;">No evidence collected yet. Pursue leads in the Leads tab.</div>';
      return;
    }

    grid.innerHTML = clues.map(c => `
      <div class="clue-card ${c.debunked ? 'debunked' : ''} ${c.is_forged ? 'forged' : ''}">
        <img src="${c.image}" alt="${c.title}" class="clue-thumb" onerror="this.src='assets/img/evidence/keypad.svg'">
        <div class="clue-title">[${c.id}] ${c.title}</div>
        <div class="clue-desc">${c.desc}</div>
        <div class="clue-chips-wrap">
          <span style="font-family: monospace; font-size: 10px; color: var(--text-muted);">Points to:</span>
          ${(c.allowed || []).map(id => `<span class="clue-chip">${id}</span>`).join('')}
          ${c.debunked ? '<span class="clue-chip" style="color: var(--red-bright); border-color: var(--red-bright);">DEBUNKED FORGERY</span>' : ''}
        </div>
      </div>
    `).join('');
  }

  renderAlibiTab() {
    const tbody = document.getElementById('logsTableBody');
    const select = document.getElementById('selectAlibiSuspect');
    if (!tbody || !this.session.security_logs) return;

    if (select && select.children.length === 0 && this.session.suspects) {
      select.innerHTML = this.session.suspects.map(s => `
        <option value="${s.id}">[${s.id}] ${s.name}</option>
      `).join('');
    }

    tbody.innerHTML = this.session.security_logs.map((log, idx) => `
      <tr data-index="${idx}">
        <td>#${idx}</td>
        <td class="pointer-cell" style="font-weight: bold; color: var(--red-bright); font-family: monospace;"></td>
        <td><strong>${log.time}</strong></td>
        <td>${log.suspect_id}</td>
        <td>${log.event}</td>
        <td>${log.location}</td>
      </tr>
    `).join('');
  }

  renderAccuseTab() {
    const culpritGrid = document.getElementById('culpritSelectionGrid');
    const accompliceGrid = document.getElementById('accompliceSelectionGrid');
    if (!culpritGrid || !accompliceGrid || !this.session.suspects) return;

    const renderGrid = (container, isAccomplice) => {
      container.innerHTML = this.session.suspects.map(s => {
        const isSelected = isAccomplice ? this.selectedAccomplice === s.id : this.selectedCulprit === s.id;
        return `
          <div class="selectable-suspect ${isSelected ? 'selected' : ''}" data-id="${s.id}" data-type="${isAccomplice ? 'accomplice' : 'culprit'}">
            <img src="${s.image}" alt="${s.name}" class="select-thumb" onerror="this.src='assets/img/suspects/placeholder.svg'">
            <span class="select-name">${s.name.split(' ')[0]}</span>
          </div>
        `;
      }).join('');

      container.querySelectorAll('.selectable-suspect').forEach(card => {
        card.addEventListener('click', () => {
          const id = card.dataset.id;
          if (isAccomplice) {
            this.selectedAccomplice = this.selectedAccomplice === id ? null : id;
          } else {
            this.selectedCulprit = this.selectedCulprit === id ? null : id;
          }
          this.renderAccuseTab();
        });
      });
    };

    renderGrid(culpritGrid, false);
    renderGrid(accompliceGrid, true);
  }

  showSirenOverlay() {
    const overlay = document.getElementById('sirenOverlay');
    const row = document.getElementById('sirenCardsRow');
    if (!overlay || !row) return;

    overlay.classList.remove('hidden');
    const conflictIds = this.session.conflicting_clues || [];
    const conflictClues = conflictIds.map(id => this.session.discovered_clues.find(c => c.id === id)).filter(Boolean);

    row.innerHTML = conflictClues.map(c => `
      <div class="siren-clue-card">
        <h4>[${c.id}] ${c.title}</h4>
        <p>${c.desc}</p>
        <div style="font-family: monospace; font-size: 11px; color: var(--text-muted); margin-top: 4px;">
          Permitted: {${(c.allowed || []).join(', ')}}
        </div>
        <button class="btn-expose-lie" data-clue-id="${c.id}">EXPOSE AS FORGERY</button>
      </div>
    `).join('');

    row.querySelectorAll('.btn-expose-lie').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const clueId = e.currentTarget.dataset.clueId;
        const res = await this.api('/api/clue/debunk', 'POST', { clue_id: clueId });
        if (res) {
          alert(res.message);
          this.session = res.session;
          this.render();
        }
      });
    });
  }

  async exploreLead(leadId) {
    const res = await this.api('/api/lead/explore', 'POST', { lead_id: leadId });
    if (!res) return;
    if (!res.success) {
      alert(res.message);
      return;
    }
    this.session = res.session;
    this.render();
  }

  async queryPath(u, v) {
    const res = await this.api('/api/graph/path', 'POST', { start: u, target: v });
    if (!res || !res.success) {
      alert(res ? res.message : 'Path query failed');
      return;
    }

    this.session.ap = res.remaining_ap;
    this.renderAP(this.session.ap, this.session.max_ap);

    if (this.corkboard) {
      this.corkboard.setPath(res.path);
    }

    const banner = document.getElementById('bfsPathBanner');
    if (banner) {
      banner.classList.remove('hidden');
      banner.innerHTML = `
        <div><strong>BFS COLLUSION PATH (${res.path.length} NODES):</strong> ${res.path.join(' ➔ ')}</div>
        <div style="color: var(--text-muted);">1 AP Deducted (Steps: ${res.steps})</div>
      `;
    }
  }

  async runBinarySearch(stepMode = false) {
    const suspectId = document.getElementById('selectAlibiSuspect').value;
    const timeTarget = document.getElementById('inputAlibiTime').value.trim() || '23:45';

    const res = await this.api('/api/alibi/check', 'POST', { suspect_id: suspectId, time: timeTarget });
    if (!res || !res.success) {
      alert(res ? res.message : 'Alibi check failed');
      return;
    }

    this.session.ap = res.remaining_ap;
    this.renderAP(this.session.ap, this.session.max_ap);

    if (this.binSearchAnimator) {
      this.binSearchAnimator.setTrace(res.trace, res.summary);
      if (!stepMode) {
        this.binSearchAnimator.autoPlay();
      }
    }
  }

  openDossier(suspectId) {
    const s = (this.session.suspects || []).find(sub => sub.id === suspectId);
    if (!s) return;

    document.getElementById('dossierIdBadge').textContent = s.id;
    document.getElementById('dossierName').textContent = s.name;
    document.getElementById('dossierImg').src = s.image;
    document.getElementById('dossierRole').textContent = s.role;
    document.getElementById('dossierTraits').textContent = (s.traits || []).join(' • ');
    document.getElementById('dossierAlibi').textContent = s.alibi;
    document.getElementById('dossierMotive').textContent = s.motive;
    document.getElementById('dossierNotes').textContent = s.notes;

    const btnElim = document.getElementById('btnToggleEliminateDossier');
    btnElim.textContent = s.is_eliminated ? 'Restore Suspect' : 'Cross Off Suspect';
    btnElim.onclick = async () => {
      const res = await this.api('/api/suspect/toggle', 'POST', { suspect_id: s.id });
      if (res) {
        this.session = res;
        this.render();
        this.openDossier(s.id);
      }
    };

    document.getElementById('dossierModal').classList.remove('hidden');
  }

  async openUnderTheHood(tabName) {
    const hood = await this.api(`/api/dsa/stats?tab=${tabName}`);
    if (!hood) return;

    document.getElementById('hoodDsName').textContent = hood.name;
    document.getElementById('hoodExplanation').textContent = hood.explanation;
    document.getElementById('hoodComplexityBadge').textContent = hood.complexity;

    const visual = document.getElementById('hoodLiveVisual');
    if (hood.visual_type === 'hashmap') {
      const buckets = hood.data.buckets || [];
      visual.innerHTML = `
        <div style="font-family: monospace; font-size: 11px; margin-bottom: 4px;">
          Capacity: ${hood.data.capacity} | Items: ${hood.data.size} | α: ${hood.data.load_factor} | Collisions: ${hood.data.collisions}
        </div>
        <div style="display: flex; gap: 4px; flex-wrap: wrap;">
          ${buckets.map((len, idx) => `
            <div style="width: 20px; height: 28px; background: ${len > 0 ? 'var(--red-dark)' : '#1a1a1a'}; border: 1px solid ${idx === hood.data.last_accessed ? 'var(--red-bright)' : '#333'}; display: flex; align-items: center; justify-content: center; font-size: 10px; font-family: monospace; color: #fff;">
              ${len}
            </div>
          `).join('')}
        </div>
      `;
    } else if (hood.visual_type === 'graph') {
      visual.innerHTML = `
        <div style="font-family: monospace; font-size: 11px;">
          Active Vertex: [${hood.data.selected_node}] | Degree: ${hood.data.neighbor_count} | Syndicates: ${hood.data.syndicate_count}
        </div>
        <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">
          Neighbors: ${(hood.data.neighbors || []).join(', ') || 'None'}
        </div>
      `;
    } else if (hood.visual_type === 'sets') {
      visual.innerHTML = `
        <div style="font-family: monospace; font-size: 11px;">
          Universe |U|: ${hood.data.universe_count} | Eliminated |E|: ${hood.data.eliminated_count} | Viable: ${hood.data.viable_count}
        </div>
      `;
    } else if (hood.visual_type === 'tree') {
      visual.innerHTML = `
        <div style="font-family: monospace; font-size: 11px;">
          DFS Deep Dive: ${(hood.data.pre_order_ids || []).slice(0, 6).join(' ➔ ')}...
        </div>
        <div style="font-family: monospace; font-size: 11px; margin-top: 4px;">
          BFS Broad Survey: ${(hood.data.level_order_ids || []).slice(0, 6).join(' ➔ ')}...
        </div>
      `;
    } else if (hood.visual_type === 'search') {
      visual.innerHTML = `
        <div style="font-family: monospace; font-size: 11px;">
          Binary Search Iterations: ${hood.data.iterations} (O(log N))
        </div>
      `;
    } else {
      visual.innerHTML = '';
    }

    document.getElementById('hoodDrawer').classList.remove('hidden');
  }

  async submitAccusation() {
    if (!this.selectedCulprit) {
      alert('You must select a prime culprit before issuing a warrant.');
      return;
    }

    const verdict = await this.api('/api/accuse', 'POST', {
      culprit: this.selectedCulprit,
      accomplice: this.selectedAccomplice || ''
    });

    if (!verdict) return;
    this.showVerdict(verdict);
  }

  showVerdict(v) {
    const stamp = document.getElementById('verdictStamp');
    const headline = document.getElementById('verdictTitle');
    const narrative = document.getElementById('verdictNarrative');

    if (v.is_solved) {
      stamp.textContent = 'CONVICTION SECURED';
      stamp.style.borderColor = 'var(--red-bright)';
      stamp.style.color = 'var(--red-bright)';
      headline.textContent = 'CASE CLOSED: INDICTMENT SUCCESSFUL';
      narrative.textContent = `The prime suspect [${v.actual_culprit}] was apprehended with conclusive forensic evidence.`;
    } else {
      stamp.textContent = 'INDICTMENT FAILED';
      stamp.style.borderColor = '#8a8a8a';
      stamp.style.color = '#8a8a8a';
      headline.textContent = 'CASE COLLAPSED: WRONG SUSPECT';
      narrative.textContent = `False arrest! The real criminal was [${v.actual_culprit}].`;
    }

    document.getElementById('vCulpritScore').textContent = `${v.is_culprit_correct ? 500 : 0} Pts`;
    document.getElementById('vAccompliceScore').textContent = `${v.is_accomplice_correct ? 250 : 0} Pts`;
    document.getElementById('vDebunkScore').textContent = `${v.is_contradiction_debunked ? 250 : 0} Pts`;
    document.getElementById('vApScore').textContent = `${v.ap_bonus} Pts`;
    document.getElementById('vTotalScore').textContent = `${v.score} Pts`;
    document.getElementById('vRankTitle').textContent = v.rank;

    document.getElementById('verdictOverlay').classList.remove('hidden');
  }

  bindEvents() {
    // Tab Switching
    document.querySelectorAll('.nav-tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const tab = e.currentTarget.dataset.tab;
        this.activeTab = tab;

        document.querySelectorAll('.nav-tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

        e.currentTarget.classList.add('active');
        const pane = document.getElementById(`tab-${tab}`);
        if (pane) pane.classList.add('active');

        if (tab === 'connections' && this.corkboard) {
          this.corkboard.initCanvasSize();
        }
      });
    });

    // Under the Hood drawer buttons
    document.querySelectorAll('.btn-hood').forEach(btn => {
      btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        this.openUnderTheHood(tab);
      });
    });

    document.getElementById('btnCloseHood').addEventListener('click', () => {
      document.getElementById('hoodDrawer').classList.add('hidden');
    });

    // Top buttons
    document.getElementById('btnReturnToCases').addEventListener('click', () => {
      document.getElementById('gameScreen').classList.add('hidden');
      document.getElementById('titleScreen').classList.remove('hidden');
    });

    document.getElementById('btnOpenHelp').addEventListener('click', () => {
      document.getElementById('onboardingOverlay').classList.remove('hidden');
    });

    document.getElementById('btnIssueWarrant').addEventListener('click', () => {
      // Switch to accuse tab
      const accuseBtn = document.querySelector('.nav-tab-btn[data-tab="accuse"]');
      if (accuseBtn) accuseBtn.click();
    });

    // Onboarding buttons
    const closeOnboarding = () => {
      document.getElementById('onboardingOverlay').classList.add('hidden');
      localStorage.setItem('casezero_onboarding_done', '1');
    };
    document.getElementById('btnSkipOnboarding').addEventListener('click', closeOnboarding);
    document.getElementById('btnDismissOnboarding').addEventListener('click', closeOnboarding);
    document.getElementById('btnCloseOnboarding').addEventListener('click', closeOnboarding);

    // Corkboard Tools
    document.getElementById('btnToggleSyndicates').addEventListener('click', () => {
      if (this.corkboard) this.corkboard.toggleSyndicates();
    });

    document.getElementById('btnResetCorkboard').addEventListener('click', () => {
      if (this.corkboard) this.corkboard.resetPositions();
    });

    // Tree Mode Toggle
    document.getElementById('btnDeepDive').addEventListener('click', (e) => {
      document.getElementById('btnBroadSurvey').classList.remove('active');
      e.currentTarget.classList.add('active');
      if (this.treeUI) this.treeUI.setMode('pre_order');
    });

    document.getElementById('btnBroadSurvey').addEventListener('click', (e) => {
      document.getElementById('btnDeepDive').classList.remove('active');
      e.currentTarget.classList.add('active');
      if (this.treeUI) this.treeUI.setMode('level_order');
    });

    // Alibi Buttons
    document.getElementById('btnStepBinarySearch').addEventListener('click', () => {
      this.runBinarySearch(true);
    });

    document.getElementById('btnAutoBinarySearch').addEventListener('click', () => {
      this.runBinarySearch(false);
    });

    // Accusation Button
    document.getElementById('btnExecuteAccusal').addEventListener('click', () => {
      this.submitAccusation();
    });

    // Verdict Buttons
    document.getElementById('btnReplayCase').addEventListener('click', () => {
      document.getElementById('verdictOverlay').classList.add('hidden');
      this.startCase(this.session.case_id);
    });

    document.getElementById('btnNextCase').addEventListener('click', () => {
      document.getElementById('verdictOverlay').classList.add('hidden');
      const nextId = this.session.case_id === 'case_1' ? 'case_2' : 'procedural';
      this.startCase(nextId);
    });

    // Dossier Modal Close
    document.getElementById('btnCloseDossier').addEventListener('click', () => {
      document.getElementById('dossierModal').classList.add('hidden');
    });

    // Trie Search Bar
    const searchInput = document.getElementById('trieSearchInput');
    const suggestionsBox = document.getElementById('trieSuggestions');

    searchInput.addEventListener('input', async (e) => {
      const q = e.target.value.trim();
      if (!q) {
        suggestionsBox.classList.add('hidden');
        return;
      }

      const res = await this.api('/api/search', 'POST', { query: q });
      if (res && res.matches && res.matches.length > 0) {
        suggestionsBox.classList.remove('hidden');
        suggestionsBox.innerHTML = res.matches.map(m => `
          <div class="trie-item" data-word="${m.word}">
            <span>${m.word}</span>
            <small style="color: var(--text-muted);">${m.record.type}: [${m.record.id}]</small>
          </div>
        `).join('');

        suggestionsBox.querySelectorAll('.trie-item').forEach(item => {
          item.addEventListener('click', () => {
            searchInput.value = item.dataset.word;
            suggestionsBox.classList.add('hidden');
          });
        });
      } else {
        suggestionsBox.classList.add('hidden');
      }
    });
  }
}

window.addEventListener('DOMContentLoaded', () => {
  new CaseZeroApp();
});
