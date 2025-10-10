const API_BASE = window.API_BASE || 'http://localhost:5000';

function fmtBadge(pollution) {
  const level = (pollution || '').toLowerCase();
  const cls = level === 'low' ? 'low' : level === 'high' ? 'high' : 'medium';
  return `<span class="badge ${cls}">${pollution} AQI</span>`;
}

function optionCard(option) {
  return `
    <div class="option">
      <div><strong>${option.label}</strong> — ${option.mode.toUpperCase()} ${fmtBadge(option.pollution)}</div>
      <div class="small">
        <span class="kpi"><strong>${option.timeMin}</strong> min</span>
        <span class="kpi"><strong>${option.distanceKm}</strong> km</span>
        <span class="kpi">Score <strong>${option.greenScore}</strong></span>
        <span class="kpi">CO₂ <strong>${option.emissionsKg} kg</strong></span>
      </div>
      <button data-route='${JSON.stringify(option)}' class="choose">Choose & earn +${option.ecoPoints}</button>
    </div>
  `;
}

async function fetchJSON(path, opts) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

async function submitForm(ev) {
  ev.preventDefault();
  const source = document.getElementById('source').value.trim();
  const destination = document.getElementById('destination').value.trim();
  if (!source || !destination) return;

  const results = document.getElementById('results');
  const recommendedDiv = document.getElementById('recommended');
  const optionsDiv = document.getElementById('options');

  recommendedDiv.innerHTML = 'Loading...';
  optionsDiv.innerHTML = '';
  results.classList.remove('hidden');

  try {
    const data = await fetchJSON('/routes/recommend', {
      method: 'POST',
      body: JSON.stringify({ source, destination }),
    });
    const { recommended, options } = data;

    if (recommended) {
      recommendedDiv.innerHTML = `
        <div><strong>Recommended:</strong> ${recommended.label} — ${recommended.mode.toUpperCase()} ${fmtBadge(recommended.pollution)}</div>
        <div class="small">
          <span class="kpi"><strong>${recommended.timeMin}</strong> min</span>
          <span class="kpi"><strong>${recommended.distanceKm}</strong> km</span>
          <span class="kpi">Score <strong>${recommended.greenScore}</strong></span>
          <span class="kpi">CO₂ <strong>${recommended.emissionsKg} kg</strong></span>
        </div>
      `;
    } else {
      recommendedDiv.innerHTML = 'No recommendation available.';
    }

    optionsDiv.innerHTML = (options || []).map(optionCard).join('');
  } catch (err) {
    recommendedDiv.innerHTML = 'Failed to load recommendations';
  }
}

async function handleChoose(ev) {
  if (!ev.target.matches('.choose')) return;
  const btn = ev.target;
  const route = JSON.parse(btn.getAttribute('data-route'));
  try {
    await fetchJSON('/routes/choose', { method: 'POST', body: JSON.stringify({ userId: 'guest', route }) });
    await refreshLeaderboard();
    btn.textContent = `Chosen! +${route.ecoPoints} points`;
    btn.disabled = true;
  } catch (e) { /* ignore */ }
}

async function refreshLeaderboard() {
  const section = document.getElementById('leaderboard');
  const ul = document.getElementById('leaders');
  try {
    const data = await fetchJSON('/leaderboard');
    const { leaders } = data;
    ul.innerHTML = (leaders || []).map(([user, pts]) => `<li><strong>${user}</strong>: ${pts} pts</li>`).join('');
    section.classList.remove('hidden');
  } catch (e) {
    // hide on failure
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('routeForm').addEventListener('submit', submitForm);
  document.body.addEventListener('click', handleChoose);
  refreshLeaderboard();
});
