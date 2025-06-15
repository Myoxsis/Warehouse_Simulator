import fs from 'fs';
import path from 'path';
import { adjustInventory } from './inventory.js';

const dataPath = path.join(process.cwd(), 'data', 'orders.json');

let orders = [];

function loadInitial() {
  if (fs.existsSync(dataPath)) {
    orders = JSON.parse(fs.readFileSync(dataPath));
  }
}

loadInitial();

export function getOrders() {
  return orders;
}

export function createOrder(order) {
  const newOrder = { ...order, status: 'pending' };
  orders.push(newOrder);
  // deduct inventory from source when the order is placed
  adjustInventory(newOrder.from, newOrder.item, -newOrder.qty);
  return newOrder;
}

export function advanceOrders() {
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
  orders = remaining;
  return { remaining, fulfilled };
}

export function setOrders(data) {
  orders = Array.isArray(data) ? data : [];
}
