package br.com.cidadesesg;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class IniciativaControllerTest {
    @Autowired
    MockMvc mvc;

    @Test
    void criaEListaIniciativa() throws Exception {
        String body = "{\"titulo\":\"Energia solar\",\"cidade\":\"Recife\",\"pilar\":\"AMBIENTAL\",\"descricao\":\"Painéis em escolas\",\"impactoEstimado\":200}";

        mvc.perform(post("/api/iniciativas")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(body))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.status").value("PROPOSTA"));

        mvc.perform(get("/api/iniciativas"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].titulo").value("Energia solar"));
    }

    @Test
    void retorna404AoAtualizarIniciativaInexistente() throws Exception {
        mvc.perform(patch("/api/iniciativas/999/status")
                        .param("status", "CONCLUIDA"))
                .andExpect(status().isNotFound());
    }

    @Test
    void healthCheckRetornaUp() throws Exception {
        mvc.perform(get("/actuator/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"));
    }
}
