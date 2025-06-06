import fs from 'fs';
import path from 'path';
const dataPath = path.join(process.cwd(), 'data', 'entities.json');

// Allowed entity types for validation
export const ALLOWED_TYPES = [
  'supplier',
  'manufacturer',
  'warehouse',
  'distributor',
  'retailer',
];

function readData() {
  if (!fs.existsSync(dataPath)) return [];
  return JSON.parse(fs.readFileSync(dataPath));
}

function writeData(data) {
  fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
}

export function getEntities() {
  return readData();
}

export function addEntity(entity) {
  if (!ALLOWED_TYPES.includes(entity.type)) {
    throw new Error(`Invalid entity type: ${entity.type}`);
  }
  const data = readData();
  data.push(entity);
  writeData(data);
  return entity;
}

export function updateEntity(id, partial) {
  const data = readData();
  const idx = data.findIndex(e => e.id === id);
  if (idx !== -1) {
    const updated = { ...data[idx], ...partial };
    if (updated.type && !ALLOWED_TYPES.includes(updated.type)) {
      throw new Error(`Invalid entity type: ${updated.type}`);
    }
    data[idx] = updated;
    writeData(data);
    return data[idx];
  }
  return null;
}

export function deleteEntity(id) {
  const data = readData();
  const filtered = data.filter(e => e.id !== id);
  writeData(filtered);
}
