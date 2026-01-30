#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <GL/glut.h>
#endif

#define _USE_MATH_DEFINES
#include <math.h>

// Variáveis globais para controle da câmera
float camX = 5.0f, camY = 5.0f, camZ = 5.0f;
float angleY = 0.0f, angleX = 0.0f;
float zoom = 5.0f;

void changeSize(int w, int h) {
    if (h == 0) h = 1;
    float ratio = w * 1.0f / h;

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glViewport(0, 0, w, h);
    gluPerspective(45.0f, ratio, 1.0f, 1000.0f);
    glMatrixMode(GL_MODELVIEW);
}

void drawCylinder(float radius, float height, int slices) {
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);

    glBegin(GL_TRIANGLES);

    float angle = 2 * M_PI / slices;
    for (int i = 0; i < slices; i++) {
        float x1 = radius * cos(i * angle);
        float z1 = radius * sin(i * angle);
        float x2 = radius * cos((i + 1) * angle);
        float z2 = radius * sin((i + 1) * angle);

        glColor3f(0.0f, 0.5f, 1.0f);
        glVertex3f(0, 0, 0);
        glVertex3f(x1, 0, z1);
        glVertex3f(x2, 0, z2);

        glColor3f(0.0f, 0.5f, 1.0f);
        glVertex3f(0, height, 0);
        glVertex3f(x2, height, z2);
        glVertex3f(x1, height, z1);

        glVertex3f(x1, 0, z1);
        glVertex3f(x2, 0, z2);
        glVertex3f(x1, height, z1);

        glVertex3f(x1, height, z1);
        glVertex3f(x2, 0, z2);
        glVertex3f(x2, height, z2);
    }
    glEnd();

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
}

void renderScene(void) {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();

    // Configurar a câmera
    float eyeX = zoom * sin(angleY) * cos(angleX);
    float eyeY = zoom * sin(angleX);
    float eyeZ = zoom * cos(angleY) * cos(angleX);
    gluLookAt(eyeX, eyeY, eyeZ,
        0.0, 0.0, 0.0,
        0.0, 1.0, 0.0);

    drawCylinder(1, 2, 50);

    glutSwapBuffers();
}

// Processar teclas normais
void processKeys(unsigned char key, int xx, int yy) {
    if (key == 'w') zoom -= 0.2f; // Aproximar
    if (key == 's') zoom += 0.2f; // Afastar

    if (zoom < 1.0f) zoom = 1.0f; // Limite mínimo

    glutPostRedisplay();
}

// Processar teclas especiais (setas para rotação)
void processSpecialKeys(int key, int xx, int yy) {
    float rotationSpeed = 0.05f;

    if (key == GLUT_KEY_LEFT) angleY -= rotationSpeed;
    if (key == GLUT_KEY_RIGHT) angleY += rotationSpeed;
    if (key == GLUT_KEY_UP) angleX -= rotationSpeed;
    if (key == GLUT_KEY_DOWN) angleX += rotationSpeed;

    glutPostRedisplay();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
    glutInitWindowPosition(100, 100);
    glutInitWindowSize(800, 800);
    glutCreateWindow("Cilindro com Linhas");

    glutDisplayFunc(renderScene);
    glutReshapeFunc(changeSize);
    glutKeyboardFunc(processKeys);
    glutSpecialFunc(processSpecialKeys);

    glEnable(GL_DEPTH_TEST);

    glutMainLoop();

    return 0;
}
