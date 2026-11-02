import test from 'node:test';
import assert from 'node:assert/strict';
import { dividirEmThread, planejar } from '../src/split.mjs';
import { pesoDoTweet } from '../src/tweet-length.mjs';

const semNumeracao = (t) => t.replace(/ \(\d+\/\d+\)$/, '');

test('texto curto não muda', () => {
  assert.deepEqual(dividirEmThread('oi, mundo', 280), ['oi, mundo']);
});

test('texto longo vira thread numerada, cada tweet dentro do limite', () => {
  const frase = 'Isso aqui é uma frase de teste com uma ideia curiosa. ';
  const original = frase.repeat(20).trim();
  const tweets = dividirEmThread(original, 280);
  assert.ok(tweets.length > 1);
  tweets.forEach((t, i) => {
    assert.ok(pesoDoTweet(t) <= 280, `tweet ${i + 1} passou: ${pesoDoTweet(t)}`);
    assert.match(t, new RegExp(` \\(${i + 1}/${tweets.length}\\)$`));
  });
  const remontado = tweets.map(semNumeracao).join(' ').replace(/\s+/g, ' ');
  assert.equal(remontado, original.replace(/\s+/g, ' '));
});

test('nunca corta uma palavra ao meio', () => {
  const palavras = Array.from({ length: 120 }, (_, i) => `palavra${i}`);
  const tweets = dividirEmThread(palavras.join(' '), 100);
  const vistas = tweets.flatMap((t) => semNumeracao(t).split(/\s+/));
  assert.deepEqual(vistas, palavras);
});

test('link não é cortado e conta 23', () => {
  const link = 'https://exemplo.com/' + 'x'.repeat(300);
  const texto = `${'a'.repeat(200)} ${link} ${'b'.repeat(200)}`;
  const tweets = dividirEmThread(texto, 280);
  assert.ok(tweets.some((t) => t.includes(link)), 'o link deve ficar inteiro em um tweet');
  tweets.forEach((t) => assert.ok(pesoDoTweet(t) <= 280));
});

test('palavra gigante é cortada no caractere, sem laço infinito', () => {
  const tweets = dividirEmThread('a'.repeat(700), 280);
  assert.ok(tweets.length >= 3);
  tweets.forEach((t) => assert.ok(pesoDoTweet(t) <= 280));
});

test('planejar: uma parte longa divide; thread existente só avisa', () => {
  const longa = 'palavra '.repeat(100).trim();
  assert.ok(planejar([longa], 280).tweets.length > 1);
  const r = planejar(['curto', 'b'.repeat(300)], 280);
  assert.deepEqual(r.tweets, ['curto', 'b'.repeat(300)]);
  assert.equal(r.problemas.length, 1);
  assert.match(r.problemas[0], /tweet 2/);
  assert.deepEqual(planejar([], 280).problemas, ['rascunho vazio']);
});
