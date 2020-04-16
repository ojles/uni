#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fts.h>


#define ERR_INVALID_USAGE 1
#define ERR_PARAM_NOT_DIR 2


int has_cpp_extension(char* fileName) {
    int lastIndex = 0;
    while (fileName[lastIndex] != '\0') {
        lastIndex++;
    }
    lastIndex--;

    if (lastIndex < 4) {
        return -1;
    }

    return fileName[lastIndex]        - 'p'
            + fileName[lastIndex - 1] - 'p'
            + fileName[lastIndex - 2] - 'c'
            + fileName[lastIndex - 3] - '.';
}

int main(int argc, char** argv) {
    if (argc >= 2 && strcmp(argv[1], "-h") == 0) {
        printf("Usage: copy-cpp SOURCE_DIR DESTINATION_DIR\n");
        printf("Move all .cpp files in subdirectories of SOURCE_DIR to DESTINATION_DIR\n");
        return 0;
    }

    if (argc < 3) {
        fprintf(stderr, "Invalid number of parameters!\n");
        fprintf(stderr, "Try 'copy-cpp -h' for more information.\n");
        return ERR_INVALID_USAGE;
    }

    DIR* firstDir = opendir(argv[1]);
    DIR* secondDir = opendir(argv[2]);

    if (firstDir == NULL) {
        fprintf(stderr, "First parameters is not a directory!\n");
        closedir(secondDir);
        return ERR_PARAM_NOT_DIR;
    }
    if (secondDir == NULL) {
        fprintf(stderr, "Second parameters is not a directory!\n");
        closedir(firstDir);
        return ERR_PARAM_NOT_DIR;
    }

    FTS* fileSystem = fts_open(&argv[1], FTS_NOCHDIR | FTS_COMFOLLOW, NULL);
    FTSENT* firstEntry = fts_read(fileSystem);
    FTSENT* entry = firstEntry;

    if (entry == NULL) {
        return 0;
    }

    const unsigned long destinationFolderNameLength = strlen(argv[2]);
    do
    {
        if ((entry->fts_statp->st_mode & S_IFMT) == S_IFREG && entry->fts_parent != firstEntry) {
            if (has_cpp_extension(entry->fts_path) == 0) {
                char* destinationPath = (char*) malloc(sizeof(char) * (destinationFolderNameLength * strlen(entry->fts_name) + 1));
                sprintf(destinationPath, "%s/%s", argv[2], entry->fts_name);
                rename(entry->fts_path, destinationPath);
                free(destinationPath);
            }
        }
        entry = fts_read(fileSystem);
    }
    while(entry != NULL && entry != firstEntry);

    closedir(firstDir);
    closedir(secondDir);

    return 0;
}
