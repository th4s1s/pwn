#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char real_flag[64];
char* fake_flag = "CSIKB{y0u_w0nT_G3t_7h3_fL@g_tH15_7im3}";

void get_flag()
{
    FILE *f = fopen("flag.txt", "r");
    if(f == NULL)
    {
        printf("flag.txt not found!\n");
        exit(0);
    }
    fgets(real_flag, 64, f);
}

void main() {
    setbuf(stdin, 0);
    get_flag();

    FILE *fp;
    char buf[32];
    char* fake_flag_local;
    fp = fopen("/dev/null", "wb");

    puts("Hello this is the hotline of BKISC. What can I help you with?");
    puts("Since I'm a very busy person so make your problem short.");
    printf("> ");
    fgets(buf, 6, stdin);

    if(!strcmp(buf, "flag\n")) {
        puts("I see so you're one of those who came here for the flag am I right?");
        puts("Actually I have one right here...");
        get_flag();
        fake_flag_local = fake_flag;
        puts("But unfortunately since you're not our VIP, I can't give you the flag.");
    }
    else printf("I see so you're having a problem with %s", buf);

    printf("Enter your message here and I'll send it to the customer support: ");
    fgets(buf, 32, stdin);

    fprintf(fp, buf);
    puts("Sorry I just yeeted your message to the void.");
    printf("Lucky for you since I made a copy of it, you can have your message back: %s\n", buf);
    puts("Now go away!!!");
}