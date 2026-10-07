#!/usr/bin/env bash
# Uso: scripts/smoke-test.sh <porta> <ambiente> [arquivo-de-evidencia]
# Espera a aplicação ficar saudável, grava e lê uma iniciativa e registra a evidência
# no resumo do GitHub Actions ($GITHUB_STEP_SUMMARY) quando disponível.
set -euo pipefail

PORT="${1:?informe a porta}"
ENV_NAME="${2:?informe o ambiente (staging|production)}"
BASE="http://localhost:${PORT}"
EVIDENCE_FILE="${3:-}"
SUMMARY_FILE="${GITHUB_STEP_SUMMARY:-/dev/stdout}"

ok=0
for i in $(seq 1 30); do
  if curl -fsS "${BASE}/actuator/health" 2>/dev/null | grep -q '"status":"UP"'; then ok=1; break; fi
  echo "Aguardando a aplicação (${i}/30)..."; sleep 5
done
[ "$ok" = 1 ] || { echo "Health check falhou em ${BASE}"; exit 1; }

HEALTH=$(curl -fsS "${BASE}/actuator/health")
INFO=$(curl -fsS "${BASE}/actuator/info")
CREATED=$(curl -fsS -X POST "${BASE}/api/iniciativas" -H 'Content-Type: application/json' \
  -d "{\"titulo\":\"Smoke test ${ENV_NAME}\",\"cidade\":\"São Paulo\",\"pilar\":\"AMBIENTAL\",\"descricao\":\"Validação automática do deploy\",\"impactoEstimado\":100}")
LIST=$(curl -fsS "${BASE}/api/iniciativas")
echo "${LIST}" | grep -q "Smoke test ${ENV_NAME}" || { echo "Iniciativa não encontrada na listagem"; exit 1; }
echo "${INFO}" | grep -q "${ENV_NAME}" || { echo "/actuator/info não indica o ambiente ${ENV_NAME}"; exit 1; }

render_evidence() {
  echo "## ✅ Deploy validado: ${ENV_NAME}"
  echo ""
  echo "| Verificação | Resultado |"
  echo "| --- | --- |"
  echo "| URL testada | \`${BASE}\` |"
  echo "| GET /actuator/health | \`${HEALTH}\` |"
  echo "| GET /actuator/info | \`${INFO}\` |"
  echo "| POST /api/iniciativas | criada com sucesso |"
  echo "| GET /api/iniciativas | contém a iniciativa criada |"
  echo ""
  echo "Resposta do POST:"
  echo '```json'; echo "${CREATED}"; echo '```'
}

render_evidence >> "${SUMMARY_FILE}"
if [ -n "${EVIDENCE_FILE}" ]; then
  mkdir -p "$(dirname "${EVIDENCE_FILE}")"
  render_evidence > "${EVIDENCE_FILE}"
fi
echo "Smoke test de ${ENV_NAME} concluído com sucesso."
