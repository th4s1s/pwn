#include <iostream>
#include <math.h>
#include <string>

using namespace std;

int main()
{
    string s = "h_bO}EcDOR+G)uh(jl,vL";
    int l = s.length();
    int mid = l >> 1;
    int fi = 16, se = 24;
    string re = "";
    for(int i = 0; i < mid; i++)
    {
        re += (s[i] ^ fi);
    }
    for(int i = mid; i < l; i++)
    {
        re += (s[i] ^ se);
    }
    cout << re;
}