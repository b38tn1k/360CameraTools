# too drunk to do this like a sensible person. also dont have docs. ehhhhh
class GoProFriend(object):

    def __init__(self, head_file):
        self.head_file = head_file
        self.cam = head_file[:5]
        self.event = head_file[-7:-1].strip('.ts')
        self.children = [self.head_file]

    def add_child(self, child):
        self.children.append(child)

    def order_children(self):
        for child in self.children:
            index = child.find('GP0')+1
            order_flag = child[index:].strip('.ts')
            print order_flag
