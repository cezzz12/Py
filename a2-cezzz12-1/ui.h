#ifndef UI_H
#define UI_H

#include "service.h"

typedef struct {
    Service* service;
} UI;

UI* createUI(Service* service);
void destroyUI(UI* ui);
void runUI(UI* ui);
void displayMenu();
void handleAddMaterial(UI* ui);
void handleDeleteMaterial(UI* ui);
void handleUpdateMaterial(UI* ui);
void handleDisplayAllMaterials(UI* ui);
void handleDisplayExpiredMaterials(UI* ui);
void handleDisplayMaterialsInShortSupply(UI* ui);
void handleUndo(UI* ui);
void handleRedo(UI* ui);
void printMaterials(Vector* materials);
time_t parseDate(const char* dateStr);
char* formatDate(time_t date);

#endif