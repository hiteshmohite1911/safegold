from fastapi import Depends, HTTPException
from routers.Auth import get_current_user


# dependency for delete access
def delete_access(token=Depends(get_current_user)):
    if token["role"] != 1:
        raise HTTPException(401, "Access denied")
