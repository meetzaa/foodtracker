class Controller:
    def __init__(self, root):
        self.root = root
        self.pages = {}
        self.current_page = None

    def show_page(self, page_name, *args):
        page = self.pages[page_name]
        page.lift()
        if args:
            page.update(*args)

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
