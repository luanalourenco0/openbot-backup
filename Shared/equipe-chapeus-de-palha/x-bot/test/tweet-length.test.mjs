import test from 'node:test';
import assert from 'node:assert/strict';
import { pesoDoTweet } from '../src/tweet-length.mjs';

test('ASCII e acentos valem 1', () => {
  assert.equal(pesoDoTweet('abc'), 3);
  assert.equal(pesoDoTweet('ação não é só isso'), 18);
});

test('280 letras cabem exatamente', () => {
  assert.equal(pesoDoTweet('a'.repeat(280)), 280);
});

test('emoji vale 2, inclusive sequência com ZWJ', () => {
  assert.equal(pesoDoTweet('😀'), 2);
  assert.equal(pesoDoTweet('oi 😀'), 5);
  assert.equal(pesoDoTweet('👨‍👩‍👧'), 2);
});

test('link vale 23 qualquer que seja o tamanho', () => {
  assert.equal(pesoDoTweet('https://exemplo.com/um/caminho/bem/comprido/mesmo'), 23);
  assert.equal(pesoDoTweet('veja https://a.co'), 5 + 23);
});

test('CJK vale 2 e © vale 1', () => {
  assert.equal(pesoDoTweet('日本'), 4);
  assert.equal(pesoDoTweet('©'), 1);
});
