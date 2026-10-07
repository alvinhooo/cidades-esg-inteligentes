# Cidades ESG Inteligentes
**Disciplina:** DevOps | **Integrante:** Ramiro Miranda
API REST para registrar iniciativas de sustentabilidade de cidades, acompanhar o impacto estimado e classificar cada iniciativa nos pilares Ambiental, Social e Governança (ESG).
## Como executar localmente com Docker
1. Copie as variáveis de exemplo: `cp .env.example .env`.
2. Inicie o ambiente de homologação: `docker compose --env-file .env --profile staging up --build -d`.
3. Consulte a saúde: `curl http://localhost:8081/actuator/health`.
4. Consulte iniciativas: `curl http://localhost:8081/api/iniciativas`.
5. Para produção local, use: `docker compose --env-file .env --profile production up --build -d` e acesse a porta `8082`.
6. Finalize com `docker compose down -v`.
## Pipeline CI/CD
O GitHub Actions executa o workflow em `.github/workflows/ci-cd.yml`. Em cada push para `main`, ele:
1. compila o projeto Maven e executa os testes;
2. constrói e sobe o ambiente **staging** com Docker Compose, banco PostgreSQL, rede e health check;
3. constrói e sobe o ambiente **production** isolado após a conclusão do staging;
4. encerra e remove os containers ao fim de cada job, preservando o log como evidência da entrega automatizada.
O workflow usa runners hospedados pelo GitHub e não requer VPS, chaves SSH ou secrets. Os ambientes são temporários e verificáveis nos logs.
## Containerização
O `Dockerfile` usa build multi-stage: Maven com JDK 21 gera o JAR e uma imagem JRE 21 enxuta o executa sem usuário root. O `docker-compose.yml` disponibiliza instâncias isoladas em staging e produção, cada uma com banco PostgreSQL, volume persistente, rede interna e variáveis de ambiente.
## Evidências do funcionamento
Antes de enviar a atividade, inclua capturas da aba **Actions** com os jobs `test`, `deploy-staging` e `deploy-production` concluídos e dos logs com o retorno `UP` de `/actuator/health`.
## Tecnologias utilizadas
- Java 21, Spring Boot 3.3, Spring Web, Spring Data JPA e Actuator
- JUnit 5 e Spring Boot Test
- PostgreSQL 16 e H2 para testes
- Docker, Docker Compose e GitHub Actions
## Endpoints principais
| Método | Rota | Finalidade |
| --- | --- | --- |
| GET | `/api/iniciativas` | Lista iniciativas ESG |
| POST | `/api/iniciativas` | Cria iniciativa |
| PATCH | `/api/iniciativas/{id}/status?status=EM_ANDAMENTO` | Atualiza status |
| GET | `/actuator/health` | Health check |
## Checklist de entrega
- [x] Projeto compactado em `.zip` com estrutura organizada
- [x] Dockerfile e Docker Compose
- [x] Pipeline com build, testes e dois ambientes
- [x] README e documentação técnica
- [ ] Evidências reais do pipeline anexadas
