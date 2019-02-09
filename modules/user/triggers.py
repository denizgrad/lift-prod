

class UserTrigger:

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        names = [document.first_name, document.last_name]
        document.full_name = " ".join(names)
