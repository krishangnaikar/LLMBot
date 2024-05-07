import os


class SessionId:
    def __init__(self):
        self.session_id = self.get_latest_session_id()

    def get_latest_session_id(self):
        # Read from latest_sessionid.txt and check the number
        if os.path.exists("latest_sessionid.txt"):
            with open("latest_sessionid.txt", "r") as f:
                session_id = int(f.read())
                return session_id
        else:
            with open("latest_sessionid.txt", "w") as f:
                f.write(1)
                return 1

    def update_sessionid(self, session_id):
        self.session_id = session_id
        with open("latest_sessionid.txt", "w") as f:
            f.write(str(session_id))
class User:
    def __init__(self, userId=-1, username="", password="", session_id=-1, permission = "base_user"):
        self.userId = userId
        self.username = username
        self.password = password
        self.session_id = session_id
        self.permission = permission

    def save(self, filename):
        print(f"Saving user {self.username}")
        # Check if user already exists with username
        if os.path.exists(filename):
            with open(filename, "r") as f:
                for line in f:
                    user_id, user_username, user_password, session_id, permission = line.strip().split(",")
                    if user_username == self.username and not(user_password == self.password):
                        raise ValueError(f"User with username {self.username} already exists")
                    elif user_username == self.username and (user_password == self.password):
                        self.delete_user(self.username)

        if (self.userId == -1):
            # Create user id
            self.userId = self.create_userid(filename)

        if (self.session_id == -1):
            # Create session id
            self.session_id = SessionId().session_id



        # Save user to file
        with open(filename, "a") as f:
            f.write(f"{self.userId},{self.username},{self.password},{self.session_id},{self.permission}\n")

    def create_userid(self, filename):
        # Get last user id from file and add 1
        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    last_user_id = int(f.readlines()[-1].split(",")[0])
                except IndexError:
                    last_user_id = 0
                return last_user_id + 1

    def delete_user(self, username):

        # Read the data from the file
        with open('users.csv', 'r') as file:
            lines = file.readlines()

        # Find the user with the given username and remove it
        updated_lines = [line for line in lines if line.strip().split(',')[0] != username]

        # Write the updated data back to the file
        with open('users.csv', 'w') as file:
            file.writelines(updated_lines)

        return True

    def update_sessionid(self, session_id):
        self.session_id = session_id
        self.save("users.csv")


    def get_sessionid(self, filename):
        # Read from filename and check the row with the correct userId and return the row's sessionid
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    for line in f:
                        user_id, user_username, user_password, session_id = line.strip().split(",")
                        if user_id == self.userId:
                            return session_id



class Users:
    def __init__(self):
        self.users = self.load_users("users.csv")

    def load_users(self, filename):
        users = []
        if os.path.exists(filename):
            with open(filename, "r") as f:
                for line in f:
                    user_id, user_username, user_password, session_id, permission = line.strip().split(",")
                    users.append(User(user_id, user_username, user_password, session_id, permission))
        return users

    def new_user(self, username, password):
        user = User(username=username, password=password)
        try:
            user.save("users.csv")
            self.users.append(user)
        except ValueError:
            print("value error")
            return False

    def get_user(self, userId):
        for user in self.users:
            if user.userId == userId:
                return user

    def get_user_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return False

    def login(self, username, password):
        user = self.get_user_by_username(username)
        if not (user):
            return False
        if user and user.password == password:
            #user.update_sessionid(SessionId().session_id)
            return user.session_id
        else:
            return False


users = Users()