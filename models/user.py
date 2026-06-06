USer = []
class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.favorites = []
        self.wishlist = []
logs = False
while True :

    if logs == False:
        user_chose = input("""1.register?
        2. log in
        3. exit
        -
        """)
        print(user_chose)

        if user_chose == '1' :
            username = input("print your username:")
            while True :
                emailRough= input("write your e.mail:")
                if "@" and "." in emailRough :
                    print("e.mail")
                    break
                else :
                    print("please write e.mail correctly")
            while True:
                passwordRough = input("last,password:")
                if len(passwordRough)<7 :
                    print("write 8 or more symbols")
                elif passwordRough == input("rewrite your password:"):
                    print("you are registered.")
                break
            new_user = User(username = username, password = passwordRough, email = emailRough)
            USer.append(new_user)
            logs = True

        elif user_chose == '2' :
            usernameWrote = input("write your username:")
            passwordWrote = input("write your password:")
            try:
                for username in User.username:
                    if username == usernameWrote and User.password == passwordWrote:
                        logs = True
                        print("you are singed in")
            except ValueError as err:
                print(err)

        else:
            print("bye.")
            logs = False
            break
