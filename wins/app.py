import swears as sw

class app:
    """
    basic, built in menu for swears
    select layout
    save layout
    open module
        (file manager)
    MODS
    """
    def __init__(self,modName):
    def get_installed_mods():
    def display_installed_mods():
    def open_mod(name):
    def install_mod(name):
    def uninstall_mod():

class modu
    def __init__(self,modName):
        self.load_menus(modName)
        self.create_graph()
        self.start()
        pass
        #close old if necessary
        #open in location
        #auto open links
    def load_menus(self,modName):
        pass
    def start():
    def open_menu(self,num):
        self.MENUS[num].open()
    def close_menu(num):
        self.MENUS[num].close()
        #restore parent
        #close links
        #restore previous format
    def restore_parent(num):
    def close_children(num):
    def parse_location(num):
        # parent
        # empty/null
        # nearest
        # left
        # right
        # up
        # down
        # (number)
        # (format)
        pass
    def create_graph():
        pass

class menu
    """
      parent
      children - no auto close
      links    - auto close
      num
      node
      location
      auto_open
      text
      commands
    """
    def __init__(self,modName):
    def open
    def print_text
