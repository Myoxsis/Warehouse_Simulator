# Warehouse Simulator

This project contains a small web application that demonstrates a basic
supply chain simulator. The backend logic is organized under the `simulator/`
folder and data is stored as JSON in `data/`.

## Running the App

```bash
npm install   # install dependencies
npm start     # start the web server
```

Open your browser to `http://localhost:3000` to interact with the simulator.

Use the buttons in the UI to add a sample entity, advance the simulation
step, or view current inventory levels. You can also create sample orders and
view their status over time. Inventory is automatically reduced from the
source when an order is placed and added to the destination once the order is
fulfilled.

## Order Statuses

Orders move through four statuses during the simulation:

- **pending**: order has been created and is waiting to ship
- **shipped**: order is in transit
- **delayed**: shipment is temporarily delayed
- **received**: order has arrived and inventory is added to the destination
