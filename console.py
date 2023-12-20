#!/usr/bin/python3

""" Console Module """
import shlex
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args_input> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args_input: (<id>, [<delim>], [<*args_input>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args_input or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass
    
    def do_create(self, arg):
        '''
            Create a new instance of class BaseModel and saves it
            to the JSON file.
        '''
        args_input = arg.split()

        if len(args_input) == 0:
            print("** class name missing **")
            return

        new_args = []
        for a in args_input:
            idx = a.find("=")
            a = a[0: idx] + a[idx:].replace('_', ' ')
            new_args.append(a)

        if new_args[0] in HBNBCommand.classes:
            new_instance = HBNBCommand.classes[new_args[0]]()
            new_dict = {}
            for a in new_args:
                if a != new_args[0]:
                    my_list = a.split('=')
                    new_dict[my_list[0]] = my_list[1]

            for k, v in new_dict.items():
                if v[0] == '"':
                    v_list = shlex.split(v)
                    new_dict[k] = v_list[0]
                    setattr(new_instance, k, new_dict[k])
                else:
                    try:
                        if type(eval(v)).__name__ == 'int':
                            v = eval(v)
                    except:
                        continue
                    try:
                        if type(eval(str(v))).__name__ == 'float':
                            v = eval(v)
                    except:
                        continue
                    setattr(new_instance, k, v)
            new_instance.save()
            print(new_instance.id)
        else:
            print("** class doesn't exist **")


    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args_input):
        """ Method to show an individual object """
        new = args_input.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args_input
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args_input):
        """ Destroys a specified object """
        new = args_input.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args_input):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args_input:
            args_input = args_input.split(' ')[0]  # remove possible trailing args_input
            if args_input not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args_input:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args_input):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args_input == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args_input):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args_input, ex: (<cls>, delim, <id/args_input>)
        args_input = args_input.partition(" ")
        if args_input[0]:
            c_name = args_input[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args_input
        args_input = args_input[2].partition(" ")
        if args_input[0]:
            c_id = args_input[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args_input
        if '{' in args_input[2] and '}' in args_input[2] and type(eval(args_input[2])) is dict:
            kwargs = eval(args_input[2])
            args_input = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args_input.append(k)
                args_input.append(v)
        else:  # isolate args_input
            args_input = args_input[2]
            if args_input and args_input[0] == '\"':  # check for quoted arg
                second_quote = args_input.find('\"', 1)
                att_name = args_input[1:second_quote]
                args_input = args_input[second_quote + 1:]

            args_input = args_input.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args_input[0] != ' ':
                att_name = args_input[0]
            # check for quoted val arg
            if not att_name and args_input[0] != ' ':
                att_val = args_input[2][1:args_input[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args_input[2]:
                att_val = args_input[2].partition(' ')[0]

            args_input = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args_input):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args_input[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
