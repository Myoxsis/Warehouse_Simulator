import { app, BrowserWindow, ipcMain } from 'electron';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Create the main application window
function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
    },
  });

  win.loadFile('index.html');
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

// IPC handlers bridging to simulator modules
import { nextStep, addEntity, createOrder, getOrders } from './simulator/simulation.js';
import { getEntities } from './simulator/entities.js';
import { getAllInventory } from './simulator/inventory.js';

ipcMain.handle('sim:addEntity', (_event, entity) => {
  return addEntity(entity);
});

ipcMain.handle('sim:getEntities', () => {
  return getEntities();
});

ipcMain.handle('sim:nextStep', () => {
  return nextStep();
});

ipcMain.handle('sim:getAllInventory', () => {
  return getAllInventory();
});

ipcMain.handle('sim:createOrder', (_event, order) => {
  return createOrder(order);
});

ipcMain.handle('sim:getOrders', () => {
  return getOrders();
});
