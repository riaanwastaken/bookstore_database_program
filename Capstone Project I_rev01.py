# L2T13 Capstone Project 1.

import sqlite3


# Defining functions used in program.
def integer_input():
    while True:
                try:
                    qty_input = int(input("Please enter quantity: "))
                    return qty_input
                
                except ValueError:
                    print("\nOops! That was not a valid number. Try again...")


# *** Start of main program ***


# The entire program is caught in either try, except and finally as suggested in 
# the task notes. 
try:

    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()  

    #Creating table if not already exists named 'books'.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT, Author TEXT,
                        QTY INTEGER)''')
    db.commit()
    #cursor.execute('''ALTER TABLE BOOKS''')
    cursor.execute('''INSERT INTO books(id, title, author, qty)
                VALUES(?,?,?,?)''', (3001,"A Tale of Two Cities", "Charles Dickens", 30))
    # Populating table 'books' with list of books.
    book_list = [
        
        ("Harry Potter and the Philosopher's Stone","J.K. Rowling", 40),
        ("The Lion, the Witch and the Wardrobe", "C. S. Lewis" , 25),
        ("The Lord of the Rings","J.R.R Tolkien", 37),
        ("Alice in Wonderland", "Lewis Carroll", 12)]

    cursor.executemany(''' INSERT INTO books( Title, Author, QTY)
        VALUES(?,?,?)''', book_list)
    db.commit()


 
    # Menu to be displayed to user with options to manipulate the created database 
    # containing a table named 'books' with pupulated information.
    menu = '''
    Welcome to the book database.

    Please select one of the following :

    ad  = Enter book
    up  = Update book
    del = Delete book
    sr  = Search books
    e   = Exit
    '''

    while True:

        user_option = input(menu).lower()

        if user_option == 'ad':

            title_input = input("Enter book Title: ")
            author_input = input("Please enter Author Name and Surname: ")
            qty_input = integer_input()

            cursor.execute('''INSERT INTO books( Title, Author, QTY)
                            VALUES(?,?,?)''', (title_input, title_input, qty_input))
            print('\nbook succesfully entered into database')
            db.commit()
            
        elif user_option == 'up':

            id_input = input("Enter ID code to be updated 0000: ")

            if cursor.execute('''SELECT id FROM books WHERE id = ?''', (id_input,)).fetchone():
                print("ID sucsesfully found, continuing ")

                title_input = input("Enter book Title: ")
                author_input = input("Please enter Author Name and Surname: ")
                qty_input = integer_input()

                cursor.execute('''UPDATE books SET Title = ?,Author = ?, QTY = ? 
                WHERE id = ?''', (title_input, author_input, qty_input,id_input))
                db.commit()
                print(f"\nID: {id_input} succesfully updated into database")
                

            else:
                print("ID entered not found in database")


        elif user_option == 'del':
            while True:

                try:
                    id_input = int(input("\nEnter ID code to be DELETED 0000: "))
                    break
                except ValueError:
                    print("\nOops! That was not a valid number. Try again...")   
        
            cursor.execute('''DELETE FROM books WHERE id = ?''', (id_input,))
            db.commit()
            print(f"\nID: {id_input} Deleted...")


        elif user_option == 'sr':
            while True:
                try:
                    id_input = int(input("\nEnter ID code to be VIEWED 0000: "))
                    break
                except ValueError:
                    print("\nOops! That was not a valid number. Try again...")
        
            # Validating if the ID entered is in the database.
            if cursor.execute('''SELECT id FROM books WHERE id = ?''', (id_input,)).fetchone():
                print("ID sucsesfully found, here are the details: ")
                
                cursor.execute('''SELECT Title, Author, QTY FROM books  
                WHERE id=?''', (id_input,))
                book_viewed = cursor.fetchone()
                print(f"\n{book_viewed}")

            # If ID entered is not in the database, error message runs.
            else:
                print("ID entered not found in database")
                
            
        elif user_option == 'e':
            print("Goodbye")
            exit()


        else:
            print("Invalid menu option, try again...")


except Exception as e:
    raise e


finally:
    db.close

# End of program
