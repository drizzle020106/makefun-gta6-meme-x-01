// gta6-meme-x-01 entry (Node 22, standard library only).
//
// The entry itself is the X post: the house reads the post from X (its first
// picture and its text) and hands it to the judge. This program only hands
// the post's address to the grader: it reads POST.json from the repository
// root, checks it names a real X post address, and copies it byte for byte
// to /output/POST.json, where the gate reads it. Nothing this program writes
// about the post is judged.
//
// POST.json must hold the real post address before submitting:
//   {"url": "https://x.com/<handle>/status/<id>"}
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// An X post address, as X shows it: https://x.com/<handle>/status/<digits>
// (twitter.com, with or without www./mobile., and /i/web/status/<id> also read).
const POST_URL = /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/([A-Za-z0-9_]+)\/(status|i\/web\/status)\/(\d+)\/?$/;

function readPost() {
  const path = join(BOT_DIR, 'POST.json');
  let raw;
  try {
    raw = readFileSync(path, 'utf8');
  } catch (err) {
    throw new Error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  }
  let post;
  try {
    post = JSON.parse(raw);
  } catch (err) {
    throw new Error(`POST.json is not valid JSON: ${(err as Error).message}`);
  }
  if (!post || typeof post !== 'object' || typeof post.url !== 'string') {
    throw new Error('POST.json must be an object with a string "url" field');
  }
  const m = POST_URL.exec(post.url);
  if (!m) {
    throw new Error(`POST.json url is not an X post address: ${post.url}`);
  }
  return { url: post.url, handle: m[3], id: m[5] };
}

const post = readPost();
mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
console.log(`POST.json ok: @${post.handle} status ${post.id}`);
