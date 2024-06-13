class Message():
    def __init__(self, id, content, sender_id, receiver_id):
        self.id = id
        self.content = content
        # self.timestamp = timestamp
        self.sender_id = sender_id
        self.receiver_id = receiver_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"User({self.id}, {self.content}, {self.sender_id}, {self.receiver_id})"
        # return f"User({self.id}, {self.content}, {self.timestamp}, {self.sender_id}, {self.receiver_id})"
