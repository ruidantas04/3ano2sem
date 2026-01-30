#include <stdio.h>
#include <stdlib.h>

#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <GL/glut.h>
#endif

#define _USE_MATH_DEFINES
#include <cmath>  // Usar apenas <cmath> para C++


float alfa = 0.0f, beta = 0.5f, radius = 100.0f;
float camX, camY, camZ;
float time = 0.0f;
float rotateY = 0.0f;


void spherical2Cartesian() {
    camX = radius * cos(beta) * sin(alfa);
    camY = radius * sin(beta);
    camZ = radius * cos(beta) * cos(alfa);
}

void changeSize(int w, int h) {
    if (h == 0)
        h = 1;

    float ratio = w * 1.0 / h;

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    glViewport(0, 0, w, h);

    gluPerspective(45.0f, ratio, 1.0f, 1000.0f);

    glMatrixMode(GL_MODELVIEW);
}

void drawTree(float radius, float height, int slices, int stacks) {
    glPushMatrix();

    glRotatef(-90, 1, 0, 0);
    glColor3f(0.5f, 0.35f, 0.05f);
    glutSolidCone(radius, height, slices, stacks);  // Tronco

    glTranslatef(0.0, 0.0, height * 0.8);
    glColor3f(0.0f, 0.5f, 0.0f);
    glutSolidCone(radius * 2, height * 3, slices, stacks);  // Copa

    glPopMatrix();
}

void drawAllTrees(int numTrees, float minRadius, float maxRadius) {
    srand(31457);
    for (int i = 0; i < numTrees; i++) {
        float x, z;
        do {
            x = (float(rand()) / RAND_MAX) * 2.0f * maxRadius - maxRadius;
            z = (float(rand()) / RAND_MAX) * 2.0f * maxRadius - maxRadius;
        } while (sqrt(x * x + z * z) < minRadius);

        glPushMatrix();
        glTranslatef(x, 0, z);
        drawTree(1.5, 5.0, 10, 10);
        glPopMatrix();
    }
}

void drawTeapotsOnCircle(float minRadius, int numTeapots, float red, float green, float blue, float rotationDirection) {
    float angleStep = 2 * M_PI / numTeapots;

    // Ajustar o ângulo de rotação com base no tempo
    float angleOffset = time * 0.1f * rotationDirection;

    for (int i = 0; i < numTeapots; i++) {
        float angle = i * angleStep + angleOffset;
        float x = minRadius * cos(angle);
        float z = minRadius * sin(angle);
        float y = 3.0f;

        glPushMatrix();
        glTranslatef(x, y, z);
        glColor3f(red, green, blue);
        glutSolidTeapot(3.0);
        glPopMatrix();
    }
}
void updateScene(int value) {
    time += 0.05f;
    rotateY += 0.5f;
    glutPostRedisplay();
    glutTimerFunc(25, updateScene, 0);
}

void renderScene(void) {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    // Atualiza o tempo
    time += 0.01f;

    // Posiciona a câmera
    glLoadIdentity();
    gluLookAt(camX, camY, camZ,
        0.0, 0.0, 0.0,
        0.0f, 1.0f, 0.0f);

    // Desenha o terreno
    glColor3f(0.2f, 0.8f, 0.2f);
    glBegin(GL_TRIANGLES);
    glVertex3f(100.0f, 0, -100.0f);
    glVertex3f(-100.0f, 0, -100.0f);
    glVertex3f(-100.0f, 0, 100.0f);

    glVertex3f(100.0f, 0, -100.0f);
    glVertex3f(-100.0f, 0, 100.0f);
    glVertex3f(100.0f, 0, 100.0f);
    glEnd();

    // Desenha as árvores
    drawAllTrees(400, 50, 100);

    // Desenha os teapots no círculo maior (rotação para a esquerda)
    drawTeapotsOnCircle(35, 20, 1.0f, 0.0f, 0.0f, -1.0f);

    // Desenha os teapots no círculo menor (rotação para a direita)
    drawTeapotsOnCircle(15, 8, 0.0f, 0.0f, 1.0f, 1.0f);

    // Desenha um torus roxo no centro
    glColor3f(1.0f, 0.0f, 1.0f);
    glutSolidTorus(2, 8, 100, 100);

    glutSwapBuffers();
}

void processKeys(unsigned char c, int xx, int yy) {
    // Placeholder para teclas normais
}

void processSpecialKeys(int key, int xx, int yy) {
    switch (key) {
    case GLUT_KEY_RIGHT: alfa -= 0.1; break;
    case GLUT_KEY_LEFT: alfa += 0.1; break;
    case GLUT_KEY_UP:
        beta += 0.1f;
        if (beta > 1.5f) beta = 1.5f;
        break;
    case GLUT_KEY_DOWN:
        beta -= 0.1f;
        if (beta < -1.5f) beta = -1.5f;
        break;
    case GLUT_KEY_PAGE_DOWN:
        radius -= 1.0f;
        if (radius < 1.0f) radius = 1.0f;
        break;
    case GLUT_KEY_PAGE_UP: radius += 1.0f; break;
    }
    spherical2Cartesian();
    glutPostRedisplay();
}

void printInfo() {
    printf("Vendor: %s\n", glGetString(GL_VENDOR));
    printf("Renderer: %s\n", glGetString(GL_RENDERER));
    printf("Version: %s\n", glGetString(GL_VERSION));
    printf("\nUse Arrows to move the camera up/down and left/right\n");
    printf("Home and End control the distance from the camera to the origin");
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
    glutInitWindowPosition(100, 100);
    glutInitWindowSize(800, 800);
    glutCreateWindow("CG@DI-UM");

    glutDisplayFunc(renderScene);
	glutTimerFunc(8, updateScene, 0);
    glutReshapeFunc(changeSize);
    glutKeyboardFunc(processKeys);
    glutSpecialFunc(processSpecialKeys);

    glEnable(GL_DEPTH_TEST);
    glEnable(GL_CULL_FACE);

    spherical2Cartesian();
    printInfo();

    // Entra no ciclo principal do GLUT
    glutMainLoop();

    return 1;
}
