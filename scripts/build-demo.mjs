// Runs the demo build without a cross-platform env shim.
// `CHECKPD_DEMO=1 astro build` is not portable to PowerShell or cmd, and adding
// cross-env would mean a second dependency for one line.
import { spawnSync } from 'node:child_process';

const result = spawnSync('npx', ['astro', 'build'], {
  stdio: 'inherit',
  shell: true,
  env: { ...process.env, CHECKPD_DEMO: '1' },
});

process.exit(result.status ?? 1);
