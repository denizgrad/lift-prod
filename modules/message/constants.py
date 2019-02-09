from enum import Enum


class EnumMessage(Enum):

    SISTEM = 1
    KULLANICI = 2
    # Mesaj tipi 3 değerinde yani ONLYMESSAGE olarak tanımlanmışsa sistem bildirimi oluşturulmaz
    ONLYMESSAGE = 3
