from typing import List

from wcferry import Wcf


class ContactsBase:
    def __init__(self, wcf: Wcf):
        self.wcf = wcf
        self._counts = self.wcf.query_sql("MicroMsg.db", "SELECT COUNT(*) FROM Contact;")[0]["COUNT(*)"]
        self._offset = 10
        self._all_contacts = self.__get_all_contacts()

    def __get_all_contacts(self):
        """
        If accounts are too many, will cause wcf out of memory, get them by offsets
        """

        page = int(self._counts / self._offset)
        remains = self._counts % self._offset
        contacts = list()
        for i in range(page):
            contact = self.wcf.query_sql("MicroMsg.db", f"SELECT * FROM Contact "
                                                        f"LIMIT {self._offset} "
                                                        f"OFFSET {i * self._offset};")
            contacts.extend(contact)
        contacts.extend(self.wcf.query_sql("MicroMsg.db", f"SELECT * FROM Contact "
                                                          f"LIMIT {remains} "
                                                          f"OFFSET {page * self._offset};"))
        return contacts


class ChatRoom:
    def __init__(self, room_code: str, room_name: str):
        """
        room_code: unique code for every chat room, e.g. 111111@chatroom
        room_name: the real name of the chat room
        """
        self.room_code = room_code
        self.room_name = room_name


class ChatRooms(ContactsBase):
    def __init__(self, wcf: Wcf):
        super().__init__(wcf=wcf)
        self.__chat_rooms = self.__load_chat_rooms()

    def __load_chat_rooms(self) -> List[ChatRoom]:
        """
        Load all chat rooms into self
        """
        chat_rooms = list()
        contacts = self._all_contacts
        for contact in contacts:
            if contact["ChatRoomNotify"] != 1:
                continue
            room_code = contact["UserName"]
            room_name = contact["NickName"]
            chat_rooms.append(ChatRoom(room_code=room_code, room_name=room_name))
        return chat_rooms

    def get_chat_rooms(self) -> List[ChatRoom]:
        """
        return all chat rooms
        """
        return self.__chat_rooms

    def update_chat_rooms(self):
        """
        update/fresh the chat rooms list
        """
        self.__chat_rooms = self.__load_chat_rooms()


class Contact:
    def __init__(self, contact_code: str, alias: str, nick_name: str, type_number: int):
        """
        contact_code: unique contact code
        alias: alias of contact
        nick_name: the nickname of a contact
        type_number: used for check if it's a friends or comes from a room
        """
        self.contact_code = contact_code
        self.alias = alias
        self.nick_name = nick_name
        self.is_friend = True if type_number == 0 else False


class Contacts(ContactsBase):
    def __init__(self, wcf: Wcf):
        super().__init__(wcf=wcf)
        self.__contacts = self.__load_contacts()

    def __load_contacts(self) -> List[Contact]:
        """
        load contacts to self
        """
        contacts_result = list()

        contacts = self._all_contacts
        for contact in contacts:
            type_number = contact["Type"]
            if type_number != 0 and type_number != 4:
                # type 0 -> friends, type 1 internal account, type 2 group
                continue
            contact_code = contact["UserName"]
            alias = contact["Alias"]
            nick_name = contact["NickName"]
            contacts_result.append(Contact(contact_code=contact_code,
                                           alias=alias,
                                           nick_name=nick_name,
                                           type_number=type_number))
        return contacts_result

    def get_contacts(self) -> List[Contact]:
        """
        get contacts
        """
        return self.__contacts

    def update_contacts(self):
        """
        update contacts information
        """
        self.__contacts = self.__load_contacts()


class ContactInfo:
    def __init__(self, wcf: Wcf):
        self.wcf = wcf
        counts: int = self.wcf.query_sql("MicroMsg.db", "SELECT COUNT(*) FROM Contact;")[0]["COUNT(*)"]
        offset = 4
        page = int(counts / offset)
        remains = counts % offset
        contacts = list()
        for i in range(page):
            contact = self.wcf.query_sql("MicroMsg.db", f"SELECT * FROM Contact LIMIT {offset} OFFSET {i * offset};")
            contacts.extend(contact)
        contacts.extend(
            self.wcf.query_sql("MicroMsg.db", f"SELECT * FROM Contact LIMIT {remains} OFFSET {page * offset};"))
        ...

        contacts = self.wcf.query_sql("MicroMsg.db", "SELECT * FROM Contact;")
        chatroom = self.wcf.query_sql("MicroMsg.db", "SELECT * FROM ChatRoom;")

        dbs = []
        tables = []
        for db in self.wcf.get_dbs():
            [tables.append(table) for table in self.wcf.get_tables(db)]
        infos = dict()
        for table in tables:
            table_name = table["name"]
            if table_name in [
                "BizInfo",
                "BizProfileV2",
            ]:
                continue
            infos[table_name] = (self.wcf.query_sql("MicroMsg.db", f"SELECT * FROM {table_name}"))

        ...


if __name__ == "__main__":
    wcf = Wcf(debug=True)
    rooms = ChatRooms(wcf=wcf).get_chat_rooms()
    contacts = Contacts(wcf=wcf).get_contacts()
    ...
