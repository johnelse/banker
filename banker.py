#!/usr/bin/env python

import banker_frontend

import snack

if __name__ == "__main__":
    try:
        screen = snack.SnackScreen()
        banker_frontend.main(screen)
    finally:
        screen.finish()
    
