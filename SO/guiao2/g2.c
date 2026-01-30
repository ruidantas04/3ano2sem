#include <stdio.h>    // Para printf
#include <unistd.h>   // Para getpid() e getppid()

int main() {
    // Obtém e imprime o PID do processo atual
    pid_t meu_pid = getpid();
    printf("Meu PID: %d\n", meu_pid);

    // Obtém e imprime o PID do processo pai
    pid_t pai_pid = getppid();
    printf("PID do meu pai: %d\n", pai_pid);

    return 0;
}