#include "BigInt.hpp"
#include <random>

using namespace std; 

class primeGen{
    public: 
    
    static BigInt fastExp(BigInt base, BigInt exponent, BigInt modulus) {
        BigInt result = 1;
        base = base % modulus; // Update base to be within modulus (if it's large)

        while (exponent > 0) {
            // If the exponent is odd, multiply the result by the current base value
            if (exponent % 2 == 1) {
                result = (result * base) % modulus;
            }

            // Square the base and reduce the exponent by half
            base = (base * base) % modulus;
            exponent /= 2;
        }

    return result;
}

static bool MillerRabin(BigInt x, int iterations = 5) {
    if (x < 2) {
        return false;
    }
    if (x != 2 && x % 2 == 0) {
        return false;
    }
    BigInt s = x - 1;
    while (s % 2 == 0) {
        s /= 2;
    }

    // Seed the random number generator

    for (int i = 0; i < iterations; i++) {
        double random = rand();
        BigInt a = (x-2) * rand() + 2;
        BigInt temp = s;
        BigInt mod = fastExp(a, temp, x);
        while (temp != x - 1 && mod != 1 && mod != x - 1) {
            mod = (mod * mod) % x;
            temp *= 2;
        }
        if (mod != x - 1 && temp % 2 == 0) {
            return false;
        }
    }
    return true;
}



};

int main(){
    BigInt big1; 
    big1 = "11376747235397"; 
    bool x = false; 
    BigInt big2; 
    size_t len1 = 100 - (15.0 * rand())/RAND_MAX - 40;
    size_t len2 = 40 +  ((15.0 * rand())/RAND_MAX); 
    while(!x){
        big2 = big_random(len1);
        if(big2 % 5 != 0 && big2 % 2 != 0){
            x = primeGen::MillerRabin(big2,1);
        }
    }
    x = false; 
    while(!x){
        big1 = big_random(len2);
        if(big1 % 5 != 0 && big1 % 2 != 0){
            x = primeGen::MillerRabin(big1,1);
        }
    }
    cout<<big2<<endl;
    cout<<big1<<endl;
}