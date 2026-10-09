//
// Created by Cezar on 18.03.2025.
//
#include "ui.h"
#include "vector.h"
#include "domain.h"
#include "service.h"
#include "repository.h"

#include <stdlib.h>
#include <stdio.h>

int main() {
    // create repository
    Repository* repo = createRepository();
    if (repo == NULL) {
        fprintf(stderr, "Error creating repository\n");
        return 1;
    }

    // initialize with sample data
    initializeRepository(repo);

    // create service
    Service* service = createService(repo);
    if (service == NULL) {
        fprintf(stderr, "Error creating service\n");
        destroyRepository(repo);
        return 1;
    }

    // create UI
    UI* ui = createUI(service);
    if (ui == NULL) {
        fprintf(stderr, "Error creating UI\n");
        destroyService(service);
        destroyRepository(repo);
        return 1;
    }
    runUI(ui);

    // cleanup
    destroyUI(ui);
    destroyService(service);
    destroyRepository(repo);

    return 0;
}