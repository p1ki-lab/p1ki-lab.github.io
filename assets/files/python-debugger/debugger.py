import inspect
import sys


class Debugger:
    def __init__(self, commands=None, file=None):
        self.commands = iter(commands) if commands is not None else None
        self.file = file or sys.stdout
        self.breakpoints = set()
        self.functions = set()
        self.watches = []
        self.exceptions = False
        self.mode = 'step'
        self.target = None
        self.root = None
        self.active = False

    def log(self, text):
        print(text, file=self.file)

    def __enter__(self):
        self.previous = sys.gettrace()
        self.active = True
        sys.settrace(self._trace)
        return self

    def __exit__(self, exc_type, value, traceback):
        self.active = False
        sys.settrace(self.previous)
        self.root = self.target = None
        self.watches.clear()
        self.stack = []
        self.frame = None
        return False

    def _trace(self, frame, event, arg):
        if not self.active or frame.f_code.co_filename == __file__:
            return None
        if self.root is None:
            if event != 'call':
                return None
            self.root = frame
        ancestor = frame
        while ancestor is not None and ancestor is not self.root:
            ancestor = ancestor.f_back
        if ancestor is None:
            return None
        if event not in ('call', 'line', 'return', 'exception'):
            return self._trace
        reasons = []
        for watch in self.watches:
            expression, watched_frame, previous = watch
            if watched_frame is frame:
                current = self.watch_value(expression, frame)
                if current != previous:
                    reasons.append(f'watch {expression}: {previous} -> {current}')
                    watch[2] = current
        if event == 'line' and (frame.f_code.co_filename, frame.f_lineno) in self.breakpoints:
            reasons.append('line breakpoint')
        if event == 'call' and self.functions.intersection(
            (frame.f_code.co_name, frame.f_code.co_qualname)
        ):
            reasons.append('function breakpoint')
        if event == 'exception' and self.exceptions:
            reasons.append(f'{arg[0].__name__}: {arg[1]}')
        reached = False
        if event != 'exception':
            if self.mode == 'step':
                reached = True
            elif self.target is not None and self.mode in ('next', 'until', 'finish'):
                ancestor = frame
                while ancestor is not None and ancestor is not self.target:
                    ancestor = ancestor.f_back
                if ancestor is None:
                    reached = True
            if frame is self.target:
                if self.mode == 'next':
                    reached = event in ('line', 'return')
                elif self.mode == 'finish':
                    reached = event == 'return'
                elif self.mode == 'until':
                    reached = event == 'return' or (
                        event == 'line' and frame.f_lineno > self.until_line
                    )
        if reasons or reached:
            self.frame, self.event, self.arg = frame, event, arg
            self.interact(reasons)
        if event == 'return':
            self.watches = [watch for watch in self.watches if watch[1] is not frame]
            if frame is self.root:
                self.root = None
        return self._trace if self.active else None

    def watch_value(self, expression, frame):
        try:
            return repr(eval(expression, frame.f_globals, frame.f_locals))
        except NameError:
            return '<undefined>'
        except Exception as error:
            return f'<{type(error).__name__}: {error}>'

    def interact(self, reasons):
        self.stack = []
        current = self.frame
        while current is not None:
            self.stack.append(current)
            if current is self.root:
                break
            current = current.f_back
        self.selected = 0
        detail = f' value={self.arg!r}' if self.event == 'return' else ''
        self.log(f'STOP {self.event} {self.frame.f_code.co_name}:{self.frame.f_lineno}{detail}')
        for reason in reasons:
            self.log(reason)
        while self.active:
            try:
                if self.commands is None:
                    entered = input('(debugger) ')
                else:
                    entered = next(self.commands)
                    self.log(f'(debugger) {entered}')
            except (EOFError, StopIteration):
                entered = 'quit'
            parts = entered.strip().split(maxsplit=1)
            if not parts:
                continue
            command, argument = parts[0], parts[1] if len(parts) == 2 else ''
            method = getattr(self, command + '_command', None)
            if method is None:
                self.log('ERROR unknown command; use help')
                continue
            try:
                if method(argument):
                    return
            except Exception as error:
                self.log(f'ERROR {type(error).__name__}: {error}')

    def help_command(self, argument):
        for name in sorted(dir(self)):
            if name.endswith('_command'):
                method = getattr(self, name)
                self.log(f'{name[:-8]}: {method.__doc__}')

    def print_command(self, argument):
        """print [EXPR]: inspect selected frame"""
        frame = self.stack[self.selected]
        value = eval(argument, frame.f_globals, frame.f_locals) if argument else dict(frame.f_locals)
        self.log(repr(value))

    def list_command(self, argument):
        """list: show selected function source"""
        frame = self.stack[self.selected]
        lines, start = inspect.getsourcelines(frame.f_code)
        for number, source in enumerate(lines, start):
            marker = '>' if number == frame.f_lineno else ' '
            self.log(f'{marker}{number} {source.rstrip()}')

    def break_command(self, argument):
        """break [LINE|FUNCTION]: set or list breakpoints"""
        if not argument:
            self.log(repr(sorted(self.breakpoints)) + ' ' + repr(sorted(self.functions)))
        elif argument.isdecimal():
            number = int(argument)
            frame = self.stack[self.selected]
            lines, start = inspect.getsourcelines(frame.f_code)
            if number not in range(start, start + len(lines)):
                raise ValueError('line must be in selected function')
            self.breakpoints.add((frame.f_code.co_filename, number))
        elif all(part.isidentifier() for part in argument.split('.')):
            self.functions.add(argument)
        else:
            raise ValueError('use break LINE or FUNCTION')

    def delete_command(self, argument):
        """delete [LINE|FUNCTION|EXPR]: remove breakpoint/watch"""
        if not argument:
            self.breakpoints.clear()
            self.functions.clear()
            self.watches.clear()
        else:
            if argument.isdecimal():
                self.breakpoints.discard((self.stack[self.selected].f_code.co_filename, int(argument)))
            self.functions.discard(argument)
            self.watches = [watch for watch in self.watches if watch[0] != argument]

    def resume(self, mode, argument):
        if argument:
            raise ValueError(f'{mode} takes no arguments')
        self.mode, self.target = mode, self.frame
        return True

    def step_command(self, argument):
        """step: stop at next call/line/return"""
        return self.resume('step', argument)

    def continue_command(self, argument):
        """continue: run until another stop condition"""
        return self.resume('continue', argument)

    def next_command(self, argument):
        """next: run over nested calls"""
        return self.resume('next', argument)

    def finish_command(self, argument):
        """finish: stop at current function return"""
        return self.resume('finish', argument)

    def until_command(self, argument):
        """until [LINE]: run to a greater line or return"""
        number = int(argument) if argument else self.frame.f_lineno
        if number < 1:
            raise ValueError('line must be positive')
        self.until_line = number
        return self.resume('until', '')

    def where_command(self, argument):
        """where: show call stack, innermost first"""
        for index, frame in enumerate(self.stack):
            marker = '>' if index == self.selected else ' '
            self.log(f'{marker}#{index} {frame.f_code.co_name} {frame.f_code.co_filename}:{frame.f_lineno}')

    def up_command(self, argument):
        """up: inspect caller frame"""
        if self.selected + 1 >= len(self.stack):
            raise ValueError('already at outermost frame')
        self.selected += 1
        self.where_command('')

    def down_command(self, argument):
        """down: inspect inner frame"""
        if self.selected == 0:
            raise ValueError('already at innermost frame')
        self.selected -= 1
        self.where_command('')

    def watch_command(self, argument):
        """watch EXPR: stop when a frame-bound expression changes"""
        if not argument:
            raise ValueError('use watch EXPR')
        compile(argument, '<watch>', 'eval')
        frame = self.stack[self.selected]
        self.watches = [watch for watch in self.watches if not (watch[0] == argument and watch[1] is frame)]
        self.watches.append([argument, frame, self.watch_value(argument, frame)])

    def exceptions_command(self, argument):
        """exceptions [on|off]: configure exception-event stops"""
        if argument not in ('', 'on', 'off'):
            raise ValueError('use exceptions on|off')
        if argument:
            self.exceptions = argument == 'on'
        self.log('exceptions ' + ('on' if self.exceptions else 'off'))

    def quit_command(self, argument):
        """quit: detach tracing, let target continue"""
        self.active = False
        sys.settrace(self.previous)
        return True
