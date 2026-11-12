const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const dir = 'C:\\Users\\Lourenco_Filho\\OpenBot\\Shared\\equipe-chapeus-de-palha\\privado\\linkedin';

const files = ['curriculo-starchild', 'curriculo-certi', 'curriculo-it4us', 'curriculo-dalcortivo'];

for (const name of files) {
  const htmlPath = path.join(dir, `${name}.html`);
  const pdfPath = path.join(dir, `${name}.pdf`);
  const cmd = `"${chrome}" --headless --disable-gpu --print-to-pdf="${pdfPath}" "${htmlPath}"`;
  console.log(`Generating ${pdfPath}...`);
  execSync(cmd);
  if (fs.existsSync(pdfPath)) {
    console.log(`Created ${pdfPath}: ${fs.statSync(pdfPath).size} bytes`);
  }
}
