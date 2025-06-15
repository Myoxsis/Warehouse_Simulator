import fs from 'fs';
import path from 'path';

const dataPath = path.join(process.cwd(), 'data', 'entities.json');

let entities = [];

function loadInitial() {
  if (fs.existsSync(dataPath)) {
    entities = JSON.parse(fs.readFileSync(dataPath));
  }
}

loadInitial();

export function getEntities() {
  return entities;
}

export function addEntity(entity) {
  entities.push(entity);
  return entity;
}

export function updateEntity(id, partial) {
  const idx = entities.findIndex(e => e.id === id);
  if (idx !== -1) {
    entities[idx] = { ...entities[idx], ...partial };
    return entities[idx];
  }
  return null;
}

export function deleteEntity(id) {
  entities = entities.filter(e => e.id !== id);
}

export function setEntities(data) {
  entities = Array.isArray(data) ? data : [];
}
