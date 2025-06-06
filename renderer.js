// Handle UI events and interact with backend via preload API
const addBtn = document.getElementById('addEntity');
const stepBtn = document.getElementById('nextStep');
const output = document.getElementById('output');
const canvas = document.getElementById('entityCanvas');
const ctx = canvas.getContext('2d');

// Form elements for entity management
const createBtn = document.getElementById('createEntity');
const updateBtn = document.getElementById('updateEntity');
const deleteBtn = document.getElementById('deleteEntity');
const idInput = document.getElementById('entityId');
const nameInput = document.getElementById('entityName');
const locationInput = document.getElementById('entityLocation');
const typeSelect = document.getElementById('entityType');

function drawEntities(entities) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  entities.forEach((e, idx) => {
    const x = 10 + (idx % 5) * 110;
    const y = 10 + Math.floor(idx / 5) * 50;
    ctx.fillStyle = '#ddd';
    ctx.fillRect(x, y, 100, 40);
    ctx.fillStyle = '#000';
    ctx.fillText(e.name, x + 5, y + 25);
  });
}

async function refresh() {
  const entities = await window.api.getEntities();
  output.textContent = JSON.stringify(entities, null, 2);
  drawEntities(entities);
}

addBtn.addEventListener('click', async () => {
  const sample = { id: Date.now().toString(), type: 'warehouse', name: 'Temp Warehouse', location: 'Unknown' };
  await window.api.addEntity(sample);
  refresh();
});

stepBtn.addEventListener('click', async () => {
  const state = await window.api.nextStep();
  output.textContent = JSON.stringify(state, null, 2);
  const entities = await window.api.getEntities();
  drawEntities(entities);
});

createBtn.addEventListener('click', async () => {
  const entity = {
    id: idInput.value || Date.now().toString(),
    name: nameInput.value,
    location: locationInput.value,
    type: typeSelect.value,
  };
  await window.api.addEntity(entity);
  refresh();
});

updateBtn.addEventListener('click', async () => {
  if (!idInput.value) return;
  const partial = {
    name: nameInput.value,
    location: locationInput.value,
    type: typeSelect.value,
  };
  await window.api.updateEntity(idInput.value, partial);
  refresh();
});

deleteBtn.addEventListener('click', async () => {
  if (!idInput.value) return;
  await window.api.deleteEntity(idInput.value);
  refresh();
});
