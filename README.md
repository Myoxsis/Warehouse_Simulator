# Warehouse Simulator

This project contains a small Electron application that demonstrates a basic
supply chain simulator. The backend logic is organized under the `simulator/`
folder and data is stored as JSON in `data/`.

## Running the App

```bash
npm install   # install Electron
npm start     # launch the desktop app
```

Use the buttons in the UI to add a sample entity, advance the simulation
step, or view current inventory levels. Inventory is automatically reduced
from the source when an order is placed and added to the destination once
the order is fulfilled.
