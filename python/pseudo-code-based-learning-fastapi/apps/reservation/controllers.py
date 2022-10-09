from apps.reservation.repositories import ReservationRepository


def reservations(user):
    repository = ReservationRepository()
    return repository.findall()
