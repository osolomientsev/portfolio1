from fastapi import HTTPException


def check_permissions(obj, current_user):
    if hasattr(obj, "user_id"):
        owner_id = obj.user_id
    elif hasattr(obj, "id"):
        owner_id = obj.id
    else:
        raise HTTPException(status_code=500, detail="Object has no owner field")

    if owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")