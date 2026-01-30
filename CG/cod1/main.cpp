#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <GL/glut.h>
#endif

#define _USE_MATH_DEFINES
#include <math.h>
#include <stdio.h>

float time = 0.0f;
float scale = 1.0f;
float rotatey = 0.0f;
float translatey = 0.0f;


void changeSize(int w, int h)
{
	// Prevent a divide by zero, when window is too short
	// (you can�t make a window with zero width).
	if (h == 0)
		h = 1;
	// compute window's aspect ratio
	float ratio = w * 1.0f / h;
	// Set the projection matrix as current
	glMatrixMode(GL_PROJECTION);
	// Load the identity matrix
	glLoadIdentity();
	// Set the perspective
	gluPerspective(45.0f, ratio, 1.0f, 1000.0f);
	// return to the model view matrix mode
	glMatrixMode(GL_MODELVIEW);

	// finally set the viewport to be the entire window
	glViewport(0, 0, w, h);
}

void specialKeys(int key, int x, int y)
{
	switch (key)
	{
	case GLUT_KEY_UP:
		translatey += 0.2f;
		break;
	case GLUT_KEY_DOWN:
		translatey -= 0.2f;
		break;
	case GLUT_KEY_LEFT:
		rotatey -= 5.0f;
		break;
	case GLUT_KEY_RIGHT:
		rotatey += 5.0f;
		break;
	}
	glutPostRedisplay();
}

void renderScene(void)
{
	// clear buffers
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	// set camera
	glLoadIdentity();
	gluLookAt(0.0f, 0.0f, 5.0f,
		0.0f, 0.0f, -1.0f,
		0.0f, 1.0f, 0.0f);

	glScalef(scale / 4, scale / 4, scale / 4);	
	glRotatef(rotatey, 0.0f, 1.0f, 0.0f);
	glTranslated(0.0f,translatey,0.0f);
	glColor3f(1, 0,0);

	// put drawing instructions here
	glutWireTorus(1.0f, 2.0f, 16, 16);

	// End of frame
	glutSwapBuffers();
}

void updateScene(int value) {
	time += 0.05f;
	scale = sin(time) + 1.5;
	glutPostRedisplay();
	glutTimerFunc(25, updateScene, 0);
}



void printInfo() {

	printf("Vendor: %s\n", glGetString(GL_VENDOR));
	printf("Renderer: %s\n", glGetString(GL_RENDERER));
	printf("Version: %s\n", glGetString(GL_VERSION));
}


int main(int argc, char** argv)
{
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
	glutInitWindowPosition(300, 100);
	glutInitWindowSize(1000, 1000);
	glutCreateWindow("Pratica - 1");


	// put callback registry here
	glutReshapeFunc(changeSize);
	glutIdleFunc(renderScene);
	glutDisplayFunc(renderScene);
	glutTimerFunc(16, updateScene, 0);
	glutSpecialFunc(specialKeys);

	


	// some OpenGL settings
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_CULL_FACE);
	glClearColor(0.0f, 0.0f, 0.0f, 0.0f);

	// enter GLUT�s main cycle
	glutMainLoop();

	return 1;
}