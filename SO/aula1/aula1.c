#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>

#define BUF_SIZE 1024

int main(int argc, char *argv[]) {
    char buf[BUF_SIZE];
    ssize_t bytesRead;
    int fd;

    if (argc < 2) {
        // Sem arquivo fornecido, lemos do stdin
        while ((bytesRead = read(STDIN_FILENO, buf, BUF_SIZE)) > 0) {
            write(STDOUT_FILENO, buf, bytesRead);
        }
    } else {
        // Com arquivo fornecido, abrimos e lemos dele
        fd = open(argv[1], O_RDONLY);
        if (fd == -1) {
            perror("Erro ao abrir arquivo");
            return 1;
        }

        while ((bytesRead = read(fd, buf, BUF_SIZE)) > 0) {
            write(STDOUT_FILENO, buf, bytesRead);
        }

        close(fd);
    }

    return 0;
}
