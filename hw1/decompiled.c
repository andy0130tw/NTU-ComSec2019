undefined4 main(undefined1 param_1)

{
  int iVar1;
  HMODULE pHVar2;
  int *piVar3;
  char *guarderStatus;
  size_t sVar4;
  int in_FS_OFFSET;
  undefined4 local_3c;
  int idx;
  int i;
  uint local_14;

  preprocess();
  pHVar2 = GetModuleHandleA((LPCSTR)0x0);
  piVar3 = (int *)((int)&pHVar2->unused + pHVar2[0xf].unused);
  iVar1 = *(int *)(in_FS_OFFSET + 0x30);
  if ((*(short *)&pHVar2->unused == 0x5a4d) && (*piVar3 == 0x4550)) {
    printf(
          " --------------------------- \n | B@ck t0 7he Fu7ur3...  \n |en.wikipedia.org/wiki/Back_to_the_Future\n  --------------------------- \n"
          );
    fullyear = getFullYear(CONCAT44(local_3c,piVar3[2]));
    printf("[+] It\'s a time machine built in 1985, \n\tand you\'re in %i year now.\n",fullyear);
    if (fullyear != 0x7c1) {
      puts("[!] WARNING: \n\tit might be some trouble if you\'re not in 1985 year.");
    }
    if (*(char *)(iVar1 + 2) == '\0') {
      guarderStatus = "[SAFE]";
    }
    else {
      guarderStatus = "[HARMFUL!]";
    }
    printf("[!] Time Machine Guarder: %s\n",guarderStatus);
    printf("[+] input password to launch time machine: ");
    gets(&user_inp);
    local_14 = 0;
    while( true ) {
      sVar4 = strlen(&user_inp);
      if (sVar4 <= local_14) break;
      (&user_inp)[local_14] = (&user_inp)[local_14] | 0x20;
      local_14 = local_14 + 1;
    }
    printf("[!] reading ... the.... passw0r..d.....\n");
    i = 0;
    while (i < 0x13) {
      (&user_inp)[i] =
           (&user_inp)[i] ^ *(char *)(iVar1 + 2) + ((char)fullyear + '?') * '\x02' + 0x7fU;
      if ((&user_inp)[i] != (&guard)[i]) {
        puts("[!] oops... time machine g0t some trouble in the 0ld tim3... ");
        break;
      }
      i = i + 1;
    }
    idx = 0;
    while (idx < 0x13) {
      (&user_inp)[idx] = (&user_inp)[idx] ^ (&key)[idx];
      idx = idx + 1;
    }
    printf("[+] a flag found by time machine at %i:\n\t%s\n",fullyear,&user_inp);
  }
  else {
    puts("time machine broken, oohoho. please don\'t patch me ;)");
  }
  return 0;
}
