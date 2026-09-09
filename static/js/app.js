(() => {
  const el = (selector) => document.querySelector(selector);
  const fmtTime = (iso) => new Date(iso).toLocaleTimeString([], { hour12: false });

  const renderAlertRows = (alerts) => alerts.map((a) => `
    <tr class="row-enter">
      <td><span class="severity ${a.severity.toLowerCase()}">${a.severity}</span></td>
      <td><strong>${a.rule}</strong></td>
      <td><code>${a.source}</code></td>
      <td>${a.user}</td>
      <td>${a.message}</td>
      <td class="muted mono">${fmtTime(a.timestamp)}</td>
    </tr>`).join('');

  const renderEventRows = (events) => events.slice(0, 12).map((e) => `
    <tr class="row-enter">
      <td class="muted mono">${fmtTime(e.timestamp)}</td>
      <td><code>${e.source}</code></td>
      <td>${e.user}</td>
      <td><span class="action ${e.action.toLowerCase()}">${e.action}</span></td>
    </tr>`).join('');

  const drawTimeline = (timeline) => {
    const chart = el('#timeline');
    if (!chart || !timeline.length) return;
    const max = Math.max(...timeline.map((p) => p.count), 1);
    chart.innerHTML = timeline.map((p) => `
      <div class="bar-col" title="${p.label}: ${p.count} events / ${p.failures} failures">
        <div class="bar-value">${p.count}</div>
        <div class="bar-fill" style="height:${Math.max(6, (p.count / max) * 118)}px"></div>
        <span>${p.label}</span>
      </div>`).join('');
  };

  const refresh = async () => {
    const response = await fetch('/api/snapshot', { cache: 'no-store' });
    if (!response.ok) throw new Error('snapshot failed');
    const data = await response.json();

    [['total-events', data.total_events], ['alert-count', data.alert_count], ['critical-count', data.critical], ['failure-count', data.failures], ['source-count', data.unique_sources]].forEach(([id, value]) => {
      const node = el(`#${id}`);
      if (node) node.textContent = value;
    });

    const alertBody = el('#alert-rows');
    if (alertBody) alertBody.innerHTML = renderAlertRows(data.alerts);
    const eventBody = el('#event-rows');
    if (eventBody) eventBody.innerHTML = renderEventRows(data.events);

    const sourceList = el('#source-list');
    if (sourceList) sourceList.innerHTML = data.top_sources.map(([source, count]) => `<div class="rank"><code>${source}</code><span>${count} events</span></div>`).join('');

    const ruleList = el('#rule-list');
    if (ruleList) ruleList.innerHTML = Object.entries({ 'AUTH-001': data.high, 'AUTH-002': data.critical, 'AUTH-003': data.high }).map(([rule, count]) => `<div class="rank"><strong>${rule}</strong><span>${count}</span></div>`).join('');

    const severityText = el('#severity-total');
    if (severityText) severityText.textContent = `${data.critical + data.high + data.medium + data.low} detections`;

    const simClock = el('#sim-clock');
    if (simClock) simClock.textContent = fmtTime(data.generated_at);

    drawTimeline(data.timeline);
  };

  const reset = async () => {
    await fetch('/api/reset', { method: 'POST' });
    await refresh();
  };

  document.addEventListener('click', (event) => {
    const target = event.target.closest('[data-action="reset"]');
    if (target) reset().catch(console.error);
  });

  if (el('#dashboard-app')) {
    refresh().catch(console.error);
    setInterval(() => refresh().catch(console.error), 3500);
  }
})();
