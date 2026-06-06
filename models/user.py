USer = []
class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.favorites = []
logstat = False
while True :

    if logstat == False:
        user_chois = input("""1.register?
        2. lionigng
        3. nothing.
        -
        """)
        print(user_chois)

        if user_chois == '1' :
            username = input("pirnt youre username:")
            while True :
                emailRough= input("write youre e.mail:")
                if "@" and "." in emailRough :
                    print("e.mail")
                    break
                else :
                    print("please write e.mail correctly")
            while True:
                passwordRough = input("last,password:")
                if len(passwordRough)<7 :
                    print("write 8 or more symbols")
                elif passwordRough == input("rewrite youre password:"):
                    print("you registered.")
                break
            new_user = User(username = username, password = passwordRough, email = emailRough)
            USer.append(new_user)
            logstat = True

        elif user_chois == '2' :
            usernameWrited = input("write youre username:")
            passwordWrited = input("write youre password:")
            try:
                for usernam in User.username:
                    if usernam.username == usernameWrited and user.password == passwordWrited:
                        logstat = True
                        print("you are singed in")
            except ValueError as err:
                print(err)

        else:
            print("bye.")
            logstat = False
    else :
        user_chois = input("""
        1.add something to wishlist?
        2.delete something?
        3.look to a wishlist.
        3.nouhing
        -""")
        if user_chois == '1':
            wish = input('''what to add?
            -''')
            USer[0].favorites.append(wish)
            print("item added to a wishlist. ")
        elif user_chois == '2':
            for ind in range(len(self.user.favorites)):
                print(str(ind)+ind-1[self.user.favorites])

            uwished = int(input("what to delete?"))-1 
            self.User.favorites.pop(unwished)
        elif user_chois == '3':
            for ind in range(len(self.user.favorites)):
                print(str(ind)+ind-1[USer.favorites])
        else :
            print('bue')
            break