from datetime import timedelta, time

def format_to_hours_minutes(delta: timedelta) -> str:
    """Convierte un objeto timedelta a una cadena de horas y minutos (HH:MM)."""
    if isinstance(delta, timedelta):
        total_seconds = int(delta.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}"
    return "00:00"  # Devuelve "00:00" si no es un timedelta válido

def format_reservation_data(reservation: dict) -> dict:
    """Formatea los campos de fecha, hora y creación de una reserva."""
    return {
        **reservation,
        'reservation_date': reservation['reservation_date'].strftime("%Y-%m-%d"),
        'reservation_time': format_to_hours_minutes(reservation['reservation_time']),
        'created_at': reservation['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    }
    
def format_dates(reservations: list[dict]) -> list[dict]:
    """Formatea las fechas de una lista de reservas."""
    return [format_reservation_data(reservation) for reservation in reservations]

def format_date(reservation: dict) -> dict:
    """Formatea los campos de fecha, hora y creación de una sola reserva."""
    return format_reservation_data(reservation)

def format_to_hours_minutes(delta: timedelta) -> str:
    """Convierte un objeto timedelta a una cadena de horas y minutos (HH:MM)."""
    if isinstance(delta, timedelta):
        total_seconds = int(delta.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}"
    return "00:00"  # Devuelve "00:00" si no es un timedelta válido

def convert_timedelta_to_time(existing_time: timedelta) -> time:
    """Convierte un objeto timedelta a un objeto time."""
    if isinstance(existing_time, timedelta):
        total_seconds = int(existing_time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return time(hour=hours, minute=minutes)
    return time()  # Devuelve un time vacío si no es un timedelta válido

