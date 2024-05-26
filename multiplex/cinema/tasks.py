from celery import shared_task


@shared_task
def rewrite_movie_status(movie_id, new_status):
    from cinema.models import Movie
    movie = Movie.objects.get(id=movie_id)
    movie.status = new_status
    movie.save()


@shared_task
def delete_session(session_id):
    from cinema.models import Session
    session = Session.objects.filter(pk=session_id) #.prefetch_related('tickets')
    #session.tickets.delete()
    session.delete()