import fs from 'fs';
import path from 'path';
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
  data.push(order);
  writeData(data);
  return order;
}

export function advanceOrders() {
  const orders = readData();
  const remaining = [];
  const fulfilled = [];
  for (const o of orders) {
    o.delay -= 1;
    if (o.delay <= 0) {
      fulfilled.push(o);
    } else {
      remaining.push(o);
    }
  }
  writeData(remaining);
  return { remaining, fulfilled };
}
