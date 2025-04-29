from fastapi import HTTPException

def check_role(project, current_user):
    if project.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to modify this project")