import sublime
import sublime_plugin
import re

VIEW_NAME = 'SVN Output'
SYNTAX = 'Packages/HypnotoadSVN/languages/SVN Output.tmLanguage'

class SvnView(sublime_plugin.EventListener):
    view = None
    def get():
        if SvnView.view is None or SvnView.view.window() is None:
            view = sublime.active_window().new_file()
            view.set_scratch(True)
            view.set_name(VIEW_NAME)
            view.set_syntax_file(SYNTAX)
            view.set_read_only(True)
            SvnView.view = view
        return SvnView.view
    def on_close(self, view):
        if view == SvnView.view:
            SvnView.view = None


def indent(text="", spaces=4):
    return " " * spaces + re.sub(r'\n', '\n' + " " * spaces, text)

def add_message(message):
    view = SvnView.get()
    view.run_command(
        'svn_view_message',
        {
            "message": message
        }
    );

def add_command(name):
    view = SvnView.get()
    view.window().focus_view(view)
    point = view.text_to_layout(view.size() - 1)
    add_message("Command: " + name)
    view.set_viewport_position(point, True)

def add_files(paths=None):
    if paths is None:
        return
    s = paths
    if isinstance(paths, list):
        s = "\n".join(paths)
    add_message("Files:\n" + indent(s))

def add_result(result):
    if result:
        add_message("Output:\n" + indent(result))

def add_error(err):
    if err:
        add_message("Error:\n" + indent(err))

def end_command():
    add_message("\n")