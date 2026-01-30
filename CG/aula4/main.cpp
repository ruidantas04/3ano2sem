#include <stdio.h>
#include <vector>
#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <GL/glew.h>
#include <GL/glut.h>
#endif

#define _USE_MATH_DEFINES
#include <math.h>

float alfa = 0.0f, beta = 0.0f, radius = 5.0f;
float camX, camY, camZ;

// Variáveis globais para os VBOs
GLuint vertices, indices;
unsigned int vertexCount, indexCount;

// Variáveis para cálculo de FPS
int frameCount = 0;
int previousTime = 0;
float fps = 0.0f;

void spherical2Cartesian() {
    camX = radius * cos(beta) * sin(alfa);
    camY = radius * sin(beta);
    camZ = radius * cos(beta) * cos(alfa);
}

void prepareCylinderData(float radius, float height, int sides) {
    std::vector<float> p;        // Vértices
    std::vector<unsigned int> i; // Índices

    float step = 2 * M_PI / sides;

    // Gerar vértices
    for (int j = 0; j < sides; j++) {
        float angle = j * step;
        float cosAngle = cos(angle) * radius;
        float sinAngle = -sin(angle) * radius;
        p.push_back(cosAngle); p.push_back(height * 0.5f); p.push_back(sinAngle); // Topo
        p.push_back(cosAngle); p.push_back(-height * 0.5f); p.push_back(sinAngle); // Base
    }
    p.push_back(0.0f); p.push_back(height * 0.5f); p.push_back(0.0f);  // Centro do topo
    p.push_back(0.0f); p.push_back(-height * 0.5f); p.push_back(0.0f); // Centro da base

    vertexCount = p.size() / 3;

    // Gerar índices
    int topCenter = vertexCount - 2;
    int bottomCenter = vertexCount - 1;
    for (int j = 0; j < sides; j++) {
        int next = (j + 1) % sides;
        i.push_back(topCenter); i.push_back(j * 2); i.push_back(next * 2); // Topo
    }
    for (int j = 0; j < sides; j++) {
        int next = (j + 1) % sides;
        i.push_back(bottomCenter); i.push_back(next * 2 + 1); i.push_back(j * 2 + 1); // Base
    }
    for (int j = 0; j < sides; j++) {
        int next = (j + 1) % sides;
        i.push_back(j * 2); i.push_back(j * 2 + 1); i.push_back(next * 2);         // Corpo, triângulo 1
        i.push_back(j * 2 + 1); i.push_back(next * 2 + 1); i.push_back(next * 2); // Corpo, triângulo 2
    }

    indexCount = i.size();

    // Configurar VBOs para os vértices
    glGenBuffers(1, &vertices);
    glBindBuffer(GL_ARRAY_BUFFER, vertices);
    glBufferData(GL_ARRAY_BUFFER, sizeof(float) * p.size(), p.data(), GL_STATIC_DRAW);

    // Configurar VBOs para os índices
    glGenBuffers(1, &indices);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indices);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(unsigned int) * i.size(), i.data(), GL_STATIC_DRAW);

    // Desvincular buffers após configuração
    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
}

void calculateFPS() {
    frameCount++;
    int currentTime = glutGet(GLUT_ELAPSED_TIME);
    if (currentTime - previousTime >= 1000) {
        fps = frameCount * 1000.0f / (currentTime - previousTime);
        frameCount = 0;
        previousTime = currentTime;
        char title[64];
        snprintf(title, sizeof(title), "CG@DI-UM - FPS: %.2f", fps);
        glutSetWindowTitle(title);
    }
}

void changeSize(int w, int h) {
    if (h == 0) h = 1;
    float ratio = w * 1.0f / h;
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glViewport(0, 0, w, h);
    gluPerspective(45.0f, ratio, 1.0f, 1000.0f);
    glMatrixMode(GL_MODELVIEW);
}

void renderScene(void) {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();
    gluLookAt(camX, camY, camZ, 0.0, 0.0, 0.0, 0.0f, 1.0f, 0.0f);

    glEnableClientState(GL_VERTEX_ARRAY);
    glBindBuffer(GL_ARRAY_BUFFER, vertices);
    glVertexPointer(3, GL_FLOAT, 0, 0);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indices);
    glDrawElements(GL_TRIANGLES, indexCount, GL_UNSIGNED_INT, 0);

    glDisableClientState(GL_VERTEX_ARRAY);

    glutSwapBuffers();
    calculateFPS();
}

void processSpecialKeys(int key, int xx, int yy) {
    switch (key) {
    case GLUT_KEY_RIGHT: alfa -= 0.1f; break;
    case GLUT_KEY_LEFT: alfa += 0.1f; break;
    case GLUT_KEY_UP: beta += 0.1f; if (beta > 1.5f) beta = 1.5f; break;
    case GLUT_KEY_DOWN: beta -= 0.1f; if (beta < -1.5f) beta = -1.5f; break;
    case GLUT_KEY_PAGE_DOWN: radius -= 0.1f; if (radius < 0.1f) radius = 0.1f; break;
    case GLUT_KEY_PAGE_UP: radius += 0.1f; break;
    }
    spherical2Cartesian();
    glutPostRedisplay();
}

void printInfo() {
    printf("Vendor: %s\n", glGetString(GL_VENDOR));
    printf("Renderer: %s\n", glGetString(GL_RENDERER));
    printf("Version: %s\n", glGetString(GL_VERSION));
    printf("\nUse Arrows to move the camera up/down and left/right\n");
    printf("Page Up and Page Down control the distance from the camera to the origin\n");
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
    glutInitWindowPosition(100, 100);
    glutInitWindowSize(1024, 1024); // Alterado para 1024x1024
    glutCreateWindow("CG@DI-UM");

    glutDisplayFunc(renderScene);
    glutIdleFunc(renderScene); // Adicionado para renderização contínua
    glutReshapeFunc(changeSize);
    glutSpecialFunc(processSpecialKeys);

#ifndef __APPLE__
    GLenum err = glewInit();
    if (err != GLEW_OK) {
        printf("GLEW init failed: %s\n", glewGetErrorString(err));
        return 1;
    }
#endif

    glEnable(GL_DEPTH_TEST);
    glEnable(GL_CULL_FACE);
    glPolygonMode(GL_FRONT, GL_LINE);

    prepareCylinderData(1.0f, 2.0f, 1048576);

    spherical2Cartesian();
    printInfo();

    previousTime = glutGet(GLUT_ELAPSED_TIME);
    glutMainLoop();
    return 0;
}
