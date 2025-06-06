import { contextBridge, ipcRenderer } from 'electron';

// Expose a safe API to the renderer
contextBridge.exposeInMainWorld('api', {
  addEntity: (entity) => ipcRenderer.invoke('sim:addEntity', entity),
  getEntities: () => ipcRenderer.invoke('sim:getEntities'),
  nextStep: () => ipcRenderer.invoke('sim:nextStep'),
});
