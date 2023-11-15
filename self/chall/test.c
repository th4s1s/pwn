#include <stdio.h>
#include <stdlib.h>


char* msg = "Thank you for reaching out to us. Our support team is currently unavailable, but we'll get back to you as soon as possible.";

void get_msg()
{
    setbuf(stdin, 0);
    char* feed_back = msg;
    char** auto_response = &feed_back;
    char *buffer = malloc(40);
    FILE *fp = fopen("/dev/null", "w");

    if(fp) {
        printf("> ");
        fgets(buffer, 0x20, stdin);
        fprintf(fp, buffer);
        puts(*auto_response);
    }
    else {
        return;
    }
}

void main() {
    puts("Well come to BKISC customer service.");
    puts("Give me your request and I'll what what I can do.");
    get_msg();
    puts("Your message will be in the waiting queue, never to be read.");
}