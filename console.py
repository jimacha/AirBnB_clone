#!/usr/bin/python3
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User
import cmd

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

    prompt = ' (hbnb) '

    def __init__(self, completekey='tab'):
        super().__init__(completekey=completekey)
        self.__models = {
                'BaseModel': BaseModel,
                'User': User,
                'State': State,
                'City': City,
                'Amenity': Amenity,
                'Place': Place,
                'Review': Review
                }
        self.__valid_methods = ['create', 'show', 'destroy', 'all', 'update']
        self.allowed_classes = list(self.__models.keys())
        self.__options = [
                '{}.{}'.format(k, v)
                for k, v in self.__models.items()
                for v in dir(v) if not v.startswith('_')
                ]

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, args):
        """EOF(end of file) command to exit the program"""
        return True

    def do_create(self, line):
        """Create command to create a new instance of a class"""
        args = line.split()
        if not args:
            print("** iclass name missing **")
            return

        class_name = args[0]
        if class_name not in self.allowed_classes:
            print("** class doesn't exist **")
            return
        new_instance = BaseModel()
        storage.new(new_instance)
        storage.save()
        print(new_instance.id)

    def do_show(self, line):
        """Show command to print the string representation of an instance"""
        args = line.split()
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

        instance_id = args[1]
        key = class_name + '.' + instance_id
        all_instances = storage.all()
        if key not in all_instances:
            print("** no instance found **")
            return

        instance = all_instances[key]
        print(instance)

    def do_destroy(self, line):
        """Destroy command to delete an instance"""
        args = line.split()
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
        instance_id = args[1]
        key = class_name + '.' + instance_id
        all_instances = storage.all()
        if key not in all_instances:
            print("** no instance found **")
            return

        del all_instances[key]
        storage.save()

    def do_all(self, line):
        """
        Prints all string representation of all instances based or
        not on the class name.
        
        """
        args = line.split()
        all_instances = storage.all()

        if not args:
            print([str(key) for key in all_instances.values()])
            return
        else:
            try:
                class_name, method_name = line.split('.')
                if method_name != 'all()':
                    raise ValueError
                cls = models.classes[class_name]

                if args[0] not in self.allowed_classes:
                    print("** class doesn't exist **")
                return
            except (ValueError, KeyError):
                print("** Unknown syntax:", line)
                return

            print([str(obj) for obj in all_instances.all(cls).values()])

    def do_update(self, line):
        """Update command to update an instance"""
        args = line.split()

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

    def default(self, line):
        """
        Called on an input line when the command prefix is not recognized.
        """
        parts = line.split(".")
        if len(parts) == 2 and parts[1] == "all()":
            # Retrieve all instances of the specified class
            class_name = parts[0]
            if class_name not in self.allowed_classes:
                print("** class doesn't exist **")
                return
            all_instances = storage.all()
            instances = [str(obj) for obj in all_instances.values()
                         if type(obj).__name__ == class_name]
            print(instances)
        elif len(parts) == 2 and parts[1] == "count()":
            # Retrieve the count of all instances of the specified class
            class_name = parts[0]
            if class_name not in self.allowed_classes:
                print("** class doesn't exist **")
                return
            all_instances = storage.all()
            count = sum(1 for obj in all_instances.values()
                    if type(obj).__name__ == class_name)
            print(count)
        else:
            print("*** Unknown syntax: {}".format(line))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
