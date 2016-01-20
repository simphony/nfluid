from nfluid.core.channel_assembly import ChannelAssembly
from nfluid.core.channel_element import ChannelElement


class NfluidDataManager(object):
    
    model = None
    
    def __init__(self):
        if ChannelElement.assembly is None:
            NfluidDataManager.model = ChannelAssembly()
        else:
            NfluidDataManager.model = ChannelElement.assembly
    
    @classmethod
    def exists(cls):
        return (model != None)
        
    @classmethod
    def add_piece(cls, piece):
        pass
    
    @classmethod
    def remove_piece(cls, piece):
        pass
    
    @classmethod
    def list_of_pieces(cls):
        pass
        