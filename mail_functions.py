def order_conf(user, book_data):
    msg = "Hello " + user + "!\n Thanks for choosing our store! Below you can find details of your order!\n\n" \
            "Title: " + book_data[0] + "\n Author: " + book_data[1] + "\n ISBN: " + book_data[2] + "\n Publisher: " \
             + book_data[3] + "\n Price: " + str(book_data[4]) + "\n\n Best regards \n eBookStore"
    return msg

def registration_conf(user):
    msg = "Hello " + user + "!\n Welcome in our eBookStore! \n We hope that you will be satisfied with our sevices. \n\n Best regards \n eBookStore"
    return msg
