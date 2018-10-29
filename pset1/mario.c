#include<stdio.h>
#include<stdlib.h>
#include<cs50.h>

int main(){

    //variable declarations
    int height= 0;
    int spaces = 0;
    int hashes = 0;
    int i=0, j=0, k=0;

    // validate input (No string validation)
    do{
        height = get_int("Enter height: ");
    }while(height < 0 || height > 23 );

    // create mario mountain
    for(i = 1; i <= height ; i++){

        spaces = height - i;
        for(j=0; j<spaces; j++){
            printf(" ");
        }

        hashes = height - spaces + 1;
        for(k=0; k<hashes; k++){
            printf("#");
        }
        printf("\n");
    }
    return 0;
}
