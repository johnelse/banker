import snack

def make_listbox(height, items):
    listbox = snack.Listbox(height, returnExit=1)
    for index, item in enumerate(items):
        listbox.append(item, index)
    return listbox

def main(screen):
    grid = snack.GridForm(screen, "Banker", 1, 1)
    listbox = make_listbox(20, ["Statements", "New transaction", "Exit"])
    grid.add(listbox, 0, 0)
    result = grid.runOnce()
