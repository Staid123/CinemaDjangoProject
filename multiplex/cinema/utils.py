

from cinema.models import Session


def get_places(session_id):
    session = Session.objects.get(id=session_id)
    rows = [int(num) for num in range(1, int(session.hall.places / 10) + 1)]
    count_places_in_every_row = [num for num in range(1, 10)]
    row_info = {}
    for row_num in rows:
        reserved_seats = session.tickets.filter(session=session, row=row_num).values_list('place', flat=True)
        row_info[row_num] = [{
            'count_places': count_places_in_every_row,
            'reserved_seats': list(reserved_seats)
        }]
    # {row_num: [{'count_places': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'reserved_seats': [place_num, place_num]}]
    return row_info