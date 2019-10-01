#include <stdio.h>
#include <stdlib.h>

int main(){
    printf("ready");
    char* buffer;
    size_t buffer_length = 8;

    if((buffer = (char *)malloc(buffer_length * sizeof(char))) < 0){
        perror("Malloc Error:");
        exit(EXIT_FAILURE);
    }
    
    printf("ready");
    
    if(getline(&buffer,&buffer_length,stdin) < 0){
        perror("Stdin Read Error:");
        exit(EXIT_FAILURE);
    }

    int grid_length = atoi(buffer); //works in this case but be careful with this
    free(buffer);
    
    while(1 == 1){
        printf("ready");
        printf("forward");
    }
}
