#include "domain.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

Material* createMaterial(const char* name, const char* supplier, int quantity, time_t expirationDate) {
    Material* material = (Material*)malloc(sizeof(Material));
    if (material == NULL) {
        return NULL; // Memory allocation failed
    }
    material->name = (char*)malloc(strlen(name) + 1);
    material->supplier = (char*)malloc(strlen(supplier) + 1);
    if (material->name == NULL || material->supplier == NULL) {
        free(material->name);
        free(material->supplier);
        free(material);
        return NULL;
    }

    strcpy(material->name, name);
    strcpy(material->supplier, supplier);
    material->quantity = quantity;
    material->expirationDate = expirationDate;
    return material;
}

void destroyMaterial(Material* material) {
    if (material != NULL) {
        free(material->name);
        free(material->supplier);
        free(material);
    }
}

Material* copyMaterial(const Material* source) {
    if (source == NULL) {
        return NULL;
    }
    return createMaterial(source->name, source->supplier, source->quantity, source->expirationDate);
}

int areMaterialsEqual(const Material* m1, const Material* m2) {
    if (m1 == NULL || m2 == NULL) {
        return 0;
    }

    // if materials are the same
    return (strcmp(m1->name, m2->name) == 0 &&
            strcmp(m1->supplier, m2->supplier) == 0 &&
            m1->expirationDate == m2->expirationDate);
}

char* materialToString(const Material* material) {
    if (material == NULL) {
        return NULL;
    }
    char dateStr[26];
    struct tm* tm_info = localtime(&material->expirationDate);
    strftime(dateStr, 26, "%Y-%m-%d", tm_info);
    char* result = (char*)malloc(strlen(material->name) +
                                strlen(material->supplier) +
                                strlen(dateStr) + 50);

    if (result == NULL) {
        return NULL;
    }
    sprintf(result, "Name: %s, Supplier: %s, Quantity: %d, Expires: %s",
            material->name, material->supplier, material->quantity, dateStr);

    return result;
}