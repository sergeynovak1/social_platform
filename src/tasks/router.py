from fastapi import APIRouter, BackgroundTasks, Depends

from src.auth import oauth2

from .tasks import send_email_report_dashboard

router = APIRouter(prefix="/report")


@router.get("/dashboard")
def get_dashboard_report(background_tasks: BackgroundTasks, user: int = Depends(oauth2.get_current_user)):
    # 1400 ms - Клиент ждет
    send_email_report_dashboard(user.email)
    # 500 ms - Задача выполняется на фоне FastAPI в event loop'е или в другом треде
    background_tasks.add_task(send_email_report_dashboard, user.email)
    # 600 ms - Задача выполняется воркером Celery в отдельном процессе
    send_email_report_dashboard.delay(user.email)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }
