project(EmbeddedComputing_Lab01)

set(CMAKE_C_COMPILER "clang")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -std=c99 -fPIC")
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -g -O0")
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -O4 -DNDEBUG")

list(APPEND SOURCES "Lab01/main.c")
list(APPEND SOURCES "Lab01/merge.c")
list(APPEND SOURCES "Lab01/merge.h")
list(APPEND SOURCES "Lab01/quick.c")
list(APPEND SOURCES "Lab01/quick.h")
list(APPEND SOURCES "Lab01/radix.c")
list(APPEND SOURCES "Lab01/radix.h")

add_executable(${PROJECT_NAME} ${SOURCES})
