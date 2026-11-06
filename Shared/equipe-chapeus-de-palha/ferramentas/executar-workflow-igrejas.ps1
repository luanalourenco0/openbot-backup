# Inicia UMA execução do Workflow "Igrejas Mogi: mensagem ao Instagram com aprovação" pelo webhook.
# O Workflow pega sozinho a primeira linha `pendente` de projetos\igrejas-alvos.md, prepara a mensagem
# no direct e PARA na Aprovação. Quem aprova o envio é o Luan, na tela do OpenBot. Este script NÃO envia nada.
# O segredo fica em C:\Users\Lourenco_Filho\OpenBot\Secrets\webhook-igrejas-mogi.secret. Não imprima nem copie o segredo.
$ErrorActionPreference = 'Stop'
# Não inicia outra execução enquanto houver uma em andamento ou esperando aprovação (evita mensagem duplicada).
$status = Join-Path $PSScriptRoot 'status-workflow-igrejas.py'
try {
  $saidaStatus = & python $status
  if ($LASTEXITCODE -eq 3) {
    'Ja existe execucao em andamento ou esperando aprovacao. Nada foi iniciado.'
    $saidaStatus
    exit 3
  }
} catch {
  'Aviso: nao consegui conferir se ja ha execucao aberta. Seguindo mesmo assim.'
}
$url ='https://signal.openbot.run/v1/webhooks/cc987657-42b9-4e81-8e64-6f5d69fe71d5'
$secret = (Get-Content -Raw -LiteralPath 'C:\Users\Lourenco_Filho\OpenBot\Secrets\webhook-igrejas-mogi.secret').Trim()
$body = '{"type":"openbot.test"}'
$timestamp = [string][DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$deliveryId = 'igrejas-' + [guid]::NewGuid().ToString('N')
$hmac = New-Object System.Security.Cryptography.HMACSHA256 (,[Text.Encoding]::UTF8.GetBytes($secret))
$bytes = [Text.Encoding]::UTF8.GetBytes("$timestamp.$deliveryId.$body")
$signature = 'sha256=' + (($hmac.ComputeHash($bytes) | ForEach-Object { $_.ToString('x2') }) -join '')
$headers = @{
  'x-openbot-timestamp'   = $timestamp
  'x-openbot-delivery-id' = $deliveryId
  'x-openbot-signature'   = $signature
}
try {
  $r = Invoke-WebRequest -Uri $url -Method Post -Headers $headers -ContentType 'application/json' -Body $body -UseBasicParsing
  "HTTP $($r.StatusCode): execucao iniciada. Encerre sua resposta agora, sem perguntas abertas: enquanto voce estiver ocupada, a Etapa 1 fica na fila. O Luan aprova na tela do Workflow."
} catch {
  $code = $_.Exception.Response.StatusCode.value__
  "HTTP ${code}: o OpenBot nao aceitou o pedido (401 = assinatura; 400 = corpo; 202 = ok)."
  exit 1
}
