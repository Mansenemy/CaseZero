/**
 * CaseZero - Corkboard Graph Visualizer (Vanilla JS Canvas)
 * Draggable suspect pins, red detective yarn lines, BFS path highlighting,
 * and connected-component grouping.
 */

class CorkboardGraph {
  constructor(canvasEl, options = {}) {
    this.canvas = canvasEl;
    this.ctx = canvasEl.getContext('2d');
    this.options = options;

    this.nodes = new Map(); // id -> { id, name, role, x, y, vx, vy, radius: 28, isPinned: false, img: HTMLImageElement }
    this.edges = []; // [ { u, v, type, desc } ]
    this.selectedNodes = []; // up to 2 nodes
    this.highlightedPath = []; // list of node IDs in BFS path
    this.syndicates = []; // list of lists
    this.showSyndicates = false;
    this.draggedNode = null;

    this.initCanvasSize();
    this.bindEvents();
    this.startLoop();
  }

  initCanvasSize() {
    const rect = this.canvas.parentElement.getBoundingClientRect();
    this.canvas.width = rect.width || 800;
    this.canvas.height = rect.height || 540;
  }

  setData(suspects, connections, syndicates = []) {
    this.edges = connections || [];
    this.syndicates = syndicates || [];

    const cx = this.canvas.width / 2;
    const cy = this.canvas.height / 2;
    const r = Math.min(cx, cy) * 0.7;

    suspects.forEach((s, idx) => {
      let node = this.nodes.get(s.id);
      if (!node) {
        const angle = (idx / suspects.length) * 2 * Math.PI - Math.PI / 2;
        const img = new Image();
        img.src = s.image || 'assets/img/suspects/placeholder.svg';
        img.onerror = () => { img.src = 'assets/img/suspects/placeholder.svg'; };

        node = {
          id: s.id,
          name: s.name,
          role: s.role,
          isViable: s.is_viable,
          isEliminated: s.is_eliminated,
          x: cx + r * Math.cos(angle),
          y: cy + r * Math.sin(angle),
          vx: 0,
          vy: 0,
          radius: 28,
          isPinned: false,
          img
        };
        this.nodes.set(s.id, node);
      } else {
        node.name = s.name;
        node.role = s.role;
        node.isViable = s.is_viable;
        node.isEliminated = s.is_eliminated;
      }
    });
  }

  bindEvents() {
    const getPos = (e) => {
      const rect = this.canvas.getBoundingClientRect();
      return {
        x: (e.clientX - rect.left) * (this.canvas.width / rect.width),
        y: (e.clientY - rect.top) * (this.canvas.height / rect.height)
      };
    };

    this.canvas.addEventListener('mousedown', (e) => {
      const pos = getPos(e);
      let clickedId = null;

      for (const [id, node] of this.nodes.entries()) {
        const d = Math.hypot(node.x - pos.x, node.y - pos.y);
        if (d <= node.radius + 4) {
          clickedId = id;
          this.draggedNode = id;
          node.isPinned = true;
          break;
        }
      }

      if (clickedId) {
        this.handleNodeClick(clickedId);
      } else {
        // Clicked background -> clear selection
        this.selectedNodes = [];
        this.highlightedPath = [];
        if (this.options.onPathCleared) this.options.onPathCleared();
      }
    });

    window.addEventListener('mousemove', (e) => {
      if (this.draggedNode) {
        const pos = getPos(e);
        const node = this.nodes.get(this.draggedNode);
        if (node) {
          node.x = Math.max(40, Math.min(this.canvas.width - 40, pos.x));
          node.y = Math.max(40, Math.min(this.canvas.height - 40, pos.y));
        }
      }
    });

    window.addEventListener('mouseup', () => {
      if (this.draggedNode) {
        const node = this.nodes.get(this.draggedNode);
        if (node) node.isPinned = false;
        this.draggedNode = null;
      }
    });

    window.addEventListener('resize', () => {
      this.initCanvasSize();
    });
  }

  handleNodeClick(id) {
    if (this.selectedNodes.includes(id)) {
      this.selectedNodes = this.selectedNodes.filter(n => n !== id);
    } else {
      if (this.selectedNodes.length >= 2) {
        this.selectedNodes = [id];
      } else {
        this.selectedNodes.push(id);
      }
    }

    if (this.selectedNodes.length === 2 && this.options.onRequestPath) {
      this.options.onRequestPath(this.selectedNodes[0], this.selectedNodes[1]);
    } else if (this.options.onSelectSuspect) {
      this.options.onSelectSuspect(id);
    }
  }

  setPath(path) {
    this.highlightedPath = path || [];
  }

  toggleSyndicates() {
    this.showSyndicates = !this.showSyndicates;
  }

  resetPositions() {
    const cx = this.canvas.width / 2;
    const cy = this.canvas.height / 2;
    const r = Math.min(cx, cy) * 0.7;
    const list = Array.from(this.nodes.values());
    list.forEach((node, idx) => {
      const angle = (idx / list.length) * 2 * Math.PI - Math.PI / 2;
      node.x = cx + r * Math.cos(angle);
      node.y = cy + r * Math.sin(angle);
      node.vx = 0;
      node.vy = 0;
    });
    this.selectedNodes = [];
    this.highlightedPath = [];
  }

  startLoop() {
    const loop = () => {
      this.updatePhysics();
      this.draw();
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  updatePhysics() {
    // Gentle repulsion force to prevent node overlap
    const nodes = Array.from(this.nodes.values());
    const k = 800;
    const damp = 0.85;

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const n1 = nodes[i];
        const n2 = nodes[j];
        const dx = n2.x - n1.x;
        const dy = n2.y - n1.y;
        const dist = Math.hypot(dx, dy) || 1;

        if (dist < 140) {
          const force = k / (dist * dist);
          const fx = (dx / dist) * force;
          const fy = (dy / dist) * force;
          if (!n1.isPinned) { n1.vx -= fx; n1.vy -= fy; }
          if (!n2.isPinned) { n2.vx += fx; n2.vy += fy; }
        }
      }
    }

    nodes.forEach(n => {
      if (!n.isPinned && this.draggedNode !== n.id) {
        n.x += n.vx;
        n.y += n.vy;
        n.vx *= damp;
        n.vy *= damp;
        n.x = Math.max(40, Math.min(this.canvas.width - 40, n.x));
        n.y = Math.max(40, Math.min(this.canvas.height - 40, n.y));
      }
    });
  }

  draw() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Subtle dark corkboard texture lines
    this.ctx.strokeStyle = '#141414';
    this.ctx.lineWidth = 1;
    for (let x = 0; x < this.canvas.width; x += 32) {
      this.ctx.beginPath();
      this.ctx.moveTo(x, 0);
      this.ctx.lineTo(x, this.canvas.height);
      this.ctx.stroke();
    }
    for (let y = 0; y < this.canvas.height; y += 32) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, y);
      this.ctx.lineTo(this.canvas.width, y);
      this.ctx.stroke();
    }

    // Draw Syndicates (Dashed Bounding Clusters)
    if (this.showSyndicates && this.syndicates.length > 0) {
      this.syndicates.forEach((comp, idx) => {
        if (comp.length <= 1) return;
        const pts = comp.map(id => this.nodes.get(id)).filter(Boolean);
        if (pts.length < 2) return;

        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        pts.forEach(p => {
          minX = Math.min(minX, p.x);
          minY = Math.min(minY, p.y);
          maxX = Math.max(maxX, p.x);
          maxY = Math.max(maxY, p.y);
        });

        this.ctx.save();
        this.ctx.strokeStyle = '#5c0a10';
        this.ctx.lineWidth = 1.5;
        this.ctx.setLineDash([6, 6]);
        this.ctx.strokeRect(minX - 36, minY - 36, (maxX - minX) + 72, (maxY - minY) + 72);
        this.ctx.fillStyle = '#5c0a10';
        this.ctx.font = '10px monospace';
        this.ctx.fillText(`SYNDICATE #${idx + 1}`, minX - 30, minY - 42);
        this.ctx.restore();
      });
    }

    // Draw Edges (Red Yarn)
    this.edges.forEach(e => {
      const u = this.nodes.get(e.u);
      const v = this.nodes.get(e.v);
      if (!u || !v) return;

      const isPathEdge = this.isEdgeInPath(e.u, e.v);
      const isSelectedEdge = this.selectedNodes.includes(e.u) && this.selectedNodes.includes(e.v);
      const isConnectedToActive = this.selectedNodes.length === 1 && (this.selectedNodes[0] === e.u || this.selectedNodes[0] === e.v);

      this.ctx.save();
      this.ctx.beginPath();
      this.ctx.moveTo(u.x, u.y);

      // Subtle curved detective string
      const midX = (u.x + v.x) / 2;
      const midY = (u.y + v.y) / 2 + 10;
      this.ctx.quadraticCurveTo(midX, midY, v.x, v.y);

      if (isPathEdge) {
        this.ctx.strokeStyle = '#e11d2a';
        this.ctx.lineWidth = 4;
        this.ctx.shadowColor = '#e11d2a';
        this.ctx.shadowBlur = 12;
      } else if (isSelectedEdge || isConnectedToActive) {
        this.ctx.strokeStyle = '#e11d2a';
        this.ctx.lineWidth = 2.5;
      } else {
        this.ctx.strokeStyle = '#5c0a10';
        this.ctx.lineWidth = 1.5;
        if (e.type === 'CONSPIRACY') {
          this.ctx.setLineDash([5, 5]);
        } else if (e.type === 'DEBT' || e.type === 'BLACKMAIL') {
          this.ctx.setLineDash([2, 4]);
        }
      }

      this.ctx.stroke();
      this.ctx.restore();
    });

    // Draw Suspect Nodes (Pins & Portraits)
    this.nodes.forEach(node => {
      const isSelected = this.selectedNodes.includes(node.id);
      const isPathNode = this.highlightedPath.includes(node.id);

      this.ctx.save();
      this.ctx.translate(node.x, node.y);

      // Node shadow
      if (isSelected || isPathNode) {
        this.ctx.shadowColor = '#e11d2a';
        this.ctx.shadowBlur = 16;
      }

      // Circular clipped portrait
      this.ctx.beginPath();
      this.ctx.arc(0, 0, node.radius, 0, Math.PI * 2);
      this.ctx.fillStyle = '#141414';
      this.ctx.fill();

      this.ctx.save();
      this.ctx.clip();
      if (node.img && node.img.complete && node.img.naturalWidth > 0) {
        this.ctx.drawImage(node.img, -node.radius, -node.radius, node.radius * 2, node.radius * 2);
      } else {
        this.ctx.fillStyle = '#262626';
        this.ctx.fillRect(-node.radius, -node.radius, node.radius * 2, node.radius * 2);
      }
      this.ctx.restore();

      // Border ring
      this.ctx.beginPath();
      this.ctx.arc(0, 0, node.radius, 0, Math.PI * 2);
      this.ctx.lineWidth = isSelected || isPathNode ? 3 : 1.5;
      this.ctx.strokeStyle = isSelected || isPathNode ? '#e11d2a' : (node.isEliminated ? '#333333' : '#5c0a10');
      this.ctx.stroke();

      // Pushpin top bead (Crimson red)
      this.ctx.beginPath();
      this.ctx.arc(0, -node.radius + 1, 4, 0, Math.PI * 2);
      this.ctx.fillStyle = '#e11d2a';
      this.ctx.fill();

      // Cleared overlay
      if (node.isEliminated) {
        this.ctx.fillStyle = 'rgba(10, 10, 10, 0.6)';
        this.ctx.beginPath();
        this.ctx.arc(0, 0, node.radius, 0, Math.PI * 2);
        this.ctx.fill();
      }

      // Label
      this.ctx.shadowBlur = 0;
      this.ctx.font = 'bold 11px system-ui, sans-serif';
      this.ctx.fillStyle = isSelected ? '#ffffff' : (node.isEliminated ? '#666666' : '#e8e6e3');
      this.ctx.textAlign = 'center';
      this.ctx.fillText(node.name.split(' ')[0], 0, node.radius + 14);

      this.ctx.font = '9px monospace';
      this.ctx.fillStyle = '#8a8a8a';
      this.ctx.fillText(`[${node.id}]`, 0, node.radius + 26);

      this.ctx.restore();
    });
  }

  isEdgeInPath(u, v) {
    if (!this.highlightedPath || this.highlightedPath.length < 2) return false;
    for (let i = 0; i < this.highlightedPath.length - 1; i++) {
      const a = this.highlightedPath[i];
      const b = this.highlightedPath[i + 1];
      if ((a === u && b === v) || (a === v && b === u)) return true;
    }
    return false;
  }
}

window.CorkboardGraph = CorkboardGraph;
