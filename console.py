#!/usr/bin/python3
"""" comand interpreter
     Documentetion: https://pymotw.com/3/cmd/
"""

import cmd
import re
import json
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """ console class """
    prompt = "(hbnb) "

    def do_EOF(self, line):
        """ Exit program """
        print()
        return True

    def do_quit(self, line):
        """ Exit program """
        return True

    def emptyline(self):
        pass

    def do_create(self, line):
        """ create an instance of create """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")
            obj = eval("{}()".format(my_list[0]))
            for i in range(1, len(my_list)):
                if '=' in my_list[i]:
                    k, v = tuple(my_list[i].split("="))
                if "\"" in v:
                    v = v.split("\"")[1].replace('_', ' ')
                setattr(obj, k, v)
            obj.save()
            print("{}".format(obj.id))
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """ string representation of an instance based on
                    class name
                    id
        """
        if line is None or line == "":
            print("** class name missing **")
        else:
            kword = line.split(' ')
            if kword[0] not in storage.classes():
                print(" ** class doesn't exist **")
            elif len(kword) < 2:
                print("** instance id missing **")
            else:
                k = "{}.{}".format(kword[0], kword[1])
                if k not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[k])

    def do_destroy(self, line):
        """ Deletes an instance based on
                class name
                id
        """
        if line is None or line == "":
            print("** class name missing **")
        else:
            kword = line.split(' ')
            if kword[0] not in storage.classes():
                print(" ** class doesn't exist ** ")
            elif len(kword) < 2:
                print(" ** instance id missing **")
            else:
                k = "{}.{}".format(kword[0], kword[1])
                if k not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[k]
                    storage.save()

    def do_all(self, line):
        """ print all string rep of an instance"""
        if line != "":
            kword = line.split(' ')
            if kword[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                a = [str(obj) for key, obj in storage.all().items()
                     if type(obj).__name__ == kword[0]]
                print(a)
        else:
            new = [str(obj) for key, obj in storage.all().items()]
            print(new)

    def do_update(self, line):
        """  Updates an instance based on
                class name
                id
                by adding or updating attribute
        """
        if line == "" or line is None:
            print("** class name missing **")
            return
        # can use normal arguments and index as another option
        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                """want to know if value is float"""
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_count(self, line):
        """ retrieve an instance based on its ID"""
        kword = line.split(' ')
        if not kword[0]:
            print("** class name missing **")
        elif kword[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [
                i for i in storage.all() if i.startswith(
                    kword[0] + '.')]
            print(len(matches))

    def default(self, line):
        """Catch commands if nothing else matches then."""
        self._precmd(line)

    def _precmd(self, line):
        """Intercepts commands to test for class.syntax()"""
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command

    def update_dict(self, classname, uid, s_dict):
        """Helper method for update() with a dictionary."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
