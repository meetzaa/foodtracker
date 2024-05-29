class Controller:
    def __init__(self, root):
        self.root = root
        self.pages = {}

    def add_page(self, page_name, page_class, *args):
        if args:
            page = page_class(self.root, self, *args)
        else:
            page = page_class(self.root, self)
        self.pages[page_name] = page
        page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name, *args):
        page = self.pages.get(page_name)
        if args and hasattr(page, 'update_user_key'):
            page.update_user_key(*args)
        page.tkraise()
