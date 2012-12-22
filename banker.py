#!/usr/bin/env python

import banker_db
import banker_frontend

import snack

if __name__ == "__main__":
    try:
        conn = banker_db.open_db()
        screen = snack.SnackScreen()
        banker_frontend.main(screen, conn)
    finally:
        screen.finish()
        conn.close()
    
