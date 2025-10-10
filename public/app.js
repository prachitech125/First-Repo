async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`${response.status} ${response.statusText}: ${text}`);
  }
  return response.json();
}

async function updateStatus() {
  const statusEl = document.getElementById('status');
  try {
    const data = await fetchJson('/api/health');
    statusEl.textContent = `Backend status: ${data.status} at ${new Date(data.timestamp).toLocaleString()}`;
  } catch (err) {
    statusEl.textContent = `Backend error: ${err.message}`;
  }
}

async function wireMessageButton() {
  const btn = document.getElementById('btnMessage');
  const out = document.getElementById('message');
  btn.addEventListener('click', async () => {
    btn.disabled = true;
    out.textContent = 'Fetching...';
    try {
      const data = await fetchJson('/api/message');
      out.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      out.textContent = `Error: ${err.message}`;
    } finally {
      btn.disabled = false;
    }
  });
}

updateStatus();
wireMessageButton();
