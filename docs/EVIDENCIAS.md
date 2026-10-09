# Guia de evidências da entrega

O pipeline gera evidências verificáveis sem depender apenas de capturas de tela. Em cada execução da branch `main`, a página **Actions** apresenta os quatro jobs e disponibiliza artefatos para download.

## Evidências geradas automaticamente

- `relatorio-testes`: relatórios Surefire com quantidade de testes, falhas e tempo de execução.
- `evidencias-staging-<sha>`: resultado do smoke test, estado dos containers e logs do Compose de staging.
- `evidencias-production-<sha>`: resultado do smoke test, estado dos containers e logs do Compose de produção.
- GitHub Packages: imagem `cidades-esg-inteligentes` identificada pela tag do commit.
- Job Summary: respostas de `/actuator/health`, `/actuator/info`, POST e GET em cada ambiente.

## Capturas exigidas para o PDF

Salve as imagens em `docs/evidencias/` com estes nomes:

1. `01-pipeline-completo.png` - execução da `main` com todos os jobs verdes.
2. `02-build-e-testes.png` - trecho com `Tests run: 4`, `Failures: 0` e `BUILD SUCCESS`.
3. `03-imagem-ghcr.png` - pacote publicado no GitHub Container Registry.
4. `04-deploy-staging.png` - Summary do smoke test de staging.
5. `05-staging-funcionando.png` - respostas de health e info do staging.
6. `06-deploy-producao.png` - Summary do smoke test de produção.
7. `07-producao-funcionando.png` - respostas de health e info da produção.

Não use imagens simuladas. As capturas devem vir da execução cujo SHA aparece na tag da imagem e nos nomes dos artefatos.

## Evidências já anexadas

- `01-pipeline-completo.png`: execução nº 10 com build, imagem, staging e produção aprovados.
- `08-health-local.png`: aplicação local respondendo com `status: UP`.
- `09-api-iniciativas-local.png`: API local listando uma iniciativa ESG cadastrada.

Ainda faltam as capturas obrigatórias numeradas de `02` a `07`.
