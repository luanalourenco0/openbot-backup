# Roda a bateria de testes: cada foto de teste com --rosto 0, 0.5 e 1.0 (escala 2).
# Uso (em ferramentas\restauracao):  powershell -File teste\rodar_testes.ps1 [-Fotos foto1_rapaz_quepe,foto2_homem_riscos] [-Rostos 0,0.5,1.0]
# Saida: teste\<foto>\rosto_<valor>\ (etapas, relatorio.json, lado a lado). Depois: .venv\Scripts\python.exe teste\resumir.py
param(
  [string[]]$Fotos = @('foto1_rapaz_quepe', 'foto2_homem_riscos', 'foto3_senhora_manchas'),
  [string[]]$Rostos = @('0', '0.5', '1.0')
)
$base = Split-Path -Parent $PSScriptRoot
$py = Join-Path $base '.venv\Scripts\python.exe'
foreach ($f in $Fotos) {
  foreach ($r in $Rostos) {
    $saida = Join-Path $base "teste\$f\rosto_$r"
    Write-Host "=== $f --rosto $r"
    & $py (Join-Path $base 'restaurar.py') (Join-Path $base "teste\$f.jpg") $saida --rosto $r --escala 2 2>&1 |
      Where-Object { $_ -match '^(\[|Pronto|Entrada|Rostos|Traceback|\w*Error)' }
  }
}
