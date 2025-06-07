// Handle UI events and interact with backend via preload API
const addBtn = document.getElementById('addEntity');
const stepBtn = document.getElementById('nextStep');
const inventoryBtn = document.getElementById('viewInventory');
const output = document.getElementById('output');
const canvas = document.getElementById('entityCanvas');
const ctx = canvas.getContext('2d');

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

addBtn.addEventListener('click', async () => {
  const sample = { id: Date.now().toString(), type: 'warehouse', name: 'Temp Warehouse', location: 'Unknown' };
  await window.api.addEntity(sample);
  const entities = await window.api.getEntities();
  output.textContent = JSON.stringify(entities, null, 2);
  drawEntities(entities);
});

stepBtn.addEventListener('click', async () => {
  const state = await window.api.nextStep();
  const inventory = await window.api.getAllInventory();
  output.textContent = JSON.stringify({ state, inventory }, null, 2);
  const entities = await window.api.getEntities();
  drawEntities(entities);
});

inventoryBtn.addEventListener('click', async () => {
  const inventory = await window.api.getAllInventory();
  output.textContent = JSON.stringify(inventory, null, 2);
});
