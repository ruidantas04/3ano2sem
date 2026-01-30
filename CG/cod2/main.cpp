#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <GL/glut.h>
#endif

#include <math.h>

float tX = 0.0f;
float tY = 0.0f;
float rotateX = 0.0f;

float time = 0.0f;


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

void renderScene(void) {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();
    gluLookAt(20.0f, 20.0f, 20.0f,
        0.0f, 5.0f, 0.0f,
        0.0f, 1.0f, 0.0f);

    glBegin(GL_LINES);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex3f(-100.0f, 0.0f, 0.0f);
    glVertex3f(100.0f, 0.0f, 0.0f);

    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex3f(0.0f, -100.0f, 0.0f);
    glVertex3f(0.0f, 100.0f, 0.0f);

    glColor3f(0.0f, 0.0f, 1.0f);
    glVertex3f(0.0f, 0.0f, -100.0f);
    glVertex3f(0.0f, 0.0f, 100.0f);
    glEnd();

    glTranslatef(tX, tY, 0.0f);
    glRotatef(rotateX, 1.0, 0.0, 0.0);

    glBegin(GL_TRIANGLES);
    glColor3f(0.5f, 0.5f, 0.5f);
    glVertex3f(2.0f, 0.0f, 2.0f);
    glVertex3f(2.0f, 0.0f, -2.0f);
    glVertex3f(-2.0f, 0.0f, -2.0f);

    glColor3f(0.8f, 0.5f, 0.5f);
    glVertex3f(2.0f, 0.0f, 2.0f);
    glVertex3f(-2.0f, 0.0f, -2.0f);
    glVertex3f(-2.0f, 0.0f, 2.0f);

    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex3f(2.0f, 0.0f, 2.0f);
    glVertex3f(-2.0f, 0.0f, 2.0f);
    glVertex3f(0.0f, 3.0f, 0.0f);

    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex3f(-2.0f, 0.0f, 2.0f);
    glVertex3f(-2.0f, 0.0f, -2.0f);
    glVertex3f(0.0f, 3.0f, 0.0f);

    glColor3f(0.0f, 0.0f, 1.0f);
    glVertex3f(-2.0f, 0.0f, -2.0f);
    glVertex3f(2.0f, 0.0f, -2.0f);
    glVertex3f(0.0f, 3.0f, 0.0f);

    glColor3f(1.0f, 1.0f, 0.0f);
    glVertex3f(2.0f, 0.0f, -2.0f);
    glVertex3f(2.0f, 0.0f, 2.0f);
    glVertex3f(0.0f, 3.0f, 0.0f);


    glEnd();

    glutSwapBuffers();
}

void updateScene(int value) {
    time += 0.05f;
    rotateX += 5.0f;
    glutPostRedisplay();
    glutTimerFunc(25, updateScene, 0);
}

void specialKeys(int key, int x, int y)
{
    switch (key)
    {
    case GLUT_KEY_UP:
        tX += 0.1f;
        break;
    case GLUT_KEY_DOWN:
        tX -= 0.1f;
        break;
    case GLUT_KEY_LEFT:
        tY += 0.1f;
        break;
    case GLUT_KEY_RIGHT:
        tY -= 0.1f;
        break;
    }
    glutPostRedisplay();
}


int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
    glutInitWindowPosition(100, 100);
    glutInitWindowSize(800, 800);
    glutCreateWindow("Pirâmide 6 Triângulos");

    glutDisplayFunc(renderScene);
    glutReshapeFunc(changeSize);
    glutSpecialFunc(specialKeys);
    glutTimerFunc(16, updateScene, 0);

    glEnable(GL_DEPTH_TEST);
    glEnable(GL_CULL_FACE);
    glCullFace(GL_FRONT);


    glutMainLoop();

    return 1;
}