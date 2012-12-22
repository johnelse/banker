#!/usr/bin/env python

import banker_ui

import snack

if __name__ == "__main__":
    try:
        screen = snack.SnackScreen()
        banker_ui.main(screen)
    finally:
        screen.finish()
    
