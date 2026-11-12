/**
 * テストの際はリポジトリを次のように配置してください
 * /repos
 *   |- nadesiko3
 *   |- nadesiko3-sqlite3
 */

import assert from 'node:assert/strict'
import test from 'node:test'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { NakoCompiler } from '../../nadesiko3/core/src/nako3.mjs'
import PluginNode from '../../nadesiko3/src/plugin_node.mjs'
import PluginSQLite3 from '../nadesiko3-sqlite3.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const nako = new NakoCompiler()
nako.debug = false
nako.addPluginObject('PluginNode', PluginNode)
nako.addPluginObject('PluginSQLite3', PluginSQLite3)
nako.setFunc('テスト', [['と'], ['で']], (a, b) => { assert.equal(a, b) })
nako.setFunc('ASSERT等', [['と'], ['が']], (a, b) => { assert.equal(a, b) })

const cmp = async (code, res) => {
  if (nako.debug) {
    console.log('code=' + code)
  }
  const r = await nako.runAsync(code)
  assert.equal(r.log, res)
}

const cmd = async (code) => {
  if (nako.debug) {
    console.log('code=' + code)
  }
  await nako.runAsync(code)
}

const runPluginSql = async (fname) => {
  const sys = {
    __sqlite3db: null,
    __setSysVar: () => {}
  }
  try {
    PluginSQLite3['SQLITE3開'].fn(fname, sys)
    await PluginSQLite3['SQLITE3実行'].fn('DROP TABLE IF EXISTS jp_test;', [], sys)
    await PluginSQLite3['SQLITE3実行'].fn('CREATE TABLE jp_test(id, content);', [], sys)
    await PluginSQLite3['SQLITE3実行'].fn('INSERT INTO jp_test (id,content) VALUES(?,?)', [1, '日本語テスト'], sys)
    const rows = await PluginSQLite3['SQLITE3全取得'].fn('SELECT * FROM jp_test', [], sys)
    assert.equal(rows[0].content, '日本語テスト')
  } finally {
    if (sys.__sqlite3db) {
      PluginSQLite3['SQLITE3閉'].fn(sys)
    }
  }
}

// SQLite3のテスト ---
const fname = path.join(__dirname, 'test_node_func.sqlite3')

test('表示', async () => {
  await cmp('3を表示', '3')
})

test('SQLite3 - create and delete', async () => {
  const sqlCreate = 'CREATE TABLE IF NOT EXISTS tt (id INTEGER PRIMARY KEY, value INTEGER);'
  await cmd(`「${fname}」をSQLITE3開く。\n「${sqlCreate}」を[]でSQLITE3実行時には;1と1がASSERT等しい;ここまで;`)
  await cmd(`「${fname}」をSQLITE3開く。「DELETE FROM tt」を[]でSQLITE3実行時には;1と1がASSERT等しい;ここまで;`)
})

test('SQLite3 - insert', async () => {
  const sqlIns = 'INSERT INTO tt (value) VALUES (?);'
  await cmd(`「${fname}」をSQLITE3開く。「${sqlIns}」を[1]でSQLITE3実行時には;1と1がASSERT等しい;;ここまで;`)
})

test('SQLite3 - SQLITE3取得した時', async () => {
  const sqlSelect = 'SELECT * FROM tt;'
  await cmd(`「${fname}」をSQLITE3開く。F=関数(D)\nD[0]['value']と1がASSERT等しい。ここまで;Fに「${sqlSelect}」を[]でSQLITE3取得時`)
})

// asyncFn のテスト
test('SQLite3 - create - SQLITE3実行', async () => {
  const sql = 'CREATE TABLE IF NOT EXISTS tt (id INTEGER PRIMARY KEY, value INTEGER);'
  await cmd(`「${fname}」をSQLITE3開く。\n「${sql}」を[]でSQLITE3実行;`)
})

test('SQLite3 - delete - SQLITE3実行', async () => {
  const sql = 'DELETE from tt;'
  await cmd(`「${fname}」をSQLITE3開く。\n「${sql}」を[]でSQLITE3実行;`)
})

test('SQLite3 - insert - SQLITE3実行', async () => {
  const sql = 'INSERT INTO tt (id,value)VALUES(?,?);'
  await cmd(`「${fname}」をSQLITE3開く。\n5回,「${sql}」を[回数,回数]でSQLITE3実行;`)
})

test('SQLite3 - select - SQLITE3取得', async () => {
  const sql = 'SELECT value FROM tt WHERE id=?;'
  await cmd(`「${fname}」をSQLITE3開く。\n「${sql}」を[1]でSQLITE3取得;それ['value']と1がASSERT等しい。`)
})

test('SQLite3 - select - SQLITE3全取得', async () => {
  const sql = 'SELECT value FROM tt WHERE id=?;'
  await cmd(`「${fname}」をSQLITE3開く。\n「${sql}」を[1]でSQLITE3全取得;それを表示。それ[0]['value']と1がASSERT等しい。`)
})

test('SQLite3 - Japanese text', async () => {
  const fname = path.join(__dirname, 'test_japanese_better.sqlite3')
  await runPluginSql(fname)
})

// --- ここまでSQLite3のテスト
