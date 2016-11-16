// https://sourceforge.net/p/predef/wiki/Compilers/

#include <stdio.h>

int main()
{
  printf("Hello world!\n");


#ifdef NDEBUG
  printf("This is a release build.\n");
#else
  printf("This is a debug build.\n");
#endif


#if defined(__MINW64__) 
  printf("This build was compiled using MinGW64.\n");
#elif defined(__MINW32__) 
  printf("This build was compiled using MinGW32.\n");
#elif defined(__GNUC__)
  printf("This build was compiled using gcc.\n");
#elif defined(__clang__)
  printf("This build was compiled using clang.\n");
#elif defined(_MSC_VER)
  printf("This build was compiled using Microsoft Visual Studio version %04d.\n", _MSC_VER);
#else
  printf("WARNING: Unknown compiler.\n");
#endif


  return 0;
}
