/* Scan-code set2 values checked against the locked NVBoard src/at_scancode.h.
 * Prefix/translation lives in software; hardware exposes raw byte FIFO entries. */
static int ps2_key(unsigned code,bool extended) {
  if(extended)switch(code){
    case 0x14:return AM_KEY_RCTRL;case 0x11:return AM_KEY_RALT;
    case 0x75:return AM_KEY_UP;case 0x72:return AM_KEY_DOWN;case 0x6b:return AM_KEY_LEFT;case 0x74:return AM_KEY_RIGHT;
    case 0x70:return AM_KEY_INSERT;case 0x71:return AM_KEY_DELETE;case 0x6c:return AM_KEY_HOME;case 0x69:return AM_KEY_END;
    case 0x7d:return AM_KEY_PAGEUP;case 0x7a:return AM_KEY_PAGEDOWN;default:return AM_KEY_NONE;
  }
  switch(code){
#define KEY(code,name) case code:return AM_KEY_##name
    KEY(0x76,ESCAPE);KEY(0x05,F1);KEY(0x06,F2);KEY(0x04,F3);KEY(0x0c,F4);KEY(0x03,F5);KEY(0x0b,F6);
    KEY(0x83,F7);KEY(0x0a,F8);KEY(0x01,F9);KEY(0x09,F10);KEY(0x78,F11);KEY(0x07,F12);
    KEY(0x0e,GRAVE);KEY(0x16,1);KEY(0x1e,2);KEY(0x26,3);KEY(0x25,4);KEY(0x2e,5);KEY(0x36,6);KEY(0x3d,7);KEY(0x3e,8);KEY(0x46,9);KEY(0x45,0);
    KEY(0x4e,MINUS);KEY(0x55,EQUALS);KEY(0x66,BACKSPACE);KEY(0x0d,TAB);
    KEY(0x15,Q);KEY(0x1d,W);KEY(0x24,E);KEY(0x2d,R);KEY(0x2c,T);KEY(0x35,Y);KEY(0x3c,U);KEY(0x43,I);KEY(0x44,O);KEY(0x4d,P);
    KEY(0x54,LEFTBRACKET);KEY(0x5b,RIGHTBRACKET);KEY(0x5d,BACKSLASH);KEY(0x58,CAPSLOCK);
    KEY(0x1c,A);KEY(0x1b,S);KEY(0x23,D);KEY(0x2b,F);KEY(0x34,G);KEY(0x33,H);KEY(0x3b,J);KEY(0x42,K);KEY(0x4b,L);
    KEY(0x4c,SEMICOLON);KEY(0x52,APOSTROPHE);KEY(0x5a,RETURN);KEY(0x12,LSHIFT);
    KEY(0x1a,Z);KEY(0x22,X);KEY(0x21,C);KEY(0x2a,V);KEY(0x32,B);KEY(0x31,N);KEY(0x3a,M);
    KEY(0x41,COMMA);KEY(0x49,PERIOD);KEY(0x4a,SLASH);KEY(0x59,RSHIFT);KEY(0x14,LCTRL);KEY(0x11,LALT);KEY(0x29,SPACE);
#undef KEY
    default:return AM_KEY_NONE;
  }
}
static void keyboard_read(AM_INPUT_KEYBRD_T *event) {
  static bool extended,release;static unsigned pause_remaining;
  *event=(AM_INPUT_KEYBRD_T){.keycode=AM_KEY_NONE,.keydown=false};
  for(;;){
    unsigned code=*(volatile uint8_t *)0x10011000u;
    if(!code)return;
    if(pause_remaining){pause_remaining--;continue;}
    if(code==0xe1){pause_remaining=7;extended=release=false;continue;}
    if(code==0xe0){extended=true;continue;}
    if(code==0xf0){release=true;continue;}
    int key=ps2_key(code,extended);bool down=!release;extended=release=false;
    if(key!=AM_KEY_NONE){event->keycode=key;event->keydown=down;return;}
  }
}
