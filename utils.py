from datetime import datetime, timedelta

def reset_daily_data(model, db):
    """Сброс ежедневных данных для всех записей модели."""
    db.execute(f"UPDATE {model.__tablename__} SET earnings_today = 0 WHERE TRUE")
    db.commit()

def calculate_time_left(next_reset_time):
    """Вычисление оставшегося времени до сброса."""
    now = datetime.utcnow()
    return max((next_reset_time - now).total_seconds(), 0)
