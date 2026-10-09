cmake_minimum_required(VERSION 3.16)
project(a2-cezzz12-1 C)

set(CMAKE_C_STANDARD 11)

add_executable(a2-cezzz12-1 main.c
        service.c
        vector.c
        repository.c
        domain.c
        ui.c

)
enable_testing()
add_executable(material_tests test.c domain.c vector.c repository.c service.c)
add_test(NAME material_tests COMMAND material_tests)
