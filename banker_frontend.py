import banker_db
import snack

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

States = Enum(["CHOOSE_ACTION", "CHOOSE_YEAR", "CHOOSE_MONTH",
    "DISPLAY_STATEMENT", "ADD_TRANSACTION"])

# Actions which can be carried out from the top-level menu.
Actions = Enum(["VIEW_STATEMENTS", "ADD_TRANSACTION", "EXIT"])

def make_listbox(height, items):
    listbox = snack.Listbox(height, returnExit=1, scroll=1)
    for index, item in enumerate(items):
        listbox.append(str(item), index)
    return listbox

# Return a choice from the list of items.
def get_choice(screen, items):
    listbox = make_listbox(20, items)
    grid = snack.GridForm(screen, "Banker", 1, 1)
    grid.add(listbox, 0, 0)
    grid.runOnce()
    return items[listbox.current()]

# Return a choice from the list of items,
# or None if the user chooses the "Back" choice.
def get_choice_or_back(screen, items):
    items = items + ["Back"]
    choice = get_choice(screen, items)
    if choice == "Back":
        return None
    return choice

# Choose from the months in the chosen year which have one or more transactions.
def choose_month(conn, screen, year):
    months = banker_db.get_months(conn, year)
    month = get_choice_or_back(screen, months)
    return month

# Choose from all the years in the database which have transactions.
def choose_year(conn, screen):
    years = banker_db.get_years(conn)
    year = get_choice_or_back(screen, years)
    return year

# Display a list of transactions for the chosen year and month.
def display_statement(conn, screen, year, month):
    transactions = banker_db.get_transactions(conn, year, month)
    transaction_strings =\
        map(lambda t: "%2d %30s %10.2f" %\
            (t.day, t.name, float(t.amount) / 100), transactions)
    get_choice(screen, transaction_strings)

# Choose a top-level action to perform.
def choose_action(conn, screen):
    actions = [Actions.VIEW_STATEMENTS, Actions.ADD_TRANSACTION, Actions.EXIT]
    action = get_choice(screen, actions)
    return action

# Set up initial state, then start the main loop.
def main(screen, conn):
    state = States.CHOOSE_ACTION
    running = True
    year = None
    month = None
    while running:
        if state == States.CHOOSE_ACTION:
            action = choose_action(conn, screen)
            if action == Actions.VIEW_STATEMENTS:
                state = States.CHOOSE_YEAR
            elif action == Actions.ADD_TRANSACTION:
                state = States.ADD_TRANSACTION
            elif action == Actions.EXIT:
                running = False
        elif state ==  States.CHOOSE_YEAR:
            year = choose_year(conn, screen)
            if year:
                state = States.CHOOSE_MONTH
            else:
                state = States.CHOOSE_ACTION
        elif state == States.CHOOSE_MONTH:
            month = choose_month(conn, screen, year)
            if month:
                state = States.DISPLAY_STATEMENT
            else:
                state = States.CHOOSE_YEAR
        elif state == States.DISPLAY_STATEMENT:
            display_statement(conn, screen, year, month)
            state = States.CHOOSE_MONTH
        elif state == States.ADD_TRANSACTION:
            running = False
