#include <stdlib.h>
#include <stdio.h>
#include <vector>

// Ensure M_PI is defined if not provided by cmath
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#define _USE_MATH_DEFINES
#include <cmath>

#include <IL/il.h>

#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <GL/glew.h>
#include <GL/glut.h>
#endif

// Terrain variables
float height = 2.0f;
float x = 0.0f, z = 0.0f;
float camX = 00, camY = 30, camZ = 40;
int startX, startY, tracking = 100;
int alpha = 0, beta = 45, r = 50;

ILuint t, tw, th;
GLuint buffers[1];
unsigned char* imageData;
std::vector<float> vertices;

// Tree variables
float time = 0.0f;
float rotateY = 0.0f;

void changeSize(int w, int h) {
    if (h == 0) h = 1;
    float ratio = w * 1.0 / h;

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glViewport(0, 0, w, h);
    gluPerspective(45, ratio, 1, 1000);
    glMatrixMode(GL_MODELVIEW);
}

float h(int i, int j) { return imageData[th * i + j]; }

float scale_h(float value) { return value * 150 / 255; }

float hf(float px, float pz) {
    float maxz = ((float)(th - 1)) / ((float)2);
    float maxx = ((float)(tw - 1)) / ((float)2);

    px += maxx;
    pz += maxz;

    int x1 = floor(px);
    int x2 = x1 + 1;
    int z1 = floor(pz);
    int z2 = z1 + 1;

    float fz = pz - z1;
    float fx = px - x1;

    float h_x1_z = scale_h(h(x1, z1)) * (1 - fz) + scale_h(h(x1, z2)) * fz;
    float h_x2_z = scale_h(h(x2, z1)) * (1 - fz) + scale_h(h(x2, z2)) * fz;

    float height_xz = h_x1_z * (1 - fx) + h_x2_z * fx;

    return height_xz;
}

void build_grid() {
    float max_z = (float(th - 1)) / ((float)2);
    float min_z = -max_z;
    float max_x = (float(tw - 1)) / ((float)2);
    float min_x = -max_x;

    for (int i = 0; i < th; i++) {
        for (int j = 0; j < tw; j++) {
            // Point 0
            vertices.push_back(min_x + j * 1.0f);
            vertices.push_back(scale_h(h(j, i)));
            vertices.push_back(min_z + i * 1.0f);

            // Point 1
            vertices.push_back(min_x + j * 1.0f);
            vertices.push_back(scale_h(h(j, i + 1)));
            vertices.push_back(min_z + (i + 1) * 1.0f);
        }
    }
}

void drawTerrain() {
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0]);
    glVertexPointer(3, GL_FLOAT, 0, 0);

    for (int i = 0; i < th - 1; i++) {
        glDrawArrays(GL_TRIANGLE_STRIP, tw * 2 * i, tw * 2);
    }
}

void drawAxis() {
    glBegin(GL_LINES);
    glColor3f(0, 1, 0);
    glVertex3f(0, 0, 0);
    glVertex3f(100, 0, 0);
    glColor3f(1, 0, 0);
    glVertex3f(0, 100, 0);
    glVertex3f(0, 0, 0);
    glColor3f(0, 0, 1);
    glVertex3f(0, 0, 100);
    glVertex3f(0, 0, 0);
    glColor3f(255, 255, 255);
    glEnd();
}

void drawTree(float radius, float height, int slices, int stacks) {
    glPushMatrix();

    glRotatef(-90, 1, 0, 0);
    glColor3f(0.5f, 0.35f, 0.05f);
    glutSolidCone(radius, height, slices, stacks);  

    glTranslatef(0.0, 0.0, height * 0.8);
    glColor3f(0.0f, 0.5f, 0.0f);
    glutSolidCone(radius * 2, height * 3, slices, stacks); 

    glPopMatrix();
}

void drawAllTrees(int numTrees, float minRadius, float maxRadius) {
    srand(31457);
    float max_x = (float(tw - 1)) / ((float)2);
    float max_z = (float(th - 1)) / ((float)2);

    for (int i = 0; i < numTrees; i++) {
        float x, z;
        do {
            x = (float(rand()) / RAND_MAX) * 2.0f * max_x - max_x;
            z = (float(rand()) / RAND_MAX) * 2.0f * max_z - max_z;
        } while (sqrt(x * x + z * z) < minRadius);

        glPushMatrix();
        glTranslatef(x, hf(x, z), z);
        drawTree(1.5, 5.0, 10, 10);
        glPopMatrix();
    }
}

void drawTeapotsOnCircle(float minRadius, int numTeapots, float red, float green, float blue, float rotationDirection) {
    float angleStep = 2 * M_PI / numTeapots;
    float angleOffset = time * rotationDirection;

    for (int i = 0; i < numTeapots; i++) {
        float angle = i * angleStep + angleOffset;
        float x = minRadius * cos(angle);
        float z = minRadius * sin(angle);
        float y = hf(x, z) + 3.0f;

        glPushMatrix();
        glTranslatef(x, y, z);
        glColor3f(red, green, blue);
        glutSolidTeapot(1.0);
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
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);  // Alterado para branco
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glLoadIdentity();
    float py = height + hf(x, z);
    gluLookAt(x, py, z, x + sin(alpha), py, z + cos(alpha), 0.0f, 1.0f, 0.0f);

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    glColor3f(1.0f, 1.0f, 1.0f);

    drawTerrain();
    drawAxis();
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
    drawAllTrees(200, 50, 100);
    drawTeapotsOnCircle(35, 20, 1.0f, 0.0f, 0.0f, -1.0f);  
    drawTeapotsOnCircle(15, 8, 0.0f, 0.0f, 1.0f, 1.0f);    

    // Draw a torus at the center
    glPushMatrix();
    glTranslatef(0, hf(0, 0) + 8.0f, 0);
    glColor3f(1.0f, 0.0f, 1.0f);
    glutSolidTorus(2, 8, 100, 100);
    glPopMatrix();

    glutSwapBuffers();
}

void processKeys(unsigned char key, int xx, int yy) {
    // put code to process regular keys in here
}

void processSpecialKeys(int key, int xx, int yy) {
    switch (key) {
    case GLUT_KEY_RIGHT:
        x -= cos(alpha);
        z += sin(alpha);
        break;
    case GLUT_KEY_LEFT:
        x += cos(alpha);
        z -= sin(alpha);
        break;
    case GLUT_KEY_UP:
        x += sin(alpha);
        z += cos(alpha);
        break;
    case GLUT_KEY_DOWN:
        x -= sin(alpha);
        z -= cos(alpha);
        break;
    case GLUT_KEY_PAGE_UP:
        break;
    case GLUT_KEY_PAGE_DOWN:
        break;
    }
    glutPostRedisplay();
}

void processMouseButtons(int button, int state, int xx, int yy) {
    if (state == GLUT_DOWN) {
        startX = xx;
        startY = yy;
        if (button == GLUT_LEFT_BUTTON)
            tracking = 1;
        else if (button == GLUT_RIGHT_BUTTON)
            tracking = 2;
        else
            tracking = 0;
    }
    else if (state == GLUT_UP) {
        if (tracking == 1) {
            alpha += (xx - startX);
            beta += (yy - startY);
        }
        else if (tracking == 2) {
            r -= yy - startY;
            if (r < 3) r = 3.0;
        }
        tracking = 0;
    }
}

void processMouseMotion(int xx, int yy) {
    int deltaX, deltaY;
    int alphaAux, betaAux;
    int rAux;

    if (!tracking) return;

    deltaX = xx - startX;
    deltaY = yy - startY;

    if (tracking == 1) {
        alphaAux = alpha + deltaX;
        betaAux = beta + deltaY;

        if (betaAux > 85.0)
            betaAux = 85.0;
        else if (betaAux < -85.0)
            betaAux = -85.0;

        rAux = r;
    }
    else if (tracking == 2) {
        alphaAux = alpha;
        betaAux = beta;
        rAux = r - deltaY;
        if (rAux < 3) rAux = 3;
    }
    camX = rAux * sin(alphaAux * 3.14 / 180.0) * cos(betaAux * 3.14 / 180.0);
    camZ = rAux * cos(alphaAux * 3.14 / 180.0) * cos(betaAux * 3.14 / 180.0);
    camY = rAux * sin(betaAux * 3.14 / 180.0);
}

void init() {
    // Load terrain image
    ilGenImages(1, &t);
    ilBindImage(t);
    ilLoadImage((ILstring)"terreno.jpg");
    ilConvertImage(IL_LUMINANCE, IL_UNSIGNED_BYTE);

    tw = ilGetInteger(IL_IMAGE_WIDTH);
    th = ilGetInteger(IL_IMAGE_HEIGHT);
    imageData = ilGetData();

    build_grid();

    // OpenGL settings
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_CULL_FACE);

    // Bind points to the buffer
    glEnableClientState(GL_VERTEX_ARRAY);
    glGenBuffers(1, buffers);
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0]);
    glBufferData(GL_ARRAY_BUFFER, sizeof(float) * vertices.size(), vertices.data(), GL_STATIC_DRAW);
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
    glutInitWindowPosition(100, 100);
    glutInitWindowSize(1800, 900);
    glutCreateWindow("CG@DI-UM - Terrain with Trees");

    glutDisplayFunc(renderScene);
    glutIdleFunc(renderScene);
    glutReshapeFunc(changeSize);
    glutKeyboardFunc(processKeys);
    glutSpecialFunc(processSpecialKeys);
    glutMouseFunc(processMouseButtons);
    glutMotionFunc(processMouseMotion);
    glutTimerFunc(25, updateScene, 0);

    ilInit();
#ifndef __APPLE__
    glewInit();
#endif

    init();
    glutMainLoop();

    return 0;
}