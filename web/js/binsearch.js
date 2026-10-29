/**
 * CaseZero - Binary Search Timeline Animator
 * Animates Low, Mid, and High pointers over sorted security access logs.
 */

class BinarySearchAnimator {
  constructor(tableBodyEl, traceBoxEl) {
    this.tableBody = tableBodyEl;
    this.traceBox = traceBoxEl;
    this.steps = [];
    this.currentStepIdx = 0;
    this.timer = null;
  }

  setTrace(traceData, summaryText = '') {
    this.stopAutoPlay();
    this.steps = traceData.steps || [];
    this.currentStepIdx = 0;
    this.summaryText = summaryText;
    this.traceData = traceData;

    this.traceBox.classList.remove('hidden');
    this.renderCurrentStep();
  }

  stepForward() {
    if (this.currentStepIdx < this.steps.length - 1) {
      this.currentStepIdx++;
      this.renderCurrentStep();
      return true;
    }
    return false;
  }

  autoPlay(onComplete) {
    this.stopAutoPlay();
    this.currentStepIdx = 0;
    this.renderCurrentStep();

    this.timer = setInterval(() => {
      const advanced = this.stepForward();
      if (!advanced) {
        this.stopAutoPlay();
        if (onComplete) onComplete();
      }
    }, 700);
  }

  stopAutoPlay() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  renderCurrentStep() {
    if (!this.steps || this.steps.length === 0) return;
    const step = this.steps[this.currentStepIdx];

    // Update Status Box
    const isLast = this.currentStepIdx === this.steps.length - 1;
    this.traceBox.innerHTML = `
      <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
        <span style="color: var(--red-bright); font-weight: bold;">BINARY SEARCH: STEP ${step.step} OF ${this.steps.length}</span>
        <span style="color: var(--text-muted);">POINTERS: [LOW: ${step.low}, MID: ${step.mid}, HIGH: ${step.high}]</span>
      </div>
      <div style="margin-bottom: 4px;">
        Checking Timestamp: <strong>${step.mid_time}</strong> (Target: ${step.target_time}) ➔ ${step.comparison}
      </div>
      ${isLast ? `<div style="color: #fff; font-weight: bold; margin-top: 6px; border-top: 1px solid var(--border-mid); padding-top: 6px;">${this.summaryText}</div>` : ''}
    `;

    // Highlight table rows
    const rows = this.tableBody.querySelectorAll('tr');
    rows.forEach((row, idx) => {
      row.classList.remove('mid-highlight', 'low-pointer', 'high-pointer');
      const pointerCell = row.querySelector('.pointer-cell');
      if (pointerCell) pointerCell.textContent = '';

      if (idx === step.mid) {
        row.classList.add('mid-highlight');
        if (pointerCell) pointerCell.textContent = '➔ MID';
      } else if (idx === step.low && idx === step.high) {
        if (pointerCell) pointerCell.textContent = 'L & H';
      } else if (idx === step.low) {
        row.classList.add('low-pointer');
        if (pointerCell) pointerCell.textContent = 'LOW';
      } else if (idx === step.high) {
        row.classList.add('high-pointer');
        if (pointerCell) pointerCell.textContent = 'HIGH';
      }
    });
  }
}

window.BinarySearchAnimator = BinarySearchAnimator;
