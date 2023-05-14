#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import re
import json
"""
This is a module where you define your class HBNBCommand class, a command interpreter that
implements commands for creating, showing, destroying, updating and listing
instances of classes that inherit from BaseModel.

Inside the console,the user can enter commands in the following format:

(hbnb) command class_name class_id [attribute_name] [attribute_value]

"""

class HBNBCommand(cmd.Cmd):
    """
    This class defines a command-line interpreter for managing instances of
    classes that inherit form 'BaseModel'.It allows the user to create,
    show, destroy, update and list instances of classes,
    and saves all changes to a JSON file.

    prompt (str):there is a prompt before a user enters a command that has Default value of "(hbnb)" 
    
    """

    prompt = '(hbnb) '

    __classes = ["BaseModel"]

    def do_create(self, arg):
        """Create a new instance of BaseModel"""
        if not arg:
            print("** class name missing **")
            return

        if arg not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        model_class = globals()[arg]
        if model_class is not None:
            obj = model_class()
            obj.save()
            print(obj.id)
        else:
            print("** class doesn't exist **")

    def help_create(self):
        """Dislay information about the create command."""
        print("Usage: create <class>")
        print("Create a new class, print its id, and save it to file.json")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        objects = storage.all()
        key = args[0] + '.' + args[1]
        if key not in objects:
            print("** no instance found **")
            return

    def help_show(self):
        """Displays help information for the show command"""
        print("Displays an object's string representation based\
                on the objects class and id")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return

        if args[0] not in HBNBCommand__classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return
        if not args[1]:
            print("** no instance found **")
        key = args[0] + '.' + args[1]
        all_instances = storage.all()
        if key in all_instances:
            del all_instances[key]
            storage.save()
            print(storage.all())

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.allowed_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        key = None
        value = None

        if len(args) < 3:
            print("** attribute name missing **")
            return

        key = args[2]

        if len(args) < 4:
            print("** value missing **")
            return

        value_str = args[3]
        try:
            value = int(value_str)
        except ValueError:
            if value_str.startswith('"') and value_str.endswith('"'):
                value = value_str[1:-1]
            else:
                print("** value missing **")
                return

        objs = storage.all()
        key_to_update = class_name + "." + obj_id
        if key_to_update not in objs:
            print("** no instance found **")
            return
        obj = objs[key_to_update]
        setattr(obj, key, value)
        obj.save()

    def do_quit(self, arg):
        """Return True upon receiving quit command"""
        return True

    def help_quit(self):
        """Dispaly information about the quit command."""
        print("Quit command to exit the program")

    def do_EOF(self, arg):
        """Retrun upon receiving an EOF signal"""
        print("")
        return True

    def help_EOF(self):
        """Display information about EOF signal handling."""
        print("EOF signal to exit the program")

    def emptyline(self):
        """Do nothing on empty line"""
        pass

    def do_all(self, arg):
        """
        Prints all string representation of all instances based or
        not on the class name.
        Usage:
            all             Prints all string representaion of all instances
                            from all classes.

            <class name>.all() Prints all string representaion of all instances
                                from the given class name.
        """
        tokens = arg.split()
        class_name = tokens[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        objects_dict = storage.all()
        print("object dicts = ")
        print(objects_dict)

        str_repr_list = []
        if not arg:
            for key, val in objects_dict.items():
                str_repr_list.append((objects_dict[key].__str__()))
        else:
            for key, val in objects_dict.items():
                if class_name in key:
                    str_repr_list.append((objects_dict[key].__str__()))
                    print(str_repr_list)


if __name__ == '__main__':
    HBNBCommand().cmdloop()