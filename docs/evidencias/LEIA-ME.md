# Evidências (prints)

Salve aqui os prints com **exatamente** estes nomes (o README.md já aponta para eles):

| Arquivo | O que capturar |
| --- | --- |
| `01-pipeline-completo.png` | Aba **Actions** > execução da `main`: jobs build-and-test, docker-image, deploy-staging e deploy-production, todos verdes |
| `02-build-e-testes.png` | Log do job build-and-test mostrando `Tests run: ... Failures: 0` e `BUILD SUCCESS` |
| `03-imagem-ghcr.png` | Página do repositório > **Packages** (imagem `cidades-esg-inteligentes` publicada) |
| `04-deploy-staging.png` | Resumo (Summary) / log do job deploy-staging com o smoke test aprovado |
| `05-staging-funcionando.png` | Terminal local: `curl localhost:8081/actuator/health` e `/actuator/info` (`"ambiente":"staging"`) |
| `06-deploy-producao.png` | Resumo (Summary) / log do job deploy-production com o smoke test aprovado |
| `07-producao-funcionando.png` | Terminal local: `curl localhost:8082/actuator/health` e `/actuator/info` (`"ambiente":"production"`) |

Depois de salvar os prints, marque os itens pendentes do checklist no README.md.
