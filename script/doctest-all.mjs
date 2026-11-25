import { readdir, readFile } from 'node:fs/promises';
import { delimiter, dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const dataDir = resolve(scriptDir, '../data');
const only = process.argv.slice(2).find(arg => arg.startsWith('--only='))?.slice(7) ?? 'all';
if (!['all', 'gonako', 'lnako', 'cnako3', 'system'].includes(only) || process.argv.slice(2).some(arg => !arg.startsWith('--only='))) {
  console.error('Usage: node doctest-all.mjs [--only=all|gonako|lnako|cnako3|system]');
  process.exit(2);
}
const labels = { '表示結果': 'cnako3', 'GO表示結果': 'gonako', 'lnako表示結果': 'lnako' };
const targets = Object.fromEntries(Object.values(labels).map(name => [name, new Set()]));

async function scan(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!entry.name.startsWith('.')) await scan(path);
    } else if (entry.isFile() && entry.name.endsWith('.txt')) {
      let inBlock = false;
      let foundLabel = false;
      for (const line of (await readFile(path, 'utf8')).split(/\r?\n/)) {
        if (!inBlock) {
          if (/^\s*\{\{\{#nako3/.test(line)) { inBlock = true; foundLabel = false; }
        } else if (line.trim() === '}}}') {
          inBlock = false;
        } else if (!foundLabel) {
          const match = line.match(/^###[ \t]*([^\s:：]*表示結果)[ \t]*[:：]?[ \t]?(.*)$/);
          if (match) {
            foundLabel = true;
            const runtime = labels[match[1]];
            if (runtime) targets[runtime].add(dir);
          }
        }
      }
    }
  }
}
await scan(dataDir);
const relativeDir = dir => dir.slice(dataDir.length + 1).replaceAll('\\', '/');
const selected = {
  gonako: dir => only === 'all' || (only === 'gonako' && relativeDir(dir) === 'gonako'),
  lnako: dir => only === 'all' || (only === 'lnako' && ['lnako_lowlevel', 'lnako_node'].includes(relativeDir(dir))),
  cnako3: dir => only === 'all' || (only === 'cnako3' && /^plugin_[^/]+$/.test(relativeDir(dir)) && relativeDir(dir) !== 'plugin_system') || (only === 'system' && ['plugin_system', '文法'].includes(relativeDir(dir)))
};
const skip = new Set((process.env.DOCTEST_SKIP ?? '').split(',').map(s => s.trim()).filter(Boolean));
if ([...skip].some(name => !['gonako', 'lnako'].includes(name))) {
  console.error('DOCTEST_SKIP accepts gonako and/or lnako, separated by commas.');
  process.exit(2);
}
const cnako = join(scriptDir, 'node_modules/.bin', process.platform === 'win32' ? 'cnako3.cmd' : 'cnako3');
const doctest = join(scriptDir, 'node_modules/nadesiko3/batch/doctest.nako3');
const results = [];
for (const [label, runtime] of Object.entries(labels)) {
  const dirs = [...targets[runtime]].filter(selected[runtime]).sort();
  if (!dirs.length) continue;
  if (skip.has(runtime)) { results.push([runtime, 'skipped (DOCTEST_SKIP)']); continue; }
  const args = runtime === 'gonako'
    ? ['doctest', `--label=${label}`, ...dirs]
    : [doctest, `--label=${label}`, ...(runtime === 'lnako' ? ['--runtime=lnako', '--subcommand=run'] : ['--runtime=cnako3']), ...dirs];
  // Probe lnako before running the wrapper; otherwise every sample would fail separately.
  if (runtime === 'lnako') {
    const probe = spawnSync('lnako', ['--version'], { stdio: 'ignore' });
    if (probe.error?.code === 'ENOENT') {
      console.error('lnako was not found on PATH. Install it or set DOCTEST_SKIP=lnako.');
      results.push([runtime, 'missing']); continue;
    }
  }
  console.log(`\n[doctest] ${runtime}: ${dirs.length} directories (${label})`);
  const run = spawnSync(runtime === 'gonako' ? 'gonako' : cnako, args, { cwd: scriptDir, stdio: 'inherit', env: { ...process.env, PATH: `${join(scriptDir, 'node_modules/.bin')}${delimiter}${process.env.PATH ?? ''}` } });
  if (run.error) console.error(`${runtime}: ${run.error.message}${runtime === 'gonako' ? '. Install gonako or set DOCTEST_SKIP=gonako.' : ''}`);
  results.push([runtime, run.error ? 'missing/error' : run.status === 0 ? 'passed' : `failed (exit ${run.status ?? run.signal})`]);
}
console.log('\n[doctest] Summary:');
for (const [name, result] of results) console.log(`  ${name}: ${result}`);
if (!results.length) console.log('  no matching samples');
if (results.some(([, result]) => result !== 'passed' && !result.startsWith('skipped'))) process.exitCode = 1;
