#include "vector.h"
#include <stdlib.h>

#define INITIAL_CAPACITY 10
#define RESIZE_FACTOR 2

Vector* createVector() {
    Vector* v = (Vector*)malloc(sizeof(Vector));
    if (v == NULL) {
        return NULL; // Memory allocation failed
    }
    
    v->capacity = INITIAL_CAPACITY;
    v->size = 0;
    v->elements = (void**)malloc(v->capacity * sizeof(void*));
    
    if (v->elements == NULL) {
        free(v);
        return NULL;
    }
    
    return v;
}

void destroyVector(Vector* v, void (*destroyElement)(void*)) {
    if (v != NULL) {
        if (destroyElement != NULL) {
            // Call the destruction function for each element
            for (int i = 0; i < v->size; i++) {
                destroyElement(v->elements[i]);
            }
        }

        free(v->elements);
        free(v);
    }
}

void addToVector(Vector* v, void* element) {
    if (v == NULL || element == NULL) {
        return;
    }
    

    if (v->size >= v->capacity) {
        resizeVector(v);
    }
    
    v->elements[v->size++] = element;
}

int deleteFromVector(Vector* v, int index, void (*destroyElement)(void*)) {
    if (v == NULL || index < 0 || index >= v->size) {
        return 0; // Invalid input
    }

    // Store the element to be deleted
    void* elementToDelete = v->elements[index];

    // Shift elements
    for (int i = index; i < v->size - 1; i++) {
        v->elements[i] = v->elements[i + 1];
    }

    v->size--;

    // Free the memory of the deleted element if a destroy function is provided
    if (destroyElement != NULL) {
        destroyElement(elementToDelete);
    }

    return 1; // Success
}

void* getFromVector(Vector* v, int index) {
    if (v == NULL || index < 0 || index >= v->size) {
        return NULL; // Invalid input
    }
    
    return v->elements[index];
}

int updateVector(Vector* v, int index, void* newElement, void (*destroyElement)(void*)) {
    if (v == NULL || index < 0 || index >= v->size || newElement == NULL) {
        return 0; // Invalid input
    }

    // Free the old element if a destroy function is provided
    if (destroyElement != NULL) {
        destroyElement(v->elements[index]);
    }
    
    v->elements[index] = newElement;
    return 1; // Success
}

int getVectorSize(Vector* v) {
    if (v == NULL) {
        return 0;
    }
    return v->size;
}

void resizeVector(Vector* v) {
    if (v == NULL) {
        return;
    }
    
    int newCapacity = v->capacity * RESIZE_FACTOR;
    void** newElements = (void**)realloc(v->elements, newCapacity * sizeof(void*));
    
    if (newElements != NULL) {
        v->elements = newElements;
        v->capacity = newCapacity;
    }

}