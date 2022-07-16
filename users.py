import pwd
import os


class User:
    def __init__(self, gid, uid, name) -> None:
        self.gid = gid
        self.uid = uid
        self.name = name

    def __str__(self) -> str:
        return 'User(gid={} uid={} name={})'.format(
            self.gid,
            self.uid,
            self.name
        )


def get_user_list():
    user_list = []

    raw_list = pwd.getpwall()
    for raw_user in raw_list:
        user = User(raw_user[3], raw_user[2], raw_user[0])
        user_list.append(user)

    return sorted(user_list, key=lambda u: u.name)


def current_user():
    uid = os.getuid()
    user = pwd.getpwuid(uid)
    return User(user[3], user[2], user[0])


if __name__ == "__main__":
    print(current_user())
