import fs from 'fs';
import path from 'path';
import { adjustInventory } from './inventory.js';
const dataPath = path.join(process.cwd(), 'data', 'orders.json');

function readData() {
  if (!fs.existsSync(dataPath)) return [];
  return JSON.parse(fs.readFileSync(dataPath));
}

function writeData(data) {
  fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
}

export function getOrders() {
  return readData();
}

export function createOrder(order) {
  const data = readData();
  const newOrder = { ...order, status: 'pending' };
  data.push(newOrder);
  writeData(data);
  // deduct inventory from source when the order is placed
  adjustInventory(newOrder.from, newOrder.item, -newOrder.qty);
  return newOrder;
}

export function advanceOrders() {
  const orders = readData();
  const remaining = [];
  const fulfilled = [];
  for (const o of orders) {
    // transition from pending to shipped on first step
    if (o.status === 'pending') {
      o.status = 'shipped';
    } else if (o.status === 'delayed') {
      // resume shipping after a delay
      o.status = 'shipped';
    }

    // 20% chance order experiences a delay in this step
    if (o.status === 'shipped' && Math.random() < 0.2) {
      o.status = 'delayed';
    } else {
      o.delay -= 1;
    }

    if (o.delay <= 0) {
      o.status = 'received';
      fulfilled.push(o);
    } else {
      remaining.push(o);
    }
  }
  writeData(remaining);
  return { remaining, fulfilled };
}
