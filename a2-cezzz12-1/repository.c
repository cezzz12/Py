#include "repository.h"
#include <stdlib.h>
#include <string.h>
#include <time.h>


static void freeMaterialHelper(void* material) {
    destroyMaterial((Material*)material);
}

Repository* createRepository() {
    Repository* repo = (Repository*)malloc(sizeof(Repository));
    if (repo == NULL) {
        return NULL;
    }
    
    repo->materials = createVector();
    if (repo->materials == NULL) {
        free(repo);
        return NULL;
    }
    
    return repo;
}

void destroyRepository(Repository* repo) {
    if (repo != NULL) {
        destroyVector(repo->materials, freeMaterialHelper);
        free(repo);
    }
}

int findMaterial(Repository* repo, const char* name, const char* supplier, time_t expirationDate) {
    if (repo == NULL || name == NULL || supplier == NULL) {
        return -1;
    }
    
    for (int i = 0; i < getVectorSize(repo->materials); i++) {
        Material* current = (Material*)getFromVector(repo->materials, i);
        if (strcmp(current->name, name) == 0 && 
            strcmp(current->supplier, supplier) == 0 && 
            current->expirationDate == expirationDate) {
            return i;
        }
    }
    
    return -1;
}

int addMaterial(Repository* repo, Material* material) {
    if (repo == NULL || material == NULL) {
        return 0;
    }
    int existingIndex = findMaterial(repo, material->name, material->supplier, material->expirationDate);
    
    if (existingIndex != -1) {
        Material* existingMaterial = (Material*)getFromVector(repo->materials, existingIndex);
        existingMaterial->quantity += material->quantity;
        
        destroyMaterial(material);
        return 1;
    }
    
    addToVector(repo->materials, material);
    return 1;
}

int deleteMaterialByIndex(Repository* repo, int index) {
    if (repo == NULL || index < 0 || index >= getVectorSize(repo->materials)) {
        return 0;
    }
    
    // Don't save material separately, let deleteFromVector handle it
    return deleteFromVector(repo->materials, index, freeMaterialHelper);
}

Material* getMaterialByIndex(Repository* repo, int index) {
    if (repo == NULL || index < 0 || index >= getVectorSize(repo->materials)) {
        return NULL;
    }
    
    return (Material*)getFromVector(repo->materials, index);
}

Vector* getAllMaterials(Repository* repo) {
    if (repo == NULL) {
        return NULL;
    }
    
    Vector* result = createVector();
    if (result == NULL) {
        return NULL;
    }

    for (int i = 0; i < getVectorSize(repo->materials); i++) {
        Material* original = (Material*)getFromVector(repo->materials, i);
        Material* copy = copyMaterial(original);
        
        if (copy != NULL) {
            addToVector(result, copy);
        }
    }
    
    return result;
}

Vector* getExpiredMaterials(Repository* repo, const char* searchString) {
    if (repo == NULL) {
        return NULL;
    }
    
    Vector* result = createVector();
    if (result == NULL) {
        return NULL;
    }
    
    time_t currentTime = time(NULL);
    
    for (int i = 0; i < getVectorSize(repo->materials); i++) {
        Material* material = (Material*)getFromVector(repo->materials, i);
        

        if (material->expirationDate < currentTime) {
            if (searchString == NULL || searchString[0] == '\0' || 
                strstr(material->name, searchString) != NULL) {
                Material* copy = copyMaterial(material);
                if (copy != NULL) {
                    addToVector(result, copy);
                }
            }
        }
    }
    
    return result;
}

int compareByQuantity(const void* a, const void* b) {
    Material* m1 = *(Material**)a;
    Material* m2 = *(Material**)b;
    
    return m1->quantity - m2->quantity;
}

Vector* getMaterialsInShortSupply(Repository* repo, const char* supplier, int threshold) {
    if (repo == NULL || supplier == NULL) {
        return NULL;
    }
    
    Vector* result = createVector();
    if (result == NULL) {
        return NULL;
    }
    
    for (int i = 0; i < getVectorSize(repo->materials); i++) {
        Material* material = (Material*)getFromVector(repo->materials, i);

        if (strcmp(material->supplier, supplier) == 0 && material->quantity < threshold) {
            Material* copy = copyMaterial(material);
            if (copy != NULL) {
                addToVector(result, copy);
            }
        }
    }

    if (getVectorSize(result) > 1) {
        qsort(result->elements, result->size, sizeof(void*), compareByQuantity);
    }
    
    return result;
}

void initializeRepository(Repository* repo) {
    if (repo == NULL) {
        return;
    }
    
    time_t now = time(NULL);
    time_t oneDay = 24 * 60 * 60;
    time_t expired1 = now - 5 * oneDay;
    time_t expired2 = now - 2 * oneDay;
    time_t future1 = now + 7 * oneDay;
    time_t future2 = now + 14 * oneDay;
    time_t future3 = now + 30 * oneDay;
    addMaterial(repo, createMaterial("Flour", "Flour Supply", 50, future2));
    addMaterial(repo, createMaterial("Sugar", "Sweet Supply", 30, future3));
    addMaterial(repo, createMaterial("Salt", "Salt Supply", 5, future1));
    addMaterial(repo, createMaterial("Yeast", "Yeast Supply", 8, expired1));
    addMaterial(repo, createMaterial("Butter", "Butter Supply", 15, future1));
    addMaterial(repo, createMaterial("Eggs", "Poultry Farm", 24, expired2));
    addMaterial(repo, createMaterial("Milk", "Dairy Farm", 10, expired1));
    addMaterial(repo, createMaterial("Chocolate Chips", "Sweet Ingredients", 25, future3));
    addMaterial(repo, createMaterial("Vanilla Extract", "Flavor World", 3, future2));
    addMaterial(repo, createMaterial("Baking Powder", "Baker's Supply Co", 7, future1));
}