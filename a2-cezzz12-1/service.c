#include "service.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "domain.h"
void destroyOperation(void* op) {
    if (op == NULL) {
        return;
    }
    
    Operation* operation = (Operation*)op;
    
    free(operation->type);
    
    if (operation->material != NULL) {
        destroyMaterial(operation->material);
    }
    
    if (operation->newMaterial != NULL) {
        destroyMaterial(operation->newMaterial);
    }

    free(operation);
}
static void freeMaterialHelper(void* material) {
    // Cast the void pointer to Material* and free any allocated memory
    Material* mat = (Material*)material;
    // Free any dynamically allocated fields of the Material struct
    // ...
    // If you're not freeing the material itself here, you don't need to do anything else
}
Service* createService(Repository* repo) {
    if (repo == NULL) {
        return NULL;
    }
    
    Service* service = (Service*)malloc(sizeof(Service));
    if (service == NULL) {
        return NULL;
    }
    
    service->repo = repo;

    service->undoStack = createVector();
    service->redoStack = createVector();
    
    if (service->undoStack == NULL || service->redoStack == NULL) {
        destroyVector(service->undoStack, destroyOperation);
        destroyVector(service->redoStack, destroyOperation);
        free(service);
        return NULL;
    }
    
    return service;
}

void destroyService(Service* service) {
    if (service != NULL) {

        destroyVector(service->undoStack, destroyOperation);
        destroyVector(service->redoStack, destroyOperation);
        
        free(service);
    }
}

Operation* createOperation(const char* type, Material* material, Material* newMaterial, int index) {
    if (type == NULL) {
        return NULL;
    }
    
    Operation* op = (Operation*)malloc(sizeof(Operation));
    if (op == NULL) {
        return NULL;
    }

    op->type = (char*)malloc(strlen(type) + 1);
    if (op->type == NULL) {
        free(op);
        return NULL;
    }
    strcpy(op->type, type);

    op->material = material;
    op->newMaterial = newMaterial;
    op->index = index;
    
    return op;
}


void clearRedoStack(Service* service) {
    if (service == NULL) {
        return;
    }
    
    destroyVector(service->redoStack, destroyOperation);
    service->redoStack = createVector();
    // Check if creation succeeded
    if (service->redoStack == NULL) {
        fprintf(stderr, "Failed to create new redo stack\n");
        // Handle error appropriately
    }
}

int addMaterialService(Service* service, const char* name, const char* supplier, 
                       int quantity, time_t expirationDate) {
    if (service == NULL || name == NULL || supplier == NULL || quantity <= 0) {
        return 0;
    }

    Material* material = createMaterial(name, supplier, quantity, expirationDate);
    if (material == NULL) {
        return 0;
    }

    int existingIndex = findMaterial(service->repo, name, supplier, expirationDate);
    Material* oldMaterial = NULL;
    
    if (existingIndex != -1) {

        oldMaterial = copyMaterial(getMaterialByIndex(service->repo, existingIndex));
    }
    

    int result = addMaterial(service->repo, material);
    
    if (result) {
        // Record the operation for undo
        Operation* op = createOperation("add", oldMaterial, copyMaterial(material), existingIndex);
        if (op != NULL) {
            addToVector(service->undoStack, op);
            clearRedoStack(service);
        }
    } else if (oldMaterial != NULL) {
        // Free the old material copy if the operation failed
        destroyMaterial(oldMaterial);
    }
    
    return result;
}

int deleteMaterialService(Service* service, const char* name, const char* supplier, 
                         time_t expirationDate) {
    if (service == NULL || name == NULL || supplier == NULL) {
        return 0;
    }
    
    // Find the material
    int index = findMaterial(service->repo, name, supplier, expirationDate);
    if (index == -1) {
        return 0; // Material not found
    }
    
    // Create a copy for the undo operation
    Material* oldMaterial = copyMaterial(getMaterialByIndex(service->repo, index));
    
    // Delete the material
    int result = deleteMaterialByIndex(service->repo, index);
    
    if (result) {
        // Record the operation for undo
        Operation* op = createOperation("delete", oldMaterial, NULL, index);
        if (op != NULL) {
            addToVector(service->undoStack, op);
            clearRedoStack(service);
        }
    } else if (oldMaterial != NULL) {
        // Free the old material copy if the operation failed
        destroyMaterial(oldMaterial);
    }
    
    return result;
}

int updateMaterialService(Service* service, const char* name, const char* supplier, 
                         time_t expirationDate, int newQuantity) {
    if (service == NULL || name == NULL || supplier == NULL || newQuantity < 0) {
        return 0;
    }
    
    // Find the material
    int index = findMaterial(service->repo, name, supplier, expirationDate);
    if (index == -1) {
        return 0; // Material not found
    }
    
    // Get the old material
    Material* oldMaterial = getMaterialByIndex(service->repo, index);
    
    // Create new material with updated quantity
    Material* newMaterial = createMaterial(name, supplier, newQuantity, expirationDate);
    if (newMaterial == NULL) {
        return 0;
    }
    
    // Record the operation for undo (before updating)
    Operation* op = createOperation("update", copyMaterial(oldMaterial), copyMaterial(newMaterial), index);
    
    // Update the material
    int result = updateVector(service->repo->materials, index, newMaterial, freeMaterialHelper);

    if (result) {
        if (op != NULL) {
            addToVector(service->undoStack, op);
            clearRedoStack(service);
        }
    } else {
        // If update failed, free the new material and operation
        destroyMaterial(newMaterial);
        if (op != NULL) {
            destroyOperation(op);
        }
    }
    
    return result;
}

Vector* getAllMaterialsService(Service* service) {
    if (service == NULL) {
        return NULL;
    }
    
    return getAllMaterials(service->repo);
}

Vector* getExpiredMaterialsService(Service* service, const char* searchString) {
    if (service == NULL) {
        return NULL;
    }
    
    return getExpiredMaterials(service->repo, searchString);
}

Vector* getMaterialsInShortSupplyService(Service* service, const char* supplier, int threshold) {
    if (service == NULL || supplier == NULL || threshold <= 0) {
        return NULL;
    }
    
    return getMaterialsInShortSupply(service->repo, supplier, threshold);
}

int undo(Service* service) {
    if (service == NULL || getVectorSize(service->undoStack) == 0) {
        return 0; // Nothing to undo
    }
    
    // Get the last operation
    int lastIndex = getVectorSize(service->undoStack) - 1;
    Operation* op = (Operation*)getFromVector(service->undoStack, lastIndex);
    
    int result = 0;
    
    if (strcmp(op->type, "add") == 0) {
        // Undo an add operation
        if (op->material == NULL) {
            // It was a new material, just delete it
            result = deleteMaterialByIndex(service->repo, findMaterial(service->repo, 
                                          op->newMaterial->name, 
                                          op->newMaterial->supplier, 
                                          op->newMaterial->expirationDate));
        } else {
            // It was an update to existing material, restore the old one
            int index = findMaterial(service->repo, op->material->name, 
                                   op->material->supplier, 
                                   op->material->expirationDate);
            
            if (index != -1) {
                Material* old = getMaterialByIndex(service->repo, index);
                Material* restored = copyMaterial(op->material);
                
                result = updateVector(service->repo->materials, index, restored, freeMaterialHelper);
                if (!result) {
                    destroyMaterial(restored);
                } else {
                    destroyMaterial(old);
                }
            }
        }
    } else if (strcmp(op->type, "delete") == 0) {
        // Undo a delete operation - add the material back
        result = addMaterial(service->repo, copyMaterial(op->material));
    } else if (strcmp(op->type, "update") == 0) {
        // Undo an update operation - restore old value
        int index = findMaterial(service->repo, op->material->name,
                               op->material->supplier, 
                               op->material->expirationDate);
        
        if (index != -1) {
            Material* current = getMaterialByIndex(service->repo, index);
            Material* restored = copyMaterial(op->material);
            
            result = updateVector(service->repo->materials, index, restored, freeMaterialHelper);
            if (!result) {
                destroyMaterial(restored);
            } else {
                destroyMaterial(current);
            }
        }
    }
    
    if (result) {
        addToVector(service->redoStack, op);
        // We're moving the operation to redoStack, not destroying it
        deleteFromVector(service->undoStack, lastIndex, NULL);
    }
    
    return result;
}

int redo(Service* service) {
    if (service == NULL || getVectorSize(service->redoStack) == 0) {
        return 0; // Nothing to redo
    }

    int lastIndex = getVectorSize(service->redoStack) - 1;
    Operation* op = (Operation*)getFromVector(service->redoStack, lastIndex);

    int result = 0;

    if (strcmp(op->type, "add") == 0) {
        if (op->material == NULL) {
            result = addMaterial(service->repo, copyMaterial(op->newMaterial));
        } else {
            int index = findMaterial(service->repo, op->newMaterial->name,
                                   op->newMaterial->supplier,
                                   op->newMaterial->expirationDate);

            if (index == -1) {
                result = addMaterial(service->repo, copyMaterial(op->newMaterial));
            } else {
                Material* current = getMaterialByIndex(service->repo, index);
                Material* updated = copyMaterial(op->newMaterial);

                result = updateVector(service->repo->materials, index, updated, freeMaterialHelper);
                if (!result) {
                    destroyMaterial(updated);
                } else {
                    destroyMaterial(current);
                }
            }
        }
    } else if (strcmp(op->type, "delete") == 0) {
        int index = findMaterial(service->repo, op->material->name,
                               op->material->supplier,
                               op->material->expirationDate);

        if (index != -1) {
            result = deleteMaterialByIndex(service->repo, index);
        }
    } else if (strcmp(op->type, "update") == 0) {
        int index = findMaterial(service->repo, op->newMaterial->name,
                               op->newMaterial->supplier,
                               op->newMaterial->expirationDate);
        if (index != -1) {
            Material* current = getMaterialByIndex(service->repo, index);
            Material* updated = copyMaterial(op->newMaterial);
            result = updateVector(service->repo->materials, index, updated, freeMaterialHelper);
            if (!result) {
                destroyMaterial(updated);
            } else {
                destroyMaterial(current);
            }
        }
    }

    if (result) {
        addToVector(service->undoStack, op);
        // We're moving the operation to undoStack, not destroying it
        deleteFromVector(service->redoStack, lastIndex, NULL);
    }

    return result;
}