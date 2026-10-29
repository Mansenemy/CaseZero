/**
 * CaseZero - Investigation Decision Tree Visualizer
 * Renders hierarchical decision tree leads with traversal ordering and unlock statuses.
 */

class InvestigationTreeUI {
  constructor(containerEl, options = {}) {
    this.container = containerEl;
    this.options = options;
    this.mode = 'pre_order'; // 'pre_order' (Deep Dive) or 'level_order' (Broad Survey)
    this.treeData = null;
    this.preOrderMap = new Map();
    this.levelOrderMap = new Map();
  }

  setTree(treeRoot, preOrderList = [], levelOrderList = []) {
    this.treeData = treeRoot;
    this.preOrderMap.clear();
    this.levelOrderMap.clear();

    preOrderList.forEach((n, idx) => {
      this.preOrderMap.set(n.id, idx + 1);
    });

    levelOrderList.forEach((n, idx) => {
      this.levelOrderMap.set(n.id, idx + 1);
    });

    this.render();
  }

  setMode(newMode) {
    this.mode = newMode;
    this.render();
  }

  render() {
    if (!this.container || !this.treeData) return;
    this.container.innerHTML = '';

    const rootWrapper = document.createElement('div');
    rootWrapper.className = 'tree-hierarchy-wrapper';
    this.renderNode(this.treeData, rootWrapper);
    this.container.appendChild(rootWrapper);
  }

  renderNode(node, parentEl) {
    const card = document.createElement('div');
    const statusClass = (node.status || 'locked').toLowerCase();
    card.className = `tree-node-card ${statusClass}`;
    card.dataset.leadId = node.id;

    const seqNum = this.mode === 'pre_order' ? this.preOrderMap.get(node.id) : this.levelOrderMap.get(node.id);
    const seqBadge = seqNum ? `<span class="seq-badge">#${seqNum}</span>` : '';

    card.innerHTML = `
      <div class="node-header">
        <span class="node-category">${node.category}</span>
        ${seqBadge}
        <span class="node-status">${node.status}</span>
      </div>
      <div class="node-title">${node.title}</div>
      <div class="node-desc">${node.description || ''}</div>
      <div class="node-footer">
        <span class="node-cost">⚡ Cost: ${node.ap_cost} AP</span>
        ${node.clues && node.clues.length > 0 ? `<span class="node-clue-tag">Clue: ${node.clues.join(', ')}</span>` : ''}
      </div>
    `;

    if (node.status === 'AVAILABLE') {
      card.addEventListener('click', () => {
        if (this.options.onExplore) {
          this.options.onExplore(node.id);
        }
      });
    }

    const branchWrap = document.createElement('div');
    branchWrap.className = 'tree-branch-group';
    branchWrap.appendChild(card);

    if (node.children && node.children.length > 0) {
      const childWrap = document.createElement('div');
      childWrap.className = 'tree-children-row';
      node.children.forEach(child => {
        this.renderNode(child, childWrap);
      });
      branchWrap.appendChild(childWrap);
    }

    parentEl.appendChild(branchWrap);
  }
}

window.InvestigationTreeUI = InvestigationTreeUI;
