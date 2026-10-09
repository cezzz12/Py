#include "ui.h"
#include "service.h"
#include "domain.h"
#include "vector.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_STRING_LENGTH 100

UI* createUI(Service* service) {
    if (service == NULL) {
        return NULL;
    }
    
    UI* ui = (UI*)malloc(sizeof(UI));
    if (ui == NULL) {
        return NULL;
    }
    
    ui->service = service;
    return ui;
}

void destroyUI(UI* ui) {
    if (ui != NULL) {
        free(ui);
    }
}

void displayMenu() {
    printf("1. Add material\n");
    printf("2. Delete material\n");
    printf("3. Update material quantity\n");
    printf("4. Display all materials\n");
    printf("5. Display expired materials\n");
    printf("6. Display materials in short supply\n");
    printf("7. Undo\n");
    printf("8. Redo\n");
    printf("0. Exit\n");
    printf("Enter your choice: ");
}


void destroyMaterialWrapper(void* material) {
    destroyMaterial((Material*)material);
}
time_t parseDate(const char* dateStr) {
    struct tm tm_info = {0};
    if (sscanf(dateStr, "%d-%d-%d", &tm_info.tm_year, &tm_info.tm_mon, &tm_info.tm_mday) != 3) {
        return (time_t)-1;
    }
    tm_info.tm_year -= 1900;
    tm_info.tm_mon -= 1;
    
    return mktime(&tm_info);
}

char* formatDate(time_t date) {
    char* dateStr = (char*)malloc(11); // YYYY-MM-DD + null terminator
    if (dateStr == NULL) {
        return NULL;
    }
    
    struct tm* tm_info = localtime(&date);
    strftime(dateStr, 11, "%Y-%m-%d", tm_info);
    
    return dateStr;
}

char* readLine() {
    char* line = (char*)malloc(MAX_STRING_LENGTH);
    if (line == NULL) {
        return NULL;
    }
    if (fgets(line, MAX_STRING_LENGTH, stdin) == NULL) {
        free(line);
        return NULL;
    }
    size_t len = strlen(line);
    if (len > 0 && line[len - 1] == '\n') {
        line[len - 1] = '\0';
    }
    
    return line;
}

void handleAddMaterial(UI* ui) {
    char name[MAX_STRING_LENGTH];
    char supplier[MAX_STRING_LENGTH];
    int quantity;
    char dateStr[MAX_STRING_LENGTH];
    printf("Enter material name: ");
    fgets(name, MAX_STRING_LENGTH, stdin);
    name[strcspn(name, "\n")] = '\0';  // Remove newline
    printf("Enter supplier: ");
    fgets(supplier, MAX_STRING_LENGTH, stdin);
    supplier[strcspn(supplier, "\n")] = '\0';  // Remove newline
    printf("Enter quantity: ");
    if (scanf("%d", &quantity) != 1 || quantity <= 0) {
        printf("Invalid quantity. Please enter a positive number.\n");
        while (getchar() != '\n');
        return;
    }
    while (getchar() != '\n');
    printf("Enter expiration date (YYYY-MM-DD): ");
    fgets(dateStr, MAX_STRING_LENGTH, stdin);
    dateStr[strcspn(dateStr, "\n")] = '\0';  // Remove newline
    time_t expirationDate = parseDate(dateStr);
    if (expirationDate == (time_t)-1) {
        printf("Invalid date format. Please use YYYY-MM-DD.\n");
        return;
    }
    if (addMaterialService(ui->service, name, supplier, quantity, expirationDate)) {
        printf("Material added successfully.\n");
    } else {
        printf("Failed to add material.\n");
    }
}

void handleDeleteMaterial(UI* ui) {
    char name[MAX_STRING_LENGTH];
    char supplier[MAX_STRING_LENGTH];
    char dateStr[MAX_STRING_LENGTH];
    printf("Enter material name: ");
    fgets(name, MAX_STRING_LENGTH, stdin);
    name[strcspn(name, "\n")] = '\0';  // Remove newline
    printf("Enter supplier: ");
    fgets(supplier, MAX_STRING_LENGTH, stdin);
    supplier[strcspn(supplier, "\n")] = '\0';  // Remove newline
    printf("Enter expiration date (YYYY-MM-DD): ");
    fgets(dateStr, MAX_STRING_LENGTH, stdin);
    dateStr[strcspn(dateStr, "\n")] = '\0';  // Remove newline
    time_t expirationDate = parseDate(dateStr);
    if (expirationDate == (time_t)-1) {
        printf("Invalid date format. Please use YYYY-MM-DD.\n");
        return;
    }
    if (deleteMaterialService(ui->service, name, supplier, expirationDate)) {
        printf("Material deleted successfully.\n");
    } else {
        printf("Failed to delete material. Material not found.\n");
    }
}

void handleUpdateMaterial(UI* ui) {
    char name[MAX_STRING_LENGTH];
    char supplier[MAX_STRING_LENGTH];
    char dateStr[MAX_STRING_LENGTH];
    int newQuantity;
    printf("Enter material name: ");
    fgets(name, MAX_STRING_LENGTH, stdin);
    name[strcspn(name, "\n")] = '\0';  // Remove newline
    printf("Enter supplier: ");
    fgets(supplier, MAX_STRING_LENGTH, stdin);
    supplier[strcspn(supplier, "\n")] = '\0';  // Remove newline
    printf("Enter expiration date (YYYY-MM-DD): ");
    fgets(dateStr, MAX_STRING_LENGTH, stdin);
    dateStr[strcspn(dateStr, "\n")] = '\0';  // Remove newline
    time_t expirationDate = parseDate(dateStr);
    if (expirationDate == (time_t)-1) {
        printf("Invalid date format. Please use YYYY-MM-DD.\n");
        return;
    }
    
    printf("Enter new quantity: ");
    if (scanf("%d", &newQuantity) != 1 || newQuantity < 0) {
        printf("Invalid quantity. Please enter a non-negative number.\n");
        while (getchar() != '\n');
        return;
    }
    while (getchar() != '\n');
    if (updateMaterialService(ui->service, name, supplier, expirationDate, newQuantity)) {
        printf("Material updated successfully.\n");
    } else {
        printf("Failed to update material. Material not found.\n");
    }
}

void printMaterials(Vector* materials) {
    if (materials == NULL || getVectorSize(materials) == 0) {
        printf("No materials found.\n");
        // Even if empty, we need to destroy the vector if it exists
        if (materials != NULL) {
            destroyVector(materials, destroyMaterialWrapper);
        }
        return;
    }
    printf("\n%-20s %-20s %-10s %-12s\n", "Name", "Supplier", "Quantity", "Expiration");
    printf("------------------------------------------------------------------\n");

    for (int i = 0; i < getVectorSize(materials); i++) {
        Material* material = (Material*)getFromVector(materials, i);

        char* dateStr = formatDate(material->expirationDate);

        printf("%-20s %-20s %-10d %-12s\n",
               material->name, material->supplier, material->quantity, dateStr);

        free(dateStr);
    }

    // Properly destroy the vector and its materials after printing
    destroyVector(materials, destroyMaterialWrapper);
}

void handleDisplayAllMaterials(UI* ui) {
    Vector* materials = getAllMaterialsService(ui->service);
    printf("\n=== All Materials ===\n");
    printMaterials(materials);
}

void handleDisplayExpiredMaterials(UI* ui) {
    char searchString[MAX_STRING_LENGTH];
    printf("Enter search string (or press Enter for all expired materials): ");
    fgets(searchString, MAX_STRING_LENGTH, stdin);
    searchString[strcspn(searchString, "\n")] = '\0';  // Remove newline
    Vector* materials = getExpiredMaterialsService(ui->service, searchString);
    printf("\n=== Expired Materials ===\n");
    printMaterials(materials);
}

void handleDisplayMaterialsInShortSupply(UI* ui) {
    char supplier[MAX_STRING_LENGTH];
    int threshold;
    printf("Enter supplier: ");
    fgets(supplier, MAX_STRING_LENGTH, stdin);
    supplier[strcspn(supplier, "\n")] = '\0';  // Remove newline
    printf("Enter quantity threshold: ");
    if (scanf("%d", &threshold) != 1 || threshold <= 0) {
        printf("Invalid threshold. Please enter a positive number.\n");
        while (getchar() != '\n');
        return;
    }
    while (getchar() != '\n');
    Vector* materials = getMaterialsInShortSupplyService(ui->service, supplier, threshold);
    printf("\n=== Materials in Short Supply from %s (Below %d) ===\n", supplier, threshold);
    printMaterials(materials);
}

void handleUndo(UI* ui) {
    if (undo(ui->service)) {
        printf("Undo successful.\n");
    } else {
        printf("Nothing to undo.\n");
    }
}

void handleRedo(UI* ui) {
    if (redo(ui->service)) {
        printf("Redo successful.\n");
    } else {
        printf("Nothing to redo.\n");
    }
}

void runUI(UI* ui) {
    int choice;
    int running = 1;
    
    while (running) {
        displayMenu();
        
        if (scanf("%d", &choice) != 1) {
            printf("Invalid choice. Please enter a number.\n");
            while (getchar() != '\n');
            continue;
        }
        while (getchar() != '\n');
        
        switch (choice) {
            case 1:
                handleAddMaterial(ui);
                break;
            case 2:
                handleDeleteMaterial(ui);
                break;
            case 3:
                handleUpdateMaterial(ui);
                break;
            case 4:
                handleDisplayAllMaterials(ui);
                break;
            case 5:
                handleDisplayExpiredMaterials(ui);
                break;
            case 6:
                handleDisplayMaterialsInShortSupply(ui);
                break;
            case 7:
                handleUndo(ui);
                break;
            case 8:
                handleRedo(ui);
                break;
            case 0:
                running = 0;
                printf("Exiting program.\n");
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
}
