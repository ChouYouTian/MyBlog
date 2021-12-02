
from typing import overload


@overload
def ttt(val:int):
    """
    dcsscsdcds
    sdcd
    sdcsd
    csdcs
    """
 
    

@overload
def ttt(val:str,id:int):
    '''
    kk
    kk
    kk
    kk
    '''


def ttt(*args,**kargs):
    print(args)
    print(kargs)

    if isinstance(args[0],int):
        return args[0]
    
    if isinstance(args[0],str):
        return args

    return None



print(ttt(id=123))