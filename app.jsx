// React front-end for the warehouse simulator

const api = async (method, url, data) => {
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (data) opts.body = JSON.stringify(data);
  const res = await fetch(url, opts);
  return res.json();
};

const apiClient = {
  addEntity: (entity) => api('POST', '/api/entities', entity),
  getEntities: () => api('GET', '/api/entities'),
  nextStep: () => api('POST', '/api/next-step'),
  getAllInventory: () => api('GET', '/api/inventory'),
  createOrder: (order) => api('POST', '/api/order', order),
  getOrders: () => api('GET', '/api/orders'),
};

function drawEntities(ctx, canvas, entities) {
  if (!ctx || !canvas) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  entities.forEach((e, idx) => {
    const x = 10 + (idx % 5) * 110;
    const y = 10 + Math.floor(idx / 5) * 50;
    ctx.fillStyle = '#ddd';
    ctx.fillRect(x, y, 100, 40);
    ctx.fillStyle = '#000';
    ctx.fillText(e.name, x + 5, y + 25);
  });
}

function App() {
  const [output, setOutput] = React.useState('');
  const canvasRef = React.useRef(null);

  const updateEntities = async () => {
    const entities = await apiClient.getEntities();
    setOutput(JSON.stringify(entities, null, 2));
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    drawEntities(ctx, canvas, entities);
  };

  React.useEffect(() => {
    updateEntities();
  }, []);

  const handleAddEntity = async () => {
    const sample = { id: Date.now().toString(), type: 'warehouse', name: 'Temp Warehouse', location: 'Unknown' };
    await apiClient.addEntity(sample);
    updateEntities();
  };

  const handleNextStep = async () => {
    const state = await apiClient.nextStep();
    const inventory = await apiClient.getAllInventory();
    setOutput(JSON.stringify({ state, inventory }, null, 2));
    updateEntities();
  };

  const handleViewInventory = async () => {
    const inventory = await apiClient.getAllInventory();
    setOutput(JSON.stringify(inventory, null, 2));
  };

  const handleAddOrder = async () => {
    const order = { from: 'supplier1', to: 'retailer1', item: 'item1', qty: 5, delay: 2 };
    await apiClient.createOrder(order);
    const orders = await apiClient.getOrders();
    setOutput(JSON.stringify(orders, null, 2));
  };

  const handleViewOrders = async () => {
    const orders = await apiClient.getOrders();
    setOutput(JSON.stringify(orders, null, 2));
  };

  return (
    <div>
      <h1>Supply Chain Simulator</h1>
      <button onClick={handleAddEntity}>Add Sample Entity</button>
      <button onClick={handleNextStep}>Next Step</button>
      <button onClick={handleViewInventory}>View Inventory</button>
      <button onClick={handleAddOrder}>Add Sample Order</button>
      <button onClick={handleViewOrders}>View Orders</button>
      <pre>{output}</pre>
      <canvas ref={canvasRef} id="entityCanvas" width="600" height="400" style={{border: '1px solid #ccc'}}></canvas>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);

