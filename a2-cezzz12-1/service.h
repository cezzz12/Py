#ifndef SERVICE_H
#define SERVICE_H

#include "repository.h"

typedef struct {
    char* type;
    Material* material; // Material before operation (for undo)
    Material* newMaterial; // Material after operation (for redo)
    int index;          // Index for delete/update operations
} Operation;

typedef struct {
    Repository* repo;
    Vector* undoStack;
    Vector* redoStack;
} Service;

Service* createService(Repository* repo);

void destroyService(Service* service);

int addMaterialService(Service* service, const char* name, const char* supplier, 
                       int quantity, time_t expirationDate);

int deleteMaterialService(Service* service, const char* name, const char* supplier, 
                         time_t expirationDate);

int updateMaterialService(Service* service, const char* name, const char* supplier, 
                         time_t expirationDate, int newQuantity);

Vector* getAllMaterialsService(Service* service);

Vector* getExpiredMaterialsService(Service* service, const char* searchString);

Vector* getMaterialsInShortSupplyService(Service* service, const char* supplier, int threshold);

static void freeMaterialHelper(void* material);

int undo(Service* service);

int redo(Service* service);

Operation* createOperation(const char* type, Material* material, Material* newMaterial, int index);

void destroyOperation(void* op);

#endif