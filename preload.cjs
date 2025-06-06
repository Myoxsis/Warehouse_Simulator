const { contextBridge, ipcRenderer } = require('electron');

// Expose a safe API to the renderer
contextBridge.exposeInMainWorld('api', {
  addEntity: (entity) => ipcRenderer.invoke('sim:addEntity', entity),
  updateEntity: (id, partial) => ipcRenderer.invoke('sim:updateEntity', id, partial),
  deleteEntity: (id) => ipcRenderer.invoke('sim:deleteEntity', id),
  getEntities: () => ipcRenderer.invoke('sim:getEntities'),
  nextStep: () => ipcRenderer.invoke('sim:nextStep'),
});
