import re
import sys
import json
from io import StringIO as void


class Robot():


    directions = ('n', 'e', 's', 'w')

    def __init__(self, robo_name, x, y):
        self.x = x
        self.y = y
        self.forward = Robot.directions[0]
        self.robo_name = robo_name
        self.history = []


    def set_robot_pos(self, new_x, new_y):
        self.x = new_x
        self.y = new_y


    def reset_robot(self):
        self.__init__(self.robo_name, 0, 0)

    def add_if_safe(self, current_pos, dist_to_go, _range):
        '''
        returns the second expression to a two-expression addition
        sum depending on whether the sum as a coordinate is within
        the safe zone range
        '''

        if (current_pos + dist_to_go) not in range(-_range, (_range+1)):
            print(f"{self.robo_name}: Sorry, I cannot go outside my safe zone.")
            return 0
        return dist_to_go


    def subtract_if_safe(self, current_pos, dist_to_go, _range):
        '''
        returns the second expression to a two-expression 
        subtraction sum depending on whether the sum
        as a coordinate is within
        the safe zone range
        '''

        if (current_pos - dist_to_go) not in range(-_range, (_range+1)):
            print(f"{self.robo_name}: Sorry, I cannot go outside my safe zone.")
            return 0
        return dist_to_go


    def move_forward(self, distance):

        old_y = self.y
        old_x = self.x
        if self.forward == Robot.directions[0]:
            self.y += self.add_if_safe(self.y, distance, 200)
        elif self.forward == Robot.directions[1]:
            self.x += self.add_if_safe(self.x, distance, 100)
        elif self.forward == Robot.directions[2]:
            self.y -= self.subtract_if_safe(self.y, distance, 200)
        else:
            self.x -= self.subtract_if_safe(self.x, distance, 100)
        if (self.x != old_x) or (self.y != old_y):
            print(f" > {self.robo_name} moved forward by {distance} steps.")
        elif (distance == 0):
            print(f" > {self.robo_name} moved forward by {distance} steps.")
        return [self.x,self.y]


    def move_back(self, distance):

        old_y = self.y
        old_x = self.x
        if self.forward == Robot.directions[0]:
            self.y -= self.subtract_if_safe(self.y, distance, 200)
        elif self.forward == Robot.directions[1]:
            self.x -= self.subtract_if_safe(self.x, distance, 100)
        elif self.forward == Robot.directions[2]:
            self.y += self.add_if_safe(self.y, distance, 200)
        else:
            self.x += self.add_if_safe(self.x, distance, 100)
        if (self.x != old_x) or (self.y != old_y):
            print(f" > {self.robo_name} moved back by {distance} steps.")
        elif (distance == 0):
            print(f" > {self.robo_name} moved forward by {distance} steps.")
        return [self.x,self.y]


    def turn_right(self):
        if self.forward == 'n':
            self.forward = 'e'
        elif self.forward == 'e':
            self.forward = 's'
        elif self.forward == 's':
            self.forward = 'w'
        else:
            self.forward = 'n'

        return(f" > {self.robo_name} turned right.")


    def turn_left(self):
        if self.forward == 'n':
            self.forward = 'w'
        elif self.forward == 'e':
            self.forward = 'n'
        elif self.forward == 's':
            self.forward = 'e'
        else:                   #shaky logic. Originally meant for turn right functions
            self.forward = 's'

        return(f" > {self.robo_name} turned left.")


    def sprint(self, dist):
        if dist == 0:
            return dist
        self.move_forward(dist)
        return self.sprint(dist - 1)


    def set_hist(self, command, quantifier):
        self.history.append((command, quantifier))

    def get_hist_len(self):
        return len(self.history)

    def filter_replay_text(self):
        hist_list = (x for x in self.history)
        moves_list = {'forward', 'back', 'left', 'right', 'sprint'}
        movements = (move for move in hist_list if move[0] in moves_list)
        return movements


    def get_replay_cmd_list(self) -> list:
        moves = Robot.filter_replay_text(self)
        moves = [str(move[0])+' '+str(move[1]) for move in moves]
        return [commands.strip() for commands in moves]
        #return '\n'.join(moves)


    def get_robo_location(self):
        return (f" > {self.robo_name} now at position ({self.x},{self.y}).")


def set_name() -> str:
    '''
    Prompts and returns the robot's name
    form the user
    '''

    name = str()
    while not name:
        name =  input('What do you want to name your robot? ')
    print(f'{name}: Hello kiddo!')
    return name


def get_command(robot, list_of_commands) -> list:

    '''
    Prompts for input, returns list and boolean
    '''
    complain = False
    go_on = True
    cmd = input(f'{robot.robo_name}: What must I do next? ')
    lst_cmd = (cmd.casefold()).split()
    if lst_cmd[0] == 'replay':
        ##NEED  A LIST OF WORDS#######
        # word_args = [arg for arg in lst_cmd[1:] if arg.isalpha()]
        word_args = [arg for arg in lst_cmd[1:] if not arg.isdigit()]
        impurities = set(word_args).difference({'reversed', 'silent'})
        pattern = re.compile(r'\b\d{1,YZ}\-\d{1,YZ}\b'.replace('YZ', str(robot.get_hist_len())))
        temp_list = re.findall(pattern, ' '.join(impurities))
        impurities = impurities.difference(set(temp_list))
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>IMPORTANT STUFF<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # for val in lst_cmd:
        #     if val.isdigit():
        #         val += 1
        #Decrements all standalone integers
        lst_cmd = [(str(int(val) - 1) if val.isdigit() else val) for val in lst_cmd]
        #NOW I just need code to change range values... maybe idk
        # lst_cmd = [[(str(int(char) - 1) if char.isdigit() else char) for char in val] for val in lst_cmd]
        # lst_cmd = [''.join(value) for value in lst_cmd]
        # print(f'This is your list:\n{lst_cmd}')
        #if impurities are present, print I DO NOT UNDERSTAND
        if not (len(impurities) == 0):
            complain = True
    elif lst_cmd[0] in list_of_commands:
        return lst_cmd[:2], go_on
    else:
        complain = True

    out = (f"{robot.robo_name}: Sorry, I did not understand '{cmd}'.")
    #print out if necessary, else do nothing...
    print(out) if complain else None
    go_on = False if complain else True
    return lst_cmd, go_on


def set_help(commands, command=None, message=None, cmd_dict={}) -> dict:
    '''
    Adds the command and description
    to a dictionary as the key and value
    respectively
    '''

    ''' populate dictionary if it's empty'''
    # if (not len(cmd_dict)) or (not cmd_dict):       #True == 1 and False == 0 so if len == 0 then : if (not False) ->if True... Condition for empty dict
    if not cmd_dict:
        help_dict = {}.fromkeys(commands)         #overwrites all values
    else:           #if cmd_dict is not empty
        help_dict = cmd_dict.copy()
        for key in commands:
            if not (key in cmd_dict):       #if command[member] is not a key in cmd_dict() then help_dict[member] is created
            # If message arg is given, use it, else, do this:
                help_dict[key] = None

    if (type(command) != None and type(message) != None):
    # if command and message:
        help_dict[command] = message
    return help_dict


def show_help(help_dict) -> str:
    '''
    Returns information on available commans and
    their descriptions
    '''

    result = 'I can understand these commands:'
    for key, value in help_dict.items():
        if key == 'off':
            key = 'off '
        result += f"\n{key.upper()} - {value}"

    return result


def prep_for_replay(robot, *args):
    '''
    A processor function that is passed the cli arguments
    and calls replay with the necessary data and metadata
    '''

    if ('reversed' in args) and ('silent' in args):
        modifier = 'both'
    elif 'reversed' in args:
        modifier = 'reversed'
    elif 'silent' in args:
        modifier = 'silent'
    else:
        modifier = None

    i_cmd = [val for val in args if val.isdigit()]
    #set replace 'YZ' with the length of the history list
    pattern = re.compile(r'\b\d{1,YZ}\-\d{1,YZ}\b'.replace('YZ', str(robot.get_hist_len())))
    i_range = re.findall(pattern, ' '.join(args))
    if i_cmd != []:
        i_cmd = int(i_cmd[0])
        replay_type = 'specific'
    elif i_range != []:
            i_range = [int(num) for num in i_range[0].split('-')]
            if i_range[0] < i_range[1]:
                i_range[0], i_range[1] = i_range[1], i_range[0]
            i_range = tuple(i_range)
            replay_type = 'range'
    else:
        replay_type = 'normal'

    replay(bot=robot, mods=modifier, kind=replay_type, cmd_range=i_range, cmd_num=i_cmd)


def replay(*args, **kwargs):

    ''' commands is a list of command strings, exec_cmd expects a list of strings '''

    bot  = kwargs.get('bot')
    commands = bot.get_replay_cmd_list()
    mods = kwargs.get('mods')
    kind = kwargs.get('kind')
    cmd_range = kwargs.get('cmd_range')
    cmd_num = kwargs.get('cmd_num')


    def play(commands, cmd_range=cmd_range):

        '''
        cmd_range comes in as a tuple of two integers,
        but is turned into a list of the commands to be replayed
        '''

        #e.g replay 6
        if kind == 'specific':
            cmd_range = commands[cmd_num:]

        #e.g replay 3-1
        elif kind == 'range':
            sum = cmd_range[0] - cmd_range[1] 
            cmd_range = commands[cmd_range[1]- 1:cmd_range[1] + sum - 1]

        #e.g replay
        elif kind == 'normal':
            cmd_range = commands

        for cmd in cmd_range:
            exec_cmd(cmd.split(), bot, True)
            print(bot.get_robo_location())

        return len(cmd_range)


    def reversed():
        i_played = play(commands[::-1])
        print(f" > {bot.robo_name} replayed {i_played} commands in reverse.")

    def silent(cmds, mods='silent'):
        old_out = sys.stdout
        sys.stdout = void()
        i_played = play(cmds)
        sys.stdout = old_out
        silent = (f" > {bot.robo_name} replayed {i_played} commands silently.")
        both = (f" > {bot.robo_name} replayed {i_played} commands in reverse silently.")
        print(both if mods == 'both' else silent)

    if mods == 'both':
        if cmd_range:
            silent(commands[cmd_range[0]:cmd_range[1]:-1], mods)
        else:
            silent(commands[::-1], mods)
    elif mods == 'silent':
        silent(commands)
    elif mods == 'reversed':
        reversed()
    else:
        i_played = play(commands)
        print(f" > {bot.robo_name} replayed {i_played} commands.")


def exec_cmd(command, robot, replay=False):
    '''
    calls the function passed as a parameter
    and adds it to the command history, if replay mode if False
    '''

    cmd = command[0]
    dist = ''
    if (len(command) > 1) and (cmd != 'replay'):
        if (type(command[1]) is str) and (command[1].isdigit()):
            dist = int(command[1])
        elif type(command[1]) is int:
            dist = command[1]
        

    if cmd == 'forward':
        Robot.move_forward(robot, dist)
    elif cmd == 'back':
        Robot.move_back(robot, dist)
    elif cmd == 'right':
        print(Robot.turn_right(robot))
    elif cmd == 'left':
        print(Robot.turn_left(robot))
    elif cmd == 'sprint':
        Robot.sprint(robot, dist)
    elif cmd == 'replay':
        args = command[1:]
        prep_for_replay(robot, *args)

    if not replay:
        robot.set_hist(cmd, dist)


def robot_start():
    '''
    entry point of script
    '''

    name = set_name()
    list_of_commands = ['off', 'help', 'forward', 'back', 'right', 'left', 'sprint', 'replay']
    robot_1 = Robot(name, 0, 0)
    #first call of set_help needs and ititializing dict
    help_dict = set_help(list_of_commands, 'off', 'Shut down robot')
    #for best results, pass the returned dict as second arg
    help_dict = set_help(list_of_commands, 'help', 'provide information about commands', help_dict)
    help_dict = set_help(list_of_commands, 'forward', 'move the robot forward', help_dict)
    help_dict = set_help(list_of_commands, 'back', 'move the robot backwards', help_dict)
    help_dict = set_help(list_of_commands, 'right', 'turns robot 90 degrees to the right', help_dict)
    help_dict = set_help(list_of_commands, 'left', 'turns robot 90 degrees to the left', help_dict)
    help_dict = set_help(list_of_commands, 'sprint', 'robot sprints recursively', help_dict)
    movements = ', '.join(list_of_commands[:-2])
    help_dict = set_help(list_of_commands, 'replay',
    f'Redo all previous movement commands, such as {movements} and sprint',
    help_dict)
    while True:
        command, go_on = get_command(robot_1, list_of_commands)
        if command[0] == 'off':
            print(f'{name}: Shutting down..')
            robot_1.reset_robot()
            return
        elif command[0] == 'help':
            print(show_help(help_dict))
            print(f"\n{Robot.get_robo_location(robot_1)}")
        elif go_on and (command[0] in list_of_commands[2:]):
            exec_cmd(command, robot_1)
            print(robot_1.get_robo_location())

if __name__ == '__main__':
    '''
    for a quick hard code-style test.
    copy and paste when the robot asks for a name
    '''
    if '-v' in sys.argv:
        print('CASEE\nback 6\nright\nforward 3\nleft\nsprint 4\nright\nback 13\nreplay silent\nreplay 1-4 silent\noff\n')
    robot_start()