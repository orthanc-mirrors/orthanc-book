// https://sourceforge.net/p/predef/wiki/Compilers/

#include <stdio.h>

int main()
{
  printf("\nHello world!\n\n");

#ifdef NDEBUG
  printf("This is a release build.\n");
#else
  printf("This is a debug build.\n");
#endif

#if defined(__MINGW64__) 
  printf("This build was compiled using MinGW64.\n");
#elif defined(__MINGW32__) 
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


#if defined(_WIN64)
  printf("Running under Windows 64bit.\n");
#elif defined(_WIN32)
  printf("Running under Windows 32bit.\n");
#elif defined(__linux__)
  printf("Running under Linux.\n");
#elif defined(__APPLE__) && defined(__MACH__)
  printf("Running under Apple OS X.\n");
#else
  printf("WARNING: Unknown operating system.\n");
#endif


  printf("\n");

  return 0;
}
