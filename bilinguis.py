import os.path
import codecs
import random
import copy
import sqlite3

dbname = "turkish.db"
filelocation = "C:\\Users\\akasen2\\Documents"
available_lessons = [10, 11, 12, 13]


class Dialogue:
    @staticmethod
    def choice(description, dict):
        print description
        selection = raw_input()
        for key, value in dict.items():
            if key == selection:
                return value
        else:
            print "No match. Prompt again..."
            return Dialogue.choice(description, dict)

    @staticmethod
    def parse_choices(description, options_num):
        print description
        selection_string = raw_input()
        if options_num != len(selection_string):
            print "Length of string does not match. Input again."
            return Dialogue.parse_choices(description, options_num)
        choices = []
        for i in range(options_num):
            if selection_string[i] in ["0", "1"]:
                choices.append(int(selection_string[i]))
            else:
                print "Each option must be 0 or 1. Input again."
                return Dialogue.parse_choices(description, options_num)
        else:
            return tuple(choices)



class App:
    def __init__(self):
        self.main()

    def main(self):
        print "Welcome to this turkish lessons."
        mode = Dialogue.choice("Choose mode. [e/w]", {"w":"words", "e":"examples"})
        number = Dialogue.choice("Choose lesson number from {}".format(", ".join([str(i) for i in available_lessons])), {str(i):str(i) for i in available_lessons})
        filename = "Lesson" + number + "_" + mode + ".txt"
        try:
            l = LessonFile(filename, filelocation)
        except:
            print "Wrong input. exits..."
            exit(1)
        options = Dialogue.parse_choices("Choose options like \"0011\"(input=0, random=0, reverse=1, repeat=1)", 4)
        l.parse_content()
        p = Practice()
        p.contents = l.pairs
        p.practice(*options)
        print "You finished the lesson. Good job!"
        Dialogue.choice("Do you like to practice again? [y/n]", {"y": self.main, "n": exit})()


class FileBase:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.content = ""
        self.pairs = []
        if not os.path.isfile(os.path.join(self.location, self.name)):
            print "File is missing. Exits..."
            exit(1)
        else:
            self.open()

    def open(self):
        with codecs.open(os.path.join(self.location, self.name), "r", "utf-8") as f:
            self.content = f.read()

    def parse_content(self):
        lines = self.content.split("\n")
        length = len(lines)
        i = 0
        while True:
            self.pairs.append([lines[i], lines[i + 1].lstrip("\t")])
            if i >= length - 2:
                break
            i += 2


class LessonFile(FileBase):
    def __init__(self, name, location):
        FileBase.__init__(self, name, location)


class WordFile(FileBase):
    def __init__(self, name, location):
        FileBase.__init__(self, name, location)


class Pairs(object):
    def __init__(self, pairs):
        self.pairs = pairs

    def random(self):
        result = []
        for i in range(len(self.pairs)):
            choice = random.choice(self.pairs)
            result.append(choice)
            self.pairs.remove(choice)
        self.pairs = result

    def reverse(self):
        for pair in self.pairs:
            pair.reverse()


class Practice:
    def __init__(self):
        self.contents = []

    def practice(self, input, random, reverse, repeat):
        practice_contents = Pairs(copy.deepcopy(self.contents))
        if random != 0:
            practice_contents.random()
        if reverse != 0:
            practice_contents.reverse()
        if input != 0:
            self.input_practice(practice_contents.pairs, repeat)
        else:
            self.show(practice_contents.pairs, repeat)

    def show(self, contents, repeat=0):
        print "If you answer correctly, just press enter. Otherwise input something." if repeat\
            else "Press enter to continue to the next word."
        remains = []
        for c in contents:
            print c[0],
            raw_input()
            print c[1]
            if repeat == 1 and raw_input():
                remains.append(c)
        if repeat == 1 and remains != []:
            print "Another round..."
            self.show(remains, repeat=1)

    def input_practice(self, contents, repeat=0):
        print "Input the counterpart of the shown. Upper/Lower does not matter."
        remains = []
        for c in contents:
            print c[0]
            input = raw_input()
            if input.lower().strip() == c[1].lower().strip():
                print "Correct."
            else:
                print u"Not correct. The answer is {}.".format(c[1])
                remains.append(c)
                # print "If you have an objection, input \"objection\"
        if repeat == 1 and remains != []:
            print "Another round..."
            self.input_practice(remains, repeat=1)


if __name__ == '__main__':
    a = App()
