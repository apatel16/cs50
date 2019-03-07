#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>
#include<string.h>
#include<cs50.h>

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        printf("Usage: ./vigenere <key>\n");
        return 1;
    }

    string key = argv[1];
    for (int i = 0; i < strlen(key); i++)
    {
        if (!isalpha(key[i]))
        {
            return 1;
        }
    }

    string plaintext = get_string("plaintext:   ");
    int length = strlen(plaintext);
    int keylength = strlen(key);

    printf("ciphertext: ");
    int j = 0;
    for (int i = 0; i < length; i++)
    {
        char c = plaintext[i];
        int tempkey;
        if (isupper(key[j]))
        {
            tempkey = key[j] - 65;
        }
        else
        {
            tempkey = key[j] - 97;
        }
        if (isalpha(c))
        {
            if (isupper(c))
            {
                int a = ((plaintext[i] - 65) + tempkey) % 26;       // caesar formula
                c = a + 65;
            }
            else if (islower(c))
            {
                int a = ((plaintext[i] - 97) + tempkey) % 26;       // caesar formula
                c = a + 97;
            }
            j = (j + 1) % keylength;
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