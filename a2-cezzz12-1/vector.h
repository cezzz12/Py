#ifndef VECTOR_H
#define VECTOR_H

typedef struct {
    void** elements;     // Dynamic array of void pointers
    int size;
    int capacity;
} Vector;

Vector* createVector();

void destroyVector(Vector* v, void (*destroyElement)(void*));

void addToVector(Vector* v, void* element);

//int deleteFromVector(Vector* v, int index);

void* getFromVector(Vector* v, int index);

//int updateVector(Vector* v, int index, void* newElement);
int deleteFromVector(Vector* v, int index, void (*destroyElement)(void*));
int updateVector(Vector* v, int index, void* newElement, void (*destroyElement)(void*));
int getVectorSize(Vector* v);

void resizeVector(Vector* v);

#endif