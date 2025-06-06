// Handle UI events and interact with backend via preload API
const addBtn = document.getElementById('addEntity');
const stepBtn = document.getElementById('nextStep');
const output = document.getElementById('output');

addBtn.addEventListener('click', async () => {
  const sample = { id: Date.now().toString(), type: 'warehouse', name: 'Temp Warehouse', location: 'Unknown' };
  await window.api.addEntity(sample);
  const entities = await window.api.getEntities();
  output.textContent = JSON.stringify(entities, null, 2);
});

stepBtn.addEventListener('click', async () => {
  const state = await window.api.nextStep();
  output.textContent = JSON.stringify(state, null, 2);
});
