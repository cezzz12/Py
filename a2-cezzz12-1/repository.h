#ifndef REPOSITORY_H
#define REPOSITORY_H

#include "vector.h"
#include "domain.h"

typedef struct {
    Vector* materials;
} Repository;

Repository* createRepository();

void destroyRepository(Repository* repo);

int addMaterial(Repository* repo, Material* material);

int findMaterial(Repository* repo, const char* name, const char* supplier, time_t expirationDate);

int deleteMaterialByIndex(Repository* repo, int index);

Material* getMaterialByIndex(Repository* repo, int index);

Vector* getAllMaterials(Repository* repo);

Vector* getExpiredMaterials(Repository* repo, const char* searchString);

Vector* getMaterialsInShortSupply(Repository* repo, const char* supplier, int threshold);

void initializeRepository(Repository* repo);

#endif