#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>
#include <time.h>

#define BUF_SIZE 1024

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Uso: %s <origem> <destino>\n", argv[0]);
        return 1;
    }

    int src, dest;
    char buf[BUF_SIZE];
    ssize_t bytesRead, bytesWritten;
    clock_t start, end;

    // Abre o arquivo de origem
    src = open(argv[1], O_RDONLY);
    if (src == -1) {
        perror("Erro ao abrir o arquivo de origem");
        return 1;
    }

    // Abre/cria o arquivo de destino
    dest = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR);
    if (dest == -1) {
        perror("Erro ao abrir o arquivo de destino");
        close(src);
        return 1;
    }

    start = clock(); // Inicia a contagem de tempo

    // Copia o conteúdo
    while ((bytesRead = read(src, buf, BUF_SIZE)) > 0) {
        bytesWritten = write(dest, buf, bytesRead);
        if (bytesWritten != bytesRead) {
            perror("Erro ao escrever no arquivo de destino");
            close(src);
            close(dest);
            return 1;
        }
    }

    end = clock(); // Finaliza a contagem de tempo

    // Exibe o tempo gasto
    double timeTaken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Tempo gasto para copiar: %.2f segundos\n", timeTaken);

    // Fecha os arquivos
    close(src);
    close(dest);

    return 0;
}
