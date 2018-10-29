#include<stdio.h>
#include<cs50.h>
#include<math.h>

int main(){

    int quarter = 25;
    int dime = 10;
    int nickel = 5;
    int cents = 0;

    float change;
    int number_of_quarters = 0;
    int number_of_dimes = 0;
    int number_of_nickels = 0;
    int number_of_pennies = 0;

    int leftover = 0;

    printf("O hai! ");
    do{
        change = get_float("How much change is owed? ");
    }while(change < 0.0);


    cents = change * 100;
    leftover = round(cents);


   number_of_quarters = leftover / quarter;
   leftover = leftover % quarter;

   number_of_dimes = leftover / dime;
   leftover = leftover % dime;

   number_of_nickels = leftover / nickel;
   leftover = leftover % nickel;

   number_of_pennies =  leftover;

   printf("Total coins used are %d qurters, %d dimes, %d nickels, %d pennies",  number_of_quarters, number_of_dimes, number_of_nickels, number_of_pennies);

    return 0;
}
