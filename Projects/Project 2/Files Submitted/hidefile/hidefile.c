#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <dlfcn.h>
#include <string.h>

// Name: Ryan Coslove
// netID: rmc326
// RUID: 185002462
// your code for readdir goes here

// return array of file names
char** getFiles(char* env, int fileNum){
    // initialize array with fileNum indices
    char** fileNames = (char**) malloc(fileNum * sizeof(char*));

    int fileCounter = 0;
    int idx = 0;
    int strLen = 0;
 
    while( env[idx] != '\0' ){
        if( env[idx] == ':' ){
            fileNames[fileCounter] = (char*) malloc(sizeof(char) * (strLen+1));
            fileNames[fileCounter][strLen] = '\0';
            strLen = 0;
            idx += 1;
            fileCounter += 1;
        }else{
            strLen += 1;
            idx += 1;
        }
    }

    fileNames[fileCounter] = (char*) malloc(sizeof(char) * (strLen+1));
    fileNames[fileCounter][strLen] = '\0';

    // loop through copying names
    fileCounter = 0;
    idx = 0;
    int stringIdx = 0;

    while( env[idx] != '\0' ){
        if( env[idx] == ':' ){
            fileCounter += 1;
            stringIdx = 0;
            idx += 1;
        }else{
            fileNames[fileCounter][stringIdx] = env[idx];
            idx += 1;
            stringIdx += 1;
        }
    }    

    return fileNames;
}

// create array comparison
int strComp(char** fileNames,int fileNum,char* file){
    int counter = 0;
    for(counter = 0; counter < fileNum; counter++){
        if( strcmp(file, fileNames[counter]) == 0 )
            return 0;
    }
    return 1;
}

int numFiles(char* fileNames){
    int fileNum = 1;
    int counter = 0;
    while( fileNames[counter] != '\0' ){
        if( fileNames[counter] == ':' )
            fileNum += 1;
        counter += 1;
    }
    return fileNum;
}

struct dirent *readdir(DIR *dirp) {
    char* env = getenv("HIDDEN");
    int fileNum = numFiles(env);
    char** fileNames = getFiles(env, fileNum);

    // original readdir call
    struct dirent* (*new_readdir) (DIR* dirp);
    new_readdir = dlsym(RTLD_NEXT, "readdir");

    int fileExists = 0;
    struct dirent* curr = new_readdir(dirp);
    while( curr != NULL ){
        if( strComp(fileNames, fileNum, curr->d_name ) != 0 ){
            printf("%s\n",curr->d_name);
        }
        curr = new_readdir(dirp);
    }
}
