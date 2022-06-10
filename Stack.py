class Stack:
    def __init__(self):
        self.__stack = []
        self.__stack_ix = 0

    def undo(self):
        if self.__stack:
            self.__stack_ix = max(0, self.__stack_ix - 1)
            return self.__stack[self.__stack_ix]

    def redo(self):
        if self.__stack:
            self.__stack_ix = min(len(self.__stack) - 1, self.__stack_ix + 1)
            return self.__stack[self.__stack_ix]

    def clear(self):
        self.__stack.clear()
        self.__stack_ix = 0

    def add(self, x):
        if self.__stack_ix < len(self.__stack) - 1:
            self.__stack = self.__stack[0:self.__stack_ix + 1]

        self.__stack.append(x)
        self.__stack_ix += 1
