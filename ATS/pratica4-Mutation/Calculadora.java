public class Calculadora {
    int resultado;

    public Calculadora() {
        resultado = 0;
    }
    public Calculadora(int x) {
        resultado = x;
    }
    int adiciona(int y) {
        resultado = resultado + y;
        return resultado;
    }
    int adiciona(int x, int y) {
        resultado = x + y;
        return resultado;
    }
    int subtrai(int y) {
        resultado = resultado - y;
        return resultado;
    }
    int subtrai(int x, int y) {
        resultado = x - y;
        return resultado;
    }
    int ultimoResultado() {
        return resultado;
    }
}
