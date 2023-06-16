# Import module 'sqlite3'.
import sqlite3

# Creates or opens a file called 'ebookstore' with SQlite 3 DB.
db = sqlite3.connect(':memory:')

# Create a table called 'books' with id as the primary key.
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE books
    (id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)
''')
print('Table created successfully!')

# Save the changes to the database.
db.commit()

# 'book_inv' stores a list of tuples containing the books and their details.
book_inv = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
            (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
            (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
            (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]
cursor.executemany('''INSERT INTO books(id, Title, Author, Qty)
               VALUES (?, ?, ?, ?)''', book_inv)

print('Data inserted successfully!\n')

# Save changes to the database.
db.commit()

# Print the 'books' table using for loop.
cursor.execute(''' SELECT * FROM books''')
print('Books Table')
for row in cursor:
    print('{0} : {1} : {2}: {3}'.format(row[0], row[1], row[2], row[3]))

# Save changes to the database.
db.commit()


#  Define 'print_table' function that displays the updated books table.
def print_table():
    cursor.execute('''SELECT * FROM books''')
    print('\nUpdated Books Table')

    # Print the updated books table using for loop.
    for rows in cursor:
        print(f'id: {rows[0]}, Title: {rows[1]}, Author: {rows[2]}, Qty: {rows[3]} ')


# Define 'add_book' function that inserts new row into books table.
def add_book():
    # Request user to input book's id.
    # Check and print error message if the id already exists.
    # Except ValueError and print error message.
    while True:
        try:
            book_id = int(input("Enter the book's id number: "))
            cursor.execute('''SELECT  * FROM books WHERE id = ?''', (book_id,))
            res1 = cursor.fetchall()
            if res1:
                print("This id already exists, please enter a different id")
                continue
            break
        except ValueError:
            print("Invalid id! Please use numbers!")

    # Request user to input book's title and author.
    book_title = input("Enter the book's title: ")
    book_author = input("Enter the book's author: ")

    # Request user to input book's quantity.
    # Except ValueError and print error message.
    while True:
        try:
            book_qty = int(input("Enter the quantity of the book: "))
            break
        except ValueError:
            print("Invalid input, please enter a number!")

    cursor.execute('''INSERT INTO books (id, Title, Author, Qty)
                    VALUES(?, ?, ?, ?)''', (book_id, book_title, book_author, book_qty))
    db.commit()
    print_table()


# Define 'update_book' function that updates the details of the book.
def update_book():
    cursor.execute('''SELECT * FROM books''')
    books = cursor.fetchall()
    while True:
        try:
            book_id = int(input("Enter the book's id number: "))
            id_list = []
            for id_of_book in books:
                id_list.append(id_of_book[0])

            # Print error message if the book does not exist.
            if book_id not in id_list:
                print("The book does not exist, please try again.")
                continue

            # Else, present user with options of what they would like to update.
            else:
                while True:
                    update = input("""
What do you want to update?
1 - Title
2 - Author 
3 - Quantity
0 - Return to main menu:
Enter a number to select an option:\n""")

                    # If user input is "1", request user for the new title.
                    if update == "1":
                        new_update = input("Enter the new title: ")
                        cursor.execute('''UPDATE books SET Title = ? WHERE id = ?''', (new_update, book_id))
                        db.commit()
                        print_table()
                        break

                    # Else if, user input "2", request user for the new author.
                    elif update == "2":
                        new_update = input("Enter the new author: ")
                        cursor.execute('''UPDATE books SET Author = ? WHERE id = ?''', (new_update, book_id))
                        db.commit()
                        print_table()
                        break

                    # Else if, user input is "3" request user for the new quantity.
                    # Except ValueError and print error message.
                    elif update == "3":
                        while True:
                            try:
                                new_update = int(input("Enter the new quantity: "))
                                cursor.execute('''UPDATE books SET Qty = ? WHERE id = ?''', (new_update, book_id))
                                db.commit()
                                print_table()
                                break
                            except ValueError:
                                print("Invalid input. Please use numbers!")

                        # Else if, user input is "0", return to the main menu.
                    elif update == "0":
                        main_menu()

                        # Else, print error message.
                    else:
                        print("Invalid input! Please try again!")
                break

        # Except ValueError and print error message.
        except ValueError:
            print("Invalid input. Please enter numbers.")

        # Catch the exception, roll back any change if something goes wrong.
        except Exception as e:
            db.rollback()
            raise e


# Define 'delete_book' function that will delete the book that user wants to delete.
def delete_book():
    cursor.execute('''SELECT * FROM books''')
    books = cursor.fetchall()
    while True:
        try:
            book_id = int(input("\nEnter the id of the book you want to delete: "))
            id_list = []
            for book in books:
                id_list.append(book[0])

            # Print error message if the id does not exist.
            if book_id not in id_list:
                print("The id does not exist, please try again.")
                continue

            # Else, delete the selected book from the database.
            else:
                cursor.execute('''DELETE FROM books WHERE id = ?''', (book_id,))
                db.commit()
                break

        # Except ValueError and print error message.
        except ValueError:
            print("Invalid id, please try again!")
    print_table()


# 'Search book' function prints the row according to user's input of book_id
def search_book():
    cursor.execute('''SELECT * FROM books''')
    books = cursor.fetchall()
    while True:
        try:
            book_id = int(input("\nEnter the id of the book you want to search: "))
            id_list = []
            for id_of_book in books:
                id_list.append(id_of_book[0])

            # Print error message if the book does not exist.
            if book_id not in id_list:
                print("The book does not exist, please try again.")
                continue

            # Else, select the book from the books table and print its details.
            else:
                cursor.execute('''SELECT * FROM books WHERE id=?''', (book_id,))
                book = cursor.fetchone()
                print(f'id: {book[0]}\nTitle: {book[1]}\nAuthor: {book[2]}\nQty: {book[3]}')
                break
        except ValueError:
            print("Invalid id, please try again!")


# Define 'main_menu' function that presents user with main menu and takes the user's number choice for the menu option.
def main_menu():
    while True:
        menu = input("""
Welcome to your ebook store managing system:
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit
Please enter a number to select an option (0-4): \n""")

        # If user input is "0", close the connection, print goodbye message and exit.
        if menu == "0":
            db.close()
            print("Goodbye!")
            exit()

        # Else if, user input is "1", call the 'add_book()' function.
        elif menu == "1":
            add_book()

        # Else if, user input is "2", call the 'update_book()' function.
        elif menu == "2":
            update_book()

        # Else if, user input is "3", call the 'delete_book()' function.
        elif menu == "3":
            delete_book()

        # Else if, user input is "4", call the 'search_book()' function.
        elif menu == "4":
            search_book()

        # Else, print 'Invalid input, please try again'.
        else:
            print("Invalid input, please try again!")


# Call 'main_menu()' function to start the program.
main_menu()
