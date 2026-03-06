from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt

from .auth import SECRET_KEY, ALGORITHM

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: str = Depends(oauth2_scheme)):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload
    except jwt.ExpiredSignatureError:

        raise HTTPException(status_code=401, detail="Token expired")
    except:

        raise HTTPException(status_code=401, detail="Invalid token")



def get_admin_user(user=Depends(get_current_user)):

    if user["role"] != "admin":

        raise HTTPException(status_code=403, detail="Admins only")

    return user