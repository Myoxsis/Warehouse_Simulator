import fs from 'fs';
import path from 'path';
const dataPath = path.join(process.cwd(), 'data', 'inventory.json');

function readData() {
  if (!fs.existsSync(dataPath)) return {};
  return JSON.parse(fs.readFileSync(dataPath));
}

function writeData(data) {
  fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
}

export function getAllInventory() {
  return readData();
}

export function getInventory(id) {
  const data = readData();
  return data[id] || {};
}

export function setInventory(id, items) {
  const data = readData();
  data[id] = items;
  writeData(data);
}

export function adjustInventory(id, item, qty) {
  const data = readData();
  if (!data[id]) data[id] = {};
  data[id][item] = (data[id][item] || 0) + qty;
  writeData(data);
}
