// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <ctype.h>
#include <string.h>
#include <stdio.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    int numerator = 48 - fraction[0];
    int denominator = 48 - fraction[2];

    int duration = (numerator * 8) / denominator;
    return duration;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    float frequency = 440.0;    //440hz is freq of A4 (standardized)

    char semitone = note[0];

    int isAccidental = 0;
    char accidental = '\0';
    int octave = 0;

    if (!isdigit(note[1]))
    {
        isAccidental = 1;
        accidental = note[1];
        octave = note[2] - 48;
    }
    else
    {
        octave = note[1] - 48;
    }

    // handling octaves
    float tempVal = 0.0;
    if (octave < 4)
    {
        tempVal = 4 - octave;
        frequency = frequency / pow(2.0, tempVal);
    }
    else if (octave == 4)
    {
        //Nothing to do
    }
    else
    {
        tempVal = octave - 4;
        frequency = frequency * pow(2.0, tempVal);
    }

    //Handling sharps and flats
    if (isAccidental)
    {
        if (accidental == '#')
        {
            frequency = frequency * pow(2.0, (1 / 12.0));
        }
        else
        {
            frequency = frequency / pow(2.0, (1 / 12.0));
        }
    }

    float n = 0.0;
    switch (semitone)
    {
        case 'A':
            n = 0;
            break;

        case 'B':
            n = 2;
            break;

        case 'C':
            n = 9;
            break;

        case 'D':
            n = 7;
            break;

        case 'E':
            n = 5;
            break;

        case 'F':
            n = 4;
            break;

        case 'G':
            n = 2;
            break;
    }

    if (semitone == 'B')
    {
        frequency = frequency * pow(2.0, (n / 12.0));
    }
    else
    {
        frequency = frequency / pow(2.0, (n / 12.0));
    }

    int newFreq = round(frequency);

    return newFreq;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (strlen(s) == 0)
    {
        return true;
    }
    return false;
}
