// Handle UI events and interact with backend via preload API
const addBtn = document.getElementById('addEntity');
const stepBtn = document.getElementById('nextStep');
const inventoryBtn = document.getElementById('viewInventory');
const addOrderBtn = document.getElementById('addOrder');
const viewOrdersBtn = document.getElementById('viewOrders');
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

async function init() {
  const entities = await window.api.getEntities();
  output.textContent = JSON.stringify(entities, null, 2);
  drawEntities(entities);
}

window.addEventListener('DOMContentLoaded', init);

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

addOrderBtn.addEventListener('click', async () => {
  // create a sample order from supplier1 to retailer1
  const order = { from: 'supplier1', to: 'retailer1', item: 'item1', qty: 5, delay: 2 };
  await window.api.createOrder(order);
  const orders = await window.api.getOrders();
  output.textContent = JSON.stringify(orders, null, 2);
});

viewOrdersBtn.addEventListener('click', async () => {
  const orders = await window.api.getOrders();
  output.textContent = JSON.stringify(orders, null, 2);
});
