package br.com.cidadesesg.iniciativa;
import jakarta.persistence.*;
@Entity public class Iniciativa {
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
 @Column(nullable=false) private String titulo; @Column(nullable=false) private String cidade;
 @Enumerated(EnumType.STRING) @Column(nullable=false) private Pilar pilar;
 @Column(nullable=false,length=1000) private String descricao; private Integer impactoEstimado;
 @Enumerated(EnumType.STRING) @Column(nullable=false) private Status status=Status.PROPOSTA;
 protected Iniciativa(){} public Iniciativa(String titulo,String cidade,Pilar pilar,String descricao,Integer impactoEstimado){this.titulo=titulo;this.cidade=cidade;this.pilar=pilar;this.descricao=descricao;this.impactoEstimado=impactoEstimado;}
 public Long getId(){return id;} public String getTitulo(){return titulo;} public void setTitulo(String titulo){this.titulo=titulo;} public String getCidade(){return cidade;} public void setCidade(String cidade){this.cidade=cidade;} public Pilar getPilar(){return pilar;} public void setPilar(Pilar pilar){this.pilar=pilar;} public String getDescricao(){return descricao;} public void setDescricao(String descricao){this.descricao=descricao;} public Integer getImpactoEstimado(){return impactoEstimado;} public void setImpactoEstimado(Integer impactoEstimado){this.impactoEstimado=impactoEstimado;} public Status getStatus(){return status;} public void atualizarStatus(Status status){this.status=status;}
 public enum Pilar { AMBIENTAL, SOCIAL, GOVERNANCA } public enum Status { PROPOSTA, EM_ANDAMENTO, CONCLUIDA }
}
