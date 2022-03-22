#define _GNU_SOURCE
#define _XOPEN_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <dlfcn.h>
// Name: Ryan Coslove
// netID: rmc326
// RUID: 185002462

// your code for time() goes here

int test = 0;
time_t time(time_t* tloc){
    if( test == 0 ){
        // creating tm struct
        struct tm tm;
        memset(&tm, 0, sizeof(struct tm));
	
        if( strptime("2021-6-03 12:00:00", "%Y-%m-%d %H:%M:%S", &tm) == NULL ){
            return 0; //didn't get struct
        }
        if(tloc == NULL){
            tloc = (time_t*) malloc(sizeof(time_t));
        }
        *tloc = mktime(&tm);
        test = 1; //finished 1 test
        return *tloc;
    }
    time_t (*new_time) (time_t* tloc);
    new_time = dlsym(RTLD_NEXT, "time");
    return new_time(tloc);

}
