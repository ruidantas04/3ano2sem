import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public class Aluno implements Cloneable {
    private String nome;
    private String id;
    private Map<String, Integer> nota = new HashMap<>();

    public Aluno(String n, String id) {
        this.nome = n;
        this.id = id;
    }

    public Aluno() {
        this.nome = "";
        this.id = "";
    }

    public void setNome(String n) {
        this.nome = n;
    }

    public String getNome() {
        return nome;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Integer getNota(String cadeira) {
        return nota.getOrDefault(cadeira, 0);
    }

    public void setNota(String ats, int i) throws NotaInvalidaException {
        if (i < 0 || i > 20) {
            throw new NotaInvalidaException();
        }
        this.nota.put(ats, i);
    }

    public void incrementaNota(String ats, int i) throws NotaInvalidaException{
        nota.put(ats, nota.getOrDefault(ats, 0) + 5);
    }

    public String getNumero() {
        return id;
    }

    public double media() {
        if (nota.isEmpty()) {
            return 0.0;
        }

        double soma = 0;
        for (int valor : nota.values()) {
            soma += valor;
        }

        return soma / nota.size();
    }

    @Override
    public Aluno clone() {
        try {
            Aluno copia = (Aluno) super.clone();
            copia.nota = new HashMap<>(this.nota);
            return copia;
        } catch (CloneNotSupportedException e) {
            throw new RuntimeException("Erro ao clonar o objeto Aluno", e);
        }
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        Aluno aluno = (Aluno) o;
        return Objects.equals(nome, aluno.nome) && Objects.equals(id, aluno.id) && Objects.equals(nota, aluno.nota);
    }

    @Override
    public int hashCode() {
        return Objects.hash(nome, id, nota);
    }
}
