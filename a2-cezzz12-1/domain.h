#ifndef DOMAIN_H
#define DOMAIN_H

#include <time.h>

// Material structure
typedef struct {
    char* name;
    char* supplier;
    int quantity;
    time_t expirationDate; // Using time_t for date handling
} Material;

// create a new material
Material* createMaterial(const char* name, const char* supplier, int quantity, time_t expirationDate);

//  free memory
void destroyMaterial(Material* material);
Material* copyMaterial(const Material* source);

// compare two materials (returns 1 if equal, 0 otherwise)
int areMaterialsEqual(const Material* m1, const Material* m2);

char* materialToString(const Material* material);

#endif