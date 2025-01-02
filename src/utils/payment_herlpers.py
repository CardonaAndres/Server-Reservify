def format_ticket_payment(data : dict) -> dict:
    
    formatted_data = {}
    convert_str = {'paid_at', 'reservation_date', 'reservation_time', 'created_at'}
    
    for key, value in data.items():
        if key == 'amount':
            formatted_data[key] = float(value)
            
        elif key == 'status':
            formatted_data[key] = value.capitalize()
            
        elif key in convert_str:
            formatted_data[key] = str(value)
            
        else:
            formatted_data[key] = value
               
    return formatted_data

def format_tickets_payments(data : list) -> list:
    return [format_ticket_payment(ticket) for ticket in data]
    