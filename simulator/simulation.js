import { advanceOrders, createOrder, getOrders, setOrders } from './orders.js';
import { calculateDelay } from './transport.js';
import { adjustInventory } from './inventory.js';
import { addEntity as addEntityToStore } from './entities.js';
let currentStep = 0;

export function nextStep() {
  currentStep += 1;
  const ordersResult = advanceOrders();
  // fulfill orders by moving inventory
  for (const order of ordersResult.fulfilled) {
    adjustInventory(order.to, order.item, order.qty);
  }
  return { step: currentStep, ...ordersResult };
}

export function addSampleOrder(from, to, item, qty) {
  const delay = calculateDelay(from, to);
  return createOrder({ from, to, item, qty, delay });
}

export function addEntity(entity) {
  // forward to entities module
  return addEntityToStore(entity);
}

export { createOrder, getOrders, setOrders } from './orders.js';
