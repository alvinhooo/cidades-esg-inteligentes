package br.com.cidadesesg.iniciativa;
import java.net.URI; import java.util.List; import org.springframework.http.ResponseEntity; import org.springframework.web.bind.annotation.*;
@RestController @RequestMapping("/api/iniciativas") public class IniciativaController {
 private final IniciativaRepository repository; public IniciativaController(IniciativaRepository repository){this.repository=repository;}
 @GetMapping public List<Iniciativa> listar(){return repository.findAll();}
 @PostMapping public ResponseEntity<Iniciativa> criar(@RequestBody Iniciativa iniciativa){Iniciativa salva=repository.save(iniciativa);return ResponseEntity.created(URI.create("/api/iniciativas/"+salva.getId())).body(salva);}
 @PatchMapping("/{id}/status") public ResponseEntity<Iniciativa> atualizarStatus(@PathVariable Long id,@RequestParam Iniciativa.Status status){return repository.findById(id).map(i->{i.atualizarStatus(status);return ResponseEntity.ok(repository.save(i));}).orElseGet(()->ResponseEntity.notFound().build());}
}
