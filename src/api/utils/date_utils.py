import dateparser

def format_date(date_str):
    """Format a human-readable date string into dd/mm/YYYY format."""
    try:
        parsed_date = dateparser.parse(date_str)
        if not parsed_date:
            return "Invalid date"
        return parsed_date.strftime("%d/%m/%Y")
    except Exception as e:
        return "Invalid date"