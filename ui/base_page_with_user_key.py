from .base_page import BasePage

class BasePageWithUserKey(BasePage):
    def __init__(self, master, controller, user_key):
        super().__init__(master, controller)
        self.user_key = user_key

    def update_user_key(self, user_key):
        self.user_key = user_key