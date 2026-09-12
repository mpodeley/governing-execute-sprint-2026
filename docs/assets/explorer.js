'use strict';
const broker = document.getElementById('broker');
const arrival = document.getElementById('arrival');
const delay = document.getElementById('delay');
function updateTrace() {
  const row = window.contractResults.matrix.find(r => r.probe === 'C4' && r.adapter === broker.value);
  const items = row.events.filter(e => ['action', 'queued', 'revoke'].includes(e.kind));
  const list = document.getElementById('trace');
  list.replaceChildren();
  items.forEach(e => {
    const li = document.createElement('li');
    const tick = document.createElement('strong');
    tick.textContent = 'Tick ' + e.tick + ' ';
    let description;
    if (e.kind === 'queued') description = 'Worker a queues another request.';
    else if (e.kind === 'revoke') description = 'Parent authority is revoked.';
    else {
      const subject = e.tick === 0 ? 'Worker a’s first action' : e.tick === 3 ? 'Queued request' : 'Sibling request';
      description = subject + (e.accepted ? ' commits 10 units.' : ' is refused.');
    }
    li.append(tick, document.createTextNode(description));
    list.append(li);
  });
  const last = items.filter(e => e.kind === 'action').at(-1);
  document.getElementById('spent').textContent = 'Historical root expenditure: ' + last.root_spent + ' units';
}
function updateTiming() {
  const a = arrival.value === 'absent' ? null : Number(arrival.value);
  const d = a === null || delay.value === 'none' ? null : Number(delay.value);
  delay.disabled = a === null;
  const rows = window.contractResults.timing.filter(r => r.arrival === a && r.delay === d);
  document.getElementById('hold-count').textContent = rows.find(r => r.immediate_hold).hazardous_effects + ' / 10';
  document.getElementById('decision-count').textContent = rows.find(r => !r.immediate_hold).hazardous_effects + ' / 10';
  document.getElementById('timing-note').textContent = 'Both policies commit all ten auxiliary actions. ' +
    (a === null ? 'Without a report, neither policy stops hazardous work.' :
     d === null ? 'No decision arrives within the observation window; the receipt-triggered hold remains in place.' :
     a === 4 ? 'A late report cannot undo earlier effects.' : 'Receipt and any due decision precede the action at that tick.');
}
broker.addEventListener('change', updateTrace);
arrival.addEventListener('change', updateTiming);
delay.addEventListener('change', updateTiming);
updateTrace();
updateTiming();
