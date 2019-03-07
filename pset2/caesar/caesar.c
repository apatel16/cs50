#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>
#include<string.h>
#include<cs50.h>

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        printf("Usage: ./caesar <key>\n");
        return 1;
    }

    int key = atoi(argv[1]);
    if (key < 1)
    {
        printf("Key error\n");
        return 1;
    }

    string plaintext = get_string("plaintext:   ");
    int length = strlen(plaintext);

    printf("ciphertext:  ");
    for (int i = 0; i < length; i++)
    {
        char c = plaintext[i];
        if (isalpha(c))
        {
            if (isupper(c))
            {
                int a = ((plaintext[i] - 65) + key) % 26;       // caesar formula
                c = a + 65;
            }
            else if (islower(c))
            {
                int a = ((plaintext[i] - 97) + key) % 26;       // caesar formula
                c = a + 97;
            }
        }
        else
        {
            c = plaintext[i];
        }
        printf("%c", c);
    }
    printf("\n");

    return 0;
}