import fs from 'fs';
import path from 'path';

const dataPath = path.join(process.cwd(), 'data', 'inventory.json');

let inventory = {};

function loadInitial() {
  if (fs.existsSync(dataPath)) {
    inventory = JSON.parse(fs.readFileSync(dataPath));
  }
}

loadInitial();

export function getAllInventory() {
  return inventory;
}

export function getInventory(id) {
  return inventory[id] || {};
}

export function setInventory(id, items) {
  inventory[id] = items;
}

export function adjustInventory(id, item, qty) {
  if (!inventory[id]) inventory[id] = {};
  inventory[id][item] = (inventory[id][item] || 0) + qty;
}

export function setAllInventory(data) {
  inventory = data || {};
}
