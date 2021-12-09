use movie_lens_db;

select rating, title from rating
inner join movie on rating.movieId = movie.movieId
WHERE rating.userId = 1
limit 1;


use lect_db;

drop table individualRating if exist;

create table individualRating (
    tt int,
    uid int,
    rating float(3, 2),
    primary key (tt, uid),
    FOREIGN KEY (tt) REFERENCES movie(tt),
    FOREIGN KEY (uid) REFERENCES staff(uid)
)