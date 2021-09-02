from fastapi import FastAPI, Path, HTTPException
from nexfil_fast import start_search
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    uname: Optional[str] = None
    dns: Optional[str] = '1.1.1.1'
    ulist: Optional[str] = None
    tout: Optional[int] = 20


@app.get('/username/{uname}')
def one_username(*, uname: str = Path(None, description='Username to search on sites'), d: Optional[str] = '1.1.1.1', tout: Optional[int] = 20):
    ''' Use get request like: http://127.0.0.1:8000/username/Alex

        Use get request with optional variables like: http://127.0.0.1:8000/username/Alex?d=8.8.8.8&tout=5

        Return json with USERNAMEs and found URLs
    '''
    return start_search(uname, ulist=None, dns=[d], tout=tout)


@app.get('/username_list/{ulist}')
def list_username(*, ulist: str = Path(None, description='Usernames to search on sites separated %'), d: Optional[str] = '1.1.1.1', tout: Optional[int] = 20):
    ''' Use get request like: http://127.0.0.1:8000/username_list/Alex%Nikol%Sam

        Use get request with optional variables like: http://127.0.0.1:8000/username_list/Alex%Nikol%Jhon?d=1.1.1.1&tout=10

        Return json with USERNAMEs and found URLs
    '''

    if len(ulist.split('%')) > 1:
        return start_search(uname=None, ulist=ulist, dns=[d], tout=tout)
    else:
        raise HTTPException(status_code=400, detail='Bad Request. Usernames must be separated by % and count of names two or more. Example: http://127.0.0.1:8000/username_list/Alex%Nikol%Sam')


@app.post('/username_data_json')
def username_data_json(item: Item):
    if item.uname is None and item.ulist is not None and len(item.ulist.split('%')) > 1:
        return start_search(uname=item.uname, ulist=item.ulist, dns=[item.dns], tout=item.tout)
    elif item.ulist is None and item.uname is not None:
        return start_search(uname=item.uname, ulist=item.ulist, dns=[item.dns], tout=item.tout)
    else:
        raise HTTPException(status_code=400, detail='Bad Request. Use one of json key uname or ulist and remove unused parameter from json. Example uname: Alex. Example ulist: Alex%Nikol%Sam')
