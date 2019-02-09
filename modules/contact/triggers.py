

class ContactTrigger:

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        names = []
        if document.name or document.surname:
            if document.name:
                names.append(document.name)
            if document.surname:
                names.append(document.surname)
            document.full_name = " ".join(names)
