#include <time.h>
#include <stdio.h>

char* timestamp_to_date(time_t a1)
{
  time_t timer; // [rsp+8h] [rbp-18h] BYREF
  char *s; // [rsp+10h] [rbp-10h]
  struct tm *tp; // [rsp+18h] [rbp-8h]

  timer = a1;
  s = (char *)malloc(0x20uLL);
  tp = localtime(&timer);
  if ( !tp )
  {
    puts("[-] Error converting the UNIX timestamp to a date and time");
    exit(1);
  }
  strftime(s, 0x20uLL, "%Y-%m-%d %H:%M:%S", tp);
  fflush(stdout);
  return s;
}

void main()
{
    char *v3;
    v3 = timestamp_to_date(4199222);
    printf("%s\n", v3);
}