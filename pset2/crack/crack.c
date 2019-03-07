#define _XOPEN_SOURCE
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <cs50.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: crack <hash>\n");
        return 1;
    }

    string letters = "\0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    int length = 57;

    string hash = argv[1];

    char salt[3];
    salt[0] = hash[0];
    salt[1] = hash[1];
    salt[2] = '\0';

    char password[6] = "\0\0\0\0\0\0";

    for (int m = 0; m < length ; m++)
    {
        for (int l = 0; l < length ; l++)
        {
            for (int k = 0; k < length ; k++)
            {
                for (int j = 0; j < length ; j++)
                {
                    for (int i = 1; i < length ; i++)
                    {
                        password[0] = letters[i];
                        password[1] = letters[j];
                        password[2] = letters[k];
                        password[3] = letters[l];
                        password[4] = letters[m];

                        if (strcmp(crypt(password, salt), hash) == 0)
                        {
                            printf("%s\n", password);
                            return 0;
                        }
                    }
                }
            }
        }
    }

    printf("Password can not be cracked!\n");
    return 0;
}