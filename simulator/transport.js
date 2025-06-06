// Simple transport delay calculations
export function calculateDelay(fromId, toId) {
  // For demo, delay is random between 1 and 3 steps
  return 1 + Math.floor(Math.random() * 3);
}
