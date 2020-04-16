#include <stdio.h>
#include <fts.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <stdlib.h>
#include <string.h>


#define ERR_INVALID_PARAM_NUMBER 1
#define ERR_PARAM_NOT_DIR 2


struct FileInfo {
    char path[256];
    int lineCount;
    int charsCount;
};

struct FileInfo findFileInfo(FILE* file) {
    struct FileInfo fileInfo;
    fileInfo.path[0] = '\0';
    fileInfo.lineCount = 0;
    fileInfo.charsCount = 0;
    for (char c = getc(file); c != EOF; c = getc(file)) {
        if (c == '\n') {
            fileInfo.lineCount++;
        }
        fileInfo.charsCount++;
    }
    return fileInfo;
}

struct FileInfo* searchForMostLinesFileAndMostCharsFile(char* const* directory) {
    // firts file is the file with most lines
    // the second file has the most characters
    struct FileInfo* files = malloc(sizeof(struct FileInfo) * 2);

    FTS* fileSystem = fts_open(directory, FTS_NOCHDIR | FTS_COMFOLLOW, NULL);
    FTSENT* firstEntry = fts_read(fileSystem);
    FTSENT* entry = firstEntry;

    if (entry == NULL) {
        return NULL;
    }

    do
    {
        if ((entry->fts_statp->st_mode & S_IFMT) == S_IFREG) {
            FILE* file = fopen(entry->fts_path, "r");
            struct FileInfo fileInfo = findFileInfo(file);
            if (fileInfo.lineCount > files[0].lineCount) {
                strcpy(files[0].path, entry->fts_accpath);
                files[0].lineCount = fileInfo.lineCount;
            }
            if (fileInfo.charsCount > files[1].charsCount) {
                strcpy(files[1].path, entry->fts_accpath);
                files[1].charsCount = fileInfo.charsCount;
            }
            fclose(file);
        }
        entry = fts_read(fileSystem);
    }
    while(entry != NULL && entry != firstEntry);

    return files;
}

int main(int argc, char** argv) {
    if (argc >= 2 && strcmp(argv[1], "-h") == 0) {
        printf("Usage: search-files DIRECTORY\n");
        printf("Searches for files with most lines and most characters\n");
        return 0;
    }

    if (argc != 2) {
        fprintf(stderr, "Invalid number of parameters!\n");
        fprintf(stderr, "Try search-files -h' for more information.\n");
        return ERR_INVALID_PARAM_NUMBER;
    }

    DIR* searchDir = opendir(argv[1]);

    if (searchDir == NULL) {
        fprintf(stderr, "'%s' is not directory!", argv[1]);
        return ERR_PARAM_NOT_DIR;
    }

    struct FileInfo* files = searchForMostLinesFileAndMostCharsFile(&argv[1]);
    if (files == NULL || files[0].path[0] == '\0') {
        printf("No files found.\n");
    } else {
        printf("Most lines: %d %s\n", files[0].lineCount, files[0].path);
        printf("Most chars: %d %s\n", files[1].charsCount, files[1].path);
    }

    closedir(searchDir);

    return 0;
}
