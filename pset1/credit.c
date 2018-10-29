#include<stdio.h>
#include<cs50.h>
#include<math.h>

int main(){
    long long cc_number = 0;    //store credit card number
    int digit = 0;              //store last digit

    int first_digit=0;          //first two digit of credit card (for card company validation)

    //Some temporary variables
    long long temp = 0;
    long long temp3 = 0;
    int sum1 = 0;
    int sum2 = 0;
    int i=0;

    //Input credit card from user
    do{
        printf("Enter credit card number: ");
        cc_number = get_long_long();
    }while(!cc_number);

    temp = cc_number;

    while(temp != 0){

        digit = temp % 10; // 7
        temp = temp / 10;  // 3

        if(i%2 == 0 ){
            sum2 = sum2 + digit;
        }else{
            int temp2 = digit * 2;
            if(temp2 < 10){
                sum1 = sum1 + temp2;
            }else{
                sum1 = sum1 + (temp2 % 10) + (temp2 / 10);
            }
        }
        i++;
    }//End While

    //Check Checksum (Last digit should be 0)
    if((sum1 + sum2) % 2 != 0){
        printf("Invalid credit card number.\n");
        return 1;
    }

    temp3 = pow(10, (i-2));
    first_digit = cc_number / temp3;

    //Amex check
    if(i == 15){
        if(first_digit == 34 || first_digit == 37){
            printf("Valid AMEX credit card.\n");
            return 0;
        }
    }

    //Master Card Check
    if(i == 16){
        if(first_digit == 51 ||
           first_digit == 52 ||
           first_digit == 53 ||
           first_digit == 54 ||
           first_digit == 55){
               printf("Valid master card found.\n");
               return 0;
        }
    }

    //Visa Check
    if(i == 13 || i==16){
        if(first_digit / 10 == 4){
            printf("Valid Visa card found.\n");
            return 0;
        }
    }

    printf("Valid card found but unknown brand!!!\n");
    return 0;
}


