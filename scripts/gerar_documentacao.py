from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Documentacao_Tecnica_Cidades_ESG.pdf"
EVIDENCE_DIR = ROOT / "docs" / "evidencias"
REPOSITORY = "https://github.com/alvinhooo/cidades-esg-inteligentes"
ACTIONS = f"{REPOSITORY}/actions/runs/37678226458"
PACKAGES = "https://github.com/users/alvinhooo/packages?repo_name=cidades-esg-inteligentes"

GREEN = colors.HexColor("#0B6655")
PALE_GREEN = colors.HexColor("#EAF5F1")
LIGHT_GRAY = colors.HexColor("#E5E7EB")
TEXT_GRAY = colors.HexColor("#374151")

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="ProjectTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=29,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=14,
    )
)
styles.add(
    ParagraphStyle(
        name="ProjectSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=TEXT_GRAY,
        alignment=TA_CENTER,
        spaceAfter=24,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=21,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=10,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="Subsection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=6,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyTextCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.3,
        leading=15,
        textColor=colors.black,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="CaptionCustom",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=11,
        textColor=TEXT_GRAY,
        alignment=TA_CENTER,
        spaceBefore=4,
        spaceAfter=12,
    )
)


def p(text, style="BodyTextCustom"):
    return Paragraph(text, styles[style])


def table(data, widths):
    header_cell = ParagraphStyle(
        "TableHeaderCell",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.7,
        leading=11,
        textColor=colors.white,
    )
    body_cell = ParagraphStyle(
        "TableBodyCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.7,
        leading=11,
        textColor=colors.black,
    )
    wrapped = [
        [Paragraph(str(cell), header_cell if row_index == 0 else body_cell) for cell in row]
        for row_index, row in enumerate(data)
    ]
    result = Table(wrapped, colWidths=widths, repeatRows=1, hAlign="LEFT")
    result.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.7),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("GRID", (0, 0), (-1, -1), 0.6, LIGHT_GRAY),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    for row in range(1, len(data)):
        if row % 2 == 0:
            result.setStyle(TableStyle([("BACKGROUND", (0, row), (-1, row), PALE_GREEN)]))
    return result


def link(label, url):
    return p(f'<link href="{url}" color="#0B6655"><u>{label}</u></link>')


def evidence_image(filename, caption):
    path = EVIDENCE_DIR / filename
    if not path.exists():
        return []
    image = Image(str(path))
    max_w, max_h = 16.5 * cm, 19.5 * cm
    scale = min(max_w / image.imageWidth, max_h / image.imageHeight)
    image.drawWidth = image.imageWidth * scale
    image.drawHeight = image.imageHeight * scale
    image.hAlign = "CENTER"
    return [KeepTogether([image, p(caption, "CaptionCustom")])]


def footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(colors.HexColor("#C7D8D2"))
    canvas.line(2 * cm, 1.35 * cm, width - 2 * cm, 1.35 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(TEXT_GRAY)
    canvas.drawString(2 * cm, 0.85 * cm, "Cidades ESG Inteligentes - Documentação técnica DevOps")
    canvas.drawRightString(width - 2 * cm, 0.85 * cm, f"Página {doc.page}")
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Cidades ESG Inteligentes - Documentação técnica DevOps",
        author="Alvaro Miranda, João Victor, Vitor Viana e Leonardo Sabbatini",
    )
    story = []

    story += [
        Spacer(1, 1.3 * cm),
        p("Cidades ESG Inteligentes", "ProjectTitle"),
        p("Documentação técnica de CI CD containerização e ambientes", "ProjectSubtitle"),
        table(
            [
                ["Disciplina", "Integrantes", "Entrega"],
                [
                    "DevOps",
                    "Alvaro Miranda<br/>João Victor<br/>Vitor Viana<br/>Leonardo Sabbatini",
                    "Java Spring Boot<br/>Docker Compose<br/>GitHub Actions",
                ],
            ],
            [4.2 * cm, 6.4 * cm, 5.7 * cm],
        ),
        Spacer(1, 0.7 * cm),
        p("Resumo", "Section"),
        p(
            "A solução é uma API REST para registrar e acompanhar iniciativas urbanas nos pilares Ambiental, Social e Governança. A entrega automatiza compilação, testes, construção e publicação da imagem, validação em staging e promoção da mesma imagem para produção."
        ),
        p("Objetivo", "Section"),
        p(
            "Demonstrar um fluxo DevOps reproduzível, auditável e seguro, com falha rápida, ambientes isolados e evidências geradas automaticamente em cada execução."
        ),
        p("Referências verificáveis", "Section"),
        link("Repositório do projeto", REPOSITORY),
        link("Execuções do GitHub Actions", ACTIONS),
        link("Imagem no GitHub Container Registry", PACKAGES),
        PageBreak(),
    ]

    story += [
        p("1 Arquitetura da aplicação", "Section"),
        p(
            "A aplicação Spring Boot expõe endpoints REST, persiste os dados em PostgreSQL e publica sondas de saúde e identificação do ambiente pelo Spring Actuator. Staging e produção utilizam bancos, volumes, redes e perfis Spring independentes."
        ),
        table(
            [
                ["Componente", "Staging", "Produção"],
                ["Aplicação", "app-staging - porta 8081", "app-production - porta 8082"],
                ["Banco", "db-staging", "db-production"],
                ["Volume", "postgres-staging", "postgres-production"],
                ["Rede", "staging-net", "production-net"],
                ["Perfil", "staging", "production"],
            ],
            [4.2 * cm, 6.05 * cm, 6.05 * cm],
        ),
        Spacer(1, 0.45 * cm),
        p("Endpoints entregues", "Subsection"),
        table(
            [
                ["Método", "Rota", "Finalidade"],
                ["GET", "/api/iniciativas", "Listar iniciativas"],
                ["POST", "/api/iniciativas", "Registrar iniciativa"],
                ["PATCH", "/api/iniciativas/{id}/status", "Atualizar o status"],
                ["GET", "/actuator/health", "Comprovar disponibilidade"],
                ["GET", "/actuator/info", "Identificar o ambiente"],
            ],
            [2.2 * cm, 7.1 * cm, 7.0 * cm],
        ),
        PageBreak(),
    ]

    story += [
        p("2 Pipeline CI CD", "Section"),
        p(
            "O workflow é executado em pull requests, pushes na branch main e acionamentos manuais. Pull requests validam build, testes e imagem sem publicar nem implantar. Em main, a imagem é publicada no GHCR com a tag do commit e promovida sem rebuild."
        ),
        table(
            [
                ["Job", "Dependência", "Resultado"],
                ["build-and-test", "Código", "Compilação, 4 testes e relatório Surefire"],
                ["docker-image", "Testes aprovados", "Imagem única publicada no GHCR"],
                ["deploy-staging", "Imagem publicada", "Compose, PostgreSQL e smoke test"],
                ["deploy-production", "Staging aprovado", "Mesma imagem promovida e validada"],
            ],
            [4.0 * cm, 4.2 * cm, 8.1 * cm],
        ),
        Spacer(1, 0.45 * cm),
        p("Controles de qualidade", "Subsection"),
        p("• Promoção interrompida automaticamente quando qualquer etapa falha."),
        p("• Produção não é executada em pull requests."),
        p("• A senha pode ser fornecida pelo secret POSTGRES_PASSWORD e não é versionada."),
        p("• Os ambientes usam GitHub Environments e podem exigir aprovação manual."),
        p("• Logs, estado dos containers e resultados dos smoke tests são publicados como artefatos."),
        PageBreak(),
    ]

    story += [
        p("3 Containerização e orquestração", "Section"),
        p(
            "O Dockerfile utiliza build multi-stage. Maven e JDK 21 existem somente na etapa de compilação; a imagem final utiliza JRE 21 Alpine e executa com usuário não-root. O arquivo .dockerignore reduz o contexto e evita o envio de arquivos locais e documentação para a imagem."
        ),
        table(
            [
                ["Estratégia", "Implementação"],
                ["Imagem enxuta", "JRE Alpine na etapa final"],
                ["Segurança", "Usuário spring sem privilégios"],
                ["Disponibilidade", "HEALTHCHECK em /actuator/health"],
                ["Persistência", "Volumes PostgreSQL independentes"],
                ["Isolamento", "Redes e profiles distintos por ambiente"],
                ["Configuração", "Variáveis de ambiente e .env.example"],
            ],
            [5.0 * cm, 11.3 * cm],
        ),
        Spacer(1, 0.45 * cm),
        p("Comandos principais", "Subsection"),
        p("docker compose --env-file .env --profile staging up --build -d"),
        p("docker compose --env-file .env --profile production up --build -d"),
        p("docker compose --profile staging --profile production down -v"),
        PageBreak(),
    ]

    story += [
        p("4 Testes e validação automatizada", "Section"),
        p(
            "O Maven executa quatro testes de integração com Spring Boot, MockMvc e H2: criação e listagem de iniciativa, retorno 404 para atualização inexistente, health e exposição do endpoint info do Actuator. O smoke test de cada deploy valida saúde, identificação do ambiente, escrita e leitura no PostgreSQL."
        ),
        table(
            [
                ["Camada", "Verificações"],
                ["JUnit e MockMvc", "POST, GET, PATCH inexistente e health"],
                ["Smoke test", "health, info, POST e GET"],
                ["Banco", "Persistência real em PostgreSQL no Compose"],
                ["Evidência", "Summary, relatórios, logs e artefatos por SHA"],
            ],
            [5.0 * cm, 11.3 * cm],
        ),
        Spacer(1, 0.5 * cm),
        p("5 Desafios e soluções", "Section"),
        table(
            [
                ["Desafio", "Solução adotada"],
                ["Separar ambientes", "Profiles, redes, volumes, bancos e perfis Spring distintos"],
                ["Promover o mesmo artefato", "Imagem tagueada pelo SHA e reutilizada nos dois deploys"],
                ["Evitar deploy em PR", "Condição por evento nos jobs de staging e produção"],
                ["Comprovar o funcionamento", "Smoke test e artefatos de evidência gerados pelo pipeline"],
                ["Proteger credenciais", "Secret opcional e arquivos locais ignorados"],
            ],
            [5.4 * cm, 10.9 * cm],
        ),
        PageBreak(),
    ]

    story += [p("6 Evidências da execução", "Section")]
    evidence = [
        ("01-pipeline-completo.png", "Figura 1 - Pipeline completo com os quatro jobs aprovados."),
        ("02-build-e-testes.png", "Figura 2 - Build e quatro testes automatizados concluídos sem falhas."),
        ("03-imagem-ghcr.png", "Figura 3 - Imagem versionada publicada no GHCR."),
        ("04-deploy-staging.png", "Figura 4 - Deploy e smoke test de staging aprovados."),
        ("05-staging-funcionando.png", "Figura 5 - Health e identificação do ambiente staging."),
        ("06-deploy-producao.png", "Figura 6 - Deploy e smoke test de produção aprovados."),
        ("07-producao-funcionando.png", "Figura 7 - Health e identificação do ambiente production."),
    ]
    included = 0
    for filename, caption in evidence:
        blocks = evidence_image(filename, caption)
        if blocks:
            story.extend(blocks)
            included += 1
    if included == 0:
        story += [
            p(
                "A execução e seus artefatos são verificáveis diretamente nos endereços abaixo. O guia docs/EVIDENCIAS.md descreve as sete capturas exigidas para a versão de submissão."
            ),
            link("Abrir execuções do pipeline", ACTIONS),
            link("Abrir imagem publicada", PACKAGES),
            Spacer(1, 0.4 * cm),
            table(
                [["Evidência", "Fonte"]]
                + [
                    ["Pipeline e testes", "GitHub Actions - jobs e relatório Surefire"],
                    ["Imagem", "GitHub Packages - tag igual ao SHA"],
                    ["Staging", "Summary e artefato evidencias-staging-SHA"],
                    ["Produção", "Summary e artefato evidencias-production-SHA"],
                ],
                [6.0 * cm, 10.3 * cm],
            ),
        ]

    story += [
        PageBreak(),
        p("7 Checklist final", "Section"),
        table(
            [
                ["Item", "Status"],
                ["Projeto compactado e organizado", "OK"],
                ["Dockerfile multi-stage funcional", "OK"],
                ["Docker Compose com volumes, redes e variáveis", "OK"],
                ["Pipeline com build, testes, imagem e dois deploys", "OK"],
                ["README com execução, arquitetura e evidências", "OK"],
                ["Documentação técnica em PDF", "OK"],
                ["Evidências automáticas por execução", "OK"],
                ["Capturas anexadas ao PDF", f"{included}/7"],
            ],
            [12.2 * cm, 4.1 * cm],
        ),
        Spacer(1, 0.6 * cm),
        p(
            "A rastreabilidade é garantida pelo SHA usado simultaneamente na execução do workflow, na tag da imagem e nos nomes dos artefatos de evidência."
        ),
    ]

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build()
