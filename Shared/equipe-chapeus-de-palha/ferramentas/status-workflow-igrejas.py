# Mostra em que pé está o Workflow "Igrejas Mogi". Só lê o banco do OpenBot, não muda nada.
# Saída 3 = há execução em andamento ou esperando aprovação (não inicie outra).
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")
BANCO = r"C:\Users\Lourenco_Filho\AppData\Roaming\OpenBot\openbot.db"
WORKFLOW = "fe3f92de-0536-4469-82a9-af57d9c66dc7"
NOMES = {
    "running": "EM ANDAMENTO",
    "approval": "ESPERANDO O LUAN APROVAR OU REJEITAR NA TELA DO WORKFLOW",
    "done": "CONCLUÍDA",
    "failed": "FALHOU",
    "stopped": "PARADA (rejeitada)",
}

db = sqlite3.connect(f"file:{BANCO}?mode=ro", uri=True)
execucoes = db.execute(
    "select number, run_id, status, started_at from workflow_runs where workflow_id = ? order by number desc limit 3",
    (WORKFLOW,),
).fetchall()
for indice, (numero, run_id, status, inicio) in enumerate(execucoes):
    print(f"Execução nº {numero}: {NOMES.get(status, status)} (início {inicio} UTC)")
    passos = db.execute(
        "select error, output from workflow_steps where run_id = ? and kind = 'agent' order by started_at",
        (run_id,),
    ).fetchall()
    for erro, saida in passos:
        if erro:
            print(f"  Erro: {erro}")
        if saida and indice == 0:
            print("  " + saida[:900].replace("\n", "\n  "))
ativa = db.execute(
    "select count(*) from workflow_runs where workflow_id = ? and status in ('running', 'approval')",
    (WORKFLOW,),
).fetchone()[0]
sys.exit(3 if ativa else 0)
