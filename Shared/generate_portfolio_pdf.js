const { execSync } = require('child_process');
const fs = require('fs');

const chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const pdfPath = 'C:\\Users\\Lourenco_Filho\\OpenBot\\Shared\\equipe-chapeus-de-palha\\privado\\linkedin\\portfolio-luan-lourenco.pdf';

const cmd = `"${chrome}" --headless --disable-gpu --print-to-pdf="${pdfPath}" "https://luanalourenco0.github.io"`;
console.log('Generating portfolio PDF...');
execSync(cmd);

if (fs.existsSync(pdfPath)) {
  console.log('Generated portfolio PDF:', fs.statSync(pdfPath).size, 'bytes');
}
