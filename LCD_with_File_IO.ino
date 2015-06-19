
#include <Wire.h>
#include "rgb_lcd.h"
#include <string>
#include <iostream>
#include <fstream>
#include <sys/fcntl.h>
rgb_lcd lcd;
using namespace std;
void setup()
{
    // set up the LCD's number of columns and rows:
    lcd.begin(16, 2);
}



void loop()
{
    char * text = 0;
    long length;
    char str[17];
    int fd;
    struct flock lock;
    fd = open ("output.txt", O_RDONLY);
    FILE * f = fopen ("output.txt", "r");
    memset (&lock, 0, sizeof(lock));
    lock.l_type = F_RDLCK;
    fcntl (fd, F_SETLKW, &lock);
    if (f)
    {
      fseek (f, 0, SEEK_END);
//      length = ftell (f);
      fseek (f, 0, SEEK_SET);
      char text[1000];
      if (text)
      {
        fread (text, 1, length, f);
      }
      lock.l_type = F_UNLCK;
      fcntl (fd, F_SETLKW, &lock);
    }
    
    lcd.setCursor (16, 1);
    lcd.autoscroll ();
    for (int i = 0; i < 16; i++) {
      lcd.print (text[i]);
      delay(250);
    }
    lcd.noAutoscroll ();
    lcd.clear ();
    
    for (int i = 0; i < length - 16; i++) {
      lcd.setCursor (0, 1);
      strncpy (str, text + i, 16);
      lcd.print (str);
      delay (250);
    }
    for (int i = 0; i < 16; i++) {
      lcd.scrollDisplayLeft ();
      delay (250);
    }
    
}


/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
