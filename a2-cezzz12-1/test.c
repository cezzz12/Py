#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <time.h>

#include "domain.h"
#include "vector.h"
#include "repository.h"
#include "service.h"
void testDomain();
void testVector();
void testRepository();
void testService();
void runAllTests();

void destroyMaterialWrapper(void* material) {
    destroyMaterial((Material*)material);
}

int main() {
    printf("Running tests...\n");
    runAllTests();
    printf("All tests passed!\n");
    return 0;
}

void runAllTests() {
    testDomain();
    testVector();
    testRepository();
    testService();
}

void testDomain() {
    printf("Testing domain functions...\n");
    time_t now = time(NULL);
    Material* material = createMaterial("Flour", "Baker's Supply", 50, now);
    assert(material != NULL);
    assert(strcmp(material->name, "Flour") == 0);
    assert(strcmp(material->supplier, "Baker's Supply") == 0);
    assert(material->quantity == 50);
    assert(material->expirationDate == now);
    printf("Domain tests passed.\n");
}

void testVector() {
    printf("Testing vector functions...\n");
    Vector* vector = createVector(10);
    time_t now = time(NULL);
    Material* m1 = createMaterial("Flour", "Baker's Supply", 50, now);
    Material* m2 = createMaterial("Sugar", "Sweet Inc", 30, now + 86400);
    Material* m3 = createMaterial("Salt", "Baker's Supply", 10, now + 172800);
    addToVector(vector, m1);
    assert(getVectorSize(vector) == 1);
    addToVector(vector, m2);
    addToVector(vector, m3);
    assert(getVectorSize(vector) == 3);
    printf("Vector tests passed.\n");
}

void testRepository() {
    // Test adding materials
    Repository* repo = createRepository();
    time_t now = time(NULL);
    Material* m1 = createMaterial("Flour", "Baker's Supply", 50, now);
    Material* m2 = createMaterial("Sugar", "Sweet Inc", 30, now + 86400);
    int addResult = addMaterial(repo, m1);
    assert(addResult == 1);
    assert(getVectorSize(repo->materials) == 1);
    addResult = addMaterial(repo, m2);
    assert(addResult == 1);
    assert(getVectorSize(repo->materials) == 2);
    printf("Repository tests passed.\n");
}

void testService() {
    Repository* repo = createRepository();
    Service* service = createService(repo);
    time_t now = time(NULL);
    addMaterialService(service, "Flour", "Baker's Supply", 50, now);
    int updateResult = updateMaterialService(service, "Flour", "Baker's Supply", now, 75);
    assert(updateResult == 1);
    Vector* materials = getAllMaterialsService(service);
    Material* updated = (Material*)getFromVector(materials, 0);
    assert(updated->quantity == 75);
    destroyVector(materials, destroyMaterialWrapper);
    destroyService(service);
    printf("Service tests passed.\n");
}