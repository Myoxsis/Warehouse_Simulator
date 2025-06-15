import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { addEntity, getEntities, setEntities } from './simulator/entities.js';
import { nextStep, createOrder, getOrders, setOrders } from './simulator/simulation.js';
import { getAllInventory, setAllInventory } from './simulator/inventory.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(__dirname));

app.get('/api/entities', (_req, res) => {
  res.json(getEntities());
});

app.post('/api/entities', (req, res) => {
  const entity = addEntity(req.body);
  res.json(entity);
});

app.post('/api/next-step', (_req, res) => {
  res.json(nextStep());
});

app.get('/api/inventory', (_req, res) => {
  res.json(getAllInventory());
});

app.post('/api/order', (req, res) => {
  const order = createOrder(req.body);
  res.json(order);
});

app.get('/api/orders', (_req, res) => {
  res.json(getOrders());
});

app.get('/api/export', (_req, res) => {
  res.json({
    entities: getEntities(),
    inventory: getAllInventory(),
    orders: getOrders(),
  });
});

app.post('/api/import', (req, res) => {
  const { entities, inventory, orders } = req.body || {};
  if (entities) setEntities(entities);
  if (inventory) setAllInventory(inventory);
  if (orders) setOrders(orders);
  res.json({ status: 'ok' });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
