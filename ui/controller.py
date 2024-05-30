class Controller:
    def __init__(self, root):
        self.root = root
        self.pages = {}
        self.current_page = None

    def show_page(self, page_name, *args):
        if self.current_page is not None:
            self.current_page.place_forget()  # Hide the current page
        page = self.pages[page_name]
        page.lift()
        if args:
            page.update(*args)
        page.place(x=0, y=0, relwidth=1, relheight=1)
        self.current_page = page

    def add_page(self, page_name, page_class, *args):
        page = page_class(self.root, self, *args)
        self.pages[page_name] = page
        page.place(x=0, y=0, relwidth=1, relheight=1)

    def show_page_with_user_key(self, page_name, user_key):
        if page_name in self.pages:
            self.pages[page_name].update(user_key)
            self.show_page(page_name, user_key)
        else:
            print(f"Page {page_name} not found")

    def set_current_goal(self, goal):
        self.current_goal = goal