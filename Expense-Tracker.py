import argparse
import json
import datetime


def cargarJson() -> list:

    try:
        with open("expenses.json", "r") as archivo:
            data = json.load(archivo)
    except FileNotFoundError:
        data = []
        with open("expenses.json", "w") as archivo:
            json.dump(data, archivo, indent=4)
    except json.JSONDecodeError:
        print("⚠️ El archivo 'expenses.json' existe pero no tiene un formato JSON válido. Reiniciando...")
        data = []
        with open("expenses.json", "w") as archivo:
            json.dump(data, archivo, indent=4)

    return data

def getItemIndexById(id:int,data)->int| None:

    for index,item in enumerate(data):
            if item["id"]==id:
                return index
    return None
 

def guardarJson(data):
    try:
        with open("expenses.json", "w") as archivo:
            json.dump(data, archivo, indent=4)
        
    except Exception as e:
        print(f"Ocurrio un error al guardar la informacion",e)

def getNewId(data):
    if not data:
        return 1
    max_id = max(item["id"] for item in data)
    return max_id + 1


def add_expense(args):
    data=cargarJson()
    id=getNewId(data)
    currentDate=datetime.date.today()
    
    try:
        new_expense_data={
                    "id":id,
                    "amount":f"args.amount",
                    "description":args.description,
                    "date":f"{currentDate.year}-{currentDate.month}-{currentDate.day}",
                    "year":currentDate.year,
                    "month":currentDate.month,
                    "day":currentDate.day
                    
                    }
    
        data.append(new_expense_data)
        guardarJson(data)
        print(f"Expense added successfully (ID: {id})")

    except Exception as e:
        print("An unexpected error has occurred",e )

    
    
    

def update_expense(args):
    data=cargarJson()
    
    itemIndex=getItemIndexById(args.id,data)
    item=data[itemIndex]
    if item:
        if args.amount is not None:
            item["amount"]=args.amount

        if args.description is not None:
            item["description"]=args.description

        data[itemIndex]=item

        guardarJson(data)
        print(f"The expense with id: {args.id} was successfully updated")
    
    else:
        print(f"No expense found with the id {args.id}")
   

def delete_expense(args):

    data=cargarJson()

    if args.id:
        itemIndex=getItemIndexById(args.id,data)
        
        if itemIndex is not None:
            data.pop(itemIndex)

            guardarJson(data)

            print(f"The expense with ID {args.id} was successfully deleted, I won't miss him")
        else:
            print(f"No expense found with ID: {args.id}")
    else:
        
        first= input("Are you sure you want to delete all expenses? (y/n): ")
        
        if first.lower() == 'y':

            second = input("This action CANNOT be undone. Type 'DELETE ALL' to confirm:")
            if second == 'DELETE ALL':
                data.clear()  
                guardarJson(data)
                print("All expenses have been deleted successfully. I hope you're proud")
            else:
                print("Nice try, Whiskers. You're not deleting anything today🐾.")
        else:
            print("No expenses were deleted, I would swear they were shaking.")

def imprimirFila(fila:list):
    cadena="# "
    for element in fila:
        cadena+=str(element)
    print(cadena)

def view_expense(args):
    data=cargarJson()
    if not data:
        print("❌ No hay gastos registrados.")
        return
    fila=[]

    keys2Print=("id","date","description", "amount")
    for key in keys2Print:
        key=str(key).upper()
        printkey=key.ljust(15)
        fila.append(printkey)

    imprimirFila(fila)


    for item in data:
        fila=[]
        for key in keys2Print:
            value = item.get(key, 'N/A')
            if key=="amount":
                value=f"${value:.2f}"
            fila.append(str(value).ljust(15))
        
        imprimirFila(fila)
            
    

def summary(args):

    months=("January","February","March","April","May","June","July","August","September","October","November","December")
    currentYear=datetime.date.today().year
    month=args.month
    data=cargarJson()
    total=0

    if month is not None:
        if not (1<=month<=12):
            print("Invalid month. Please provide a number between 1 and 12.")
            return
        for item in data:
            if item['month']==month and item["year"] ==currentYear:
                total+=item['amount']

        print(f"Total expenses for {months[month-1]} {currentYear}: ${total:.2f}")
    
    else:
       
        for items in data:
            total+=items['amount']

        print(f"Total Expenses: ${total:.2f}")

    
def main():
    
    
    
    parser=argparse.ArgumentParser( description="EXPENSE-TRACKER-2025-ONE LINK-NO FAKE")
    subparser= parser.add_subparsers(title="CRUD commands",dest="comand")


    #Add command
    parser_add_expense=subparser.add_parser("add",help="Add an expense with a description and amount.")
    parser_add_expense.add_argument("--description", type=str,help="Expense description",default="Too lazy to type a description :p")
    parser_add_expense.add_argument("--amount", type=float,help="Expense Amount", default=0)
    parser_add_expense.set_defaults(func=add_expense)

    #Update command
    parser_update_expense=subparser.add_parser("update",help="Update expense information based on its ID")
    parser_update_expense.add_argument("id",type=int,help="Expense ID")
    parser_update_expense.add_argument("--description", type=str,help="Expense description",default=None)
    parser_update_expense.add_argument("--amount", type=float,help="Expense Amount",default=None)
    parser_update_expense.set_defaults(func=update_expense)

    #Delete command
    parser_delete_expense=subparser.add_parser("delete",help="Delete a expense on its ID")
    parser_delete_expense.add_argument("--id",type=int,help="Expense ID", default=None)
    parser_delete_expense.set_defaults(func=delete_expense)

    #View command
    parser_view_expense=subparser.add_parser("view",help="View all expenses in list formart")
    parser_view_expense.set_defaults(func=view_expense)

    #View summary command
    parser_summary_expense=subparser.add_parser("summary",help="Display a summary of all expenses or all expenses for a month")
    parser_summary_expense.add_argument("--month",type=int,help="Month for which the expense summary will be displayed", default=None)
    parser_summary_expense.set_defaults(func=summary)


    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


main()