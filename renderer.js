const { spawn } = require('child_process');

document.getElementById('run-btn').addEventListener('click', () => {
  const output = document.getElementById('output');
  output.textContent = 'Running...\n';

  const sim = spawn('python', ['simulation.py']);

  sim.stdout.on('data', (data) => {
    output.textContent += data.toString();
  });

  sim.stderr.on('data', (data) => {
    output.textContent += data.toString();
  });

  sim.on('close', (code) => {
    output.textContent += `\nSimulation finished with code ${code}`;
  });
});
