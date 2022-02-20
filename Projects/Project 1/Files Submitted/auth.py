import sys
from tinydb import TinyDB, Query


class Auth:
    CMD_INFO = """Usage:
        auth AddUser <user> <password>
        auth Authenticate <user> <password>
        auth SetDomain <user> <domain>
        auth DomainInfo <domain>
        auth SetType <object> <type>
        auth TypeInfo <type>
        auth AddAccess <operation> <domain> <type>
        auth CanAccess <operation> <user> <object>
        auth Clear
        """

    def __init__(self, db):
        self.db = db

        self.users = self.db.table('users', cache_size=0)
        self.User = Query()

        self.objects = self.db.table('objects', cache_size=0)
        self.Object = Query()

        self.accesses = self.db.table('access', cache_size=0)
        self.Access = Query()

    def AddUser(self, username, password):
        if self.users.get(self.User.username == username):
            return 'Error: user exists'
        if username == '':
            return 'Error: username missing'

        self.users.insert({'username': username, 'password': password, 'domains': []})
        return 'Success'

    def Authenticate(self, username, password):
        user = self.users.get(self.User.username == username)
        if not user:
            return 'Error: no such user'
        if user['password'] != password:
            return 'Error: bad password'
        return 'Success'

    def SetDomain(self, username, domain):
        # does user exist
        user = self.users.get(self.User.username == username)
        if not user:
            return 'Error: no such user'
        if domain == '':
            return 'Error: missing domain'
        # add the domain to the user if it doesn't already exist
        if domain not in user['domains']:
            self.users.update({'domains': user['domains'] + [domain]}, self.User.username == username)
        return 'Success'

    def DomainInfo(self, domain):
        if domain == '':
            return 'Error: missing domain'
        domain_users = self.users.search(self.User.domains.any(domain))
        return '\n'.join([domain_user['username'] for domain_user in domain_users])

    def SetType(self, object_name, type_name):
        if object_name == '':
            return 'Error: missing object'
        if type_name == '':
            return 'Error: missing type'
        #does object exist
        object = self.objects.get(self.Object.name == object_name)
        if object:
            if type_name not in object['types']:
                self.objects.update({'types': object['types'] + [type_name]}, self.Object.name == object_name)
        else:
            self.objects.insert({'name': object_name, 'types': [type_name]})
        return 'Success'

    def TypeInfo(self, type_name):
        if type_name == '':
            return 'Error: missing type'
        type_objects = self.objects.search(self.Object.types.any(type_name))
        return '\n'.join([type_object['name'] for type_object in type_objects])

    def AddAccess(self, operation, domain_name, type_name):
        if operation == '':
            return 'Error: missing operation'
        if domain_name == '':
            return 'Error: missing domain'
        if type_name == '':
            return 'Error: missing type'

        access = self.accesses.get(
            (self.Access.operation == operation) & (self.Access.domain == domain_name) & (
                    self.Access.type == type_name))
        if not access:
            self.accesses.insert({'operation': operation, 'domain': domain_name, 'type': type_name})
        return 'Success'

    def CanAccess(self, operation, username, object_name):
        if operation == '':
            return 'Error: missing operation'
        if username == '':
            return 'Error: missing domain'
        if object_name == '':
            return 'Error: missing object'

        # user query
        user = self.users.get(self.User.username == username)
        if not user:
            return 'Error: user not found'

        # object query
        object = self.objects.get(self.Object.name == object_name)
        if not object:
            return 'Error: object not found'

        for domain in user['domains']:
            for type in object['types']:
                if self.accesses.get(
                        (self.Access.operation == operation) & (self.Access.domain == domain) & (
                                self.Access.type == type)):
                    return 'Success'
        return 'Error: access denied'

    def Clear(self):
        self.db.drop_tables()
        return 'Success: Database was cleared'
    def execute(self, args):
        args_passed = len(args)
        if args_passed < 2:
            return Auth.CMD_INFO

        base_cmd = args[1].lower()
        if base_cmd == 'adduser':
            if args_passed != 4:
                return 'Usage: auth AddUser <user> <password>'
            return self.AddUser(args[2], args[3])

        if base_cmd == 'authenticate':
            if args_passed != 4:
                return 'Usage: auth Authenticate <user> <password>'
            return self.Authenticate(args[2], args[3])

        if base_cmd == 'setdomain':
            if args_passed != 4:
                return 'Usage: auth SetDomain <user> <domain>'
            return self.SetDomain(args[2], args[3])

        if base_cmd == 'domaininfo':
            if args_passed != 3:
                return 'Usage: auth DomainInfo <domain>'
            return self.DomainInfo(args[2])

        if base_cmd == 'settype':
            if args_passed != 4:
                return 'Usage: auth SetType <object> <type>'
            return self.SetType(args[2], args[3])

        if base_cmd == 'typeinfo':
            if args_passed != 3:
                return 'Usage: auth TypeInfo <type>'
            return self.TypeInfo(args[2])

        if base_cmd == 'addaccess':
            if args_passed != 5:
                return 'Usage: AddAccess <operation> <domain> <type>'
            return self.AddAccess(args[2], args[3], args[4])

        if base_cmd == 'canaccess':
            if args_passed != 5:
                return 'Usage: CanAccess <operation> <user> <object>'
            return self.CanAccess(args[2], args[3], args[4])

        if base_cmd == 'clear':
            return self.Clear()

        #invalid command
        return Auth.CMD_INFO


def main():
    if sys.version_info < (3, 0):
        print('Please make sure you are using Python 3.')
        return
    auth = Auth(TinyDB('db.json'))
    print(auth.execute(sys.argv))


if __name__ == '__main__':
    main()
