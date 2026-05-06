import React from 'react';
import PropTypes from 'prop-types';
import Rating from '@mui/material/Rating';

const MovieMayLike = (props) => {
  const jumpToMovieDetail = () => {
    window.location = `/movie/${props.movieId}/${props.movieName.replaceAll(' ', '_')}`;
  }

  

  return (
    <>
      <div className="row g-0">
        <div className="col-md-4">
          <img src={props.moviePicture} className="img-fluid rounded-start" alt="Movie" style={{ width: '100%',height: '100%',cursor: 'pointer' }} onClick={jumpToMovieDetail} />
        </div>
        <div className="col-md-8">
          <div className="card-body" style={{ position:'relative', height: '100%', padding: '0px', paddingLeft: '5px' }}>
            <p style={{ cursor: 'pointer', color: 'red', fontSize: '80%', fontWeight:1000 }} className="card-title" onClick={jumpToMovieDetail}>{props.movieName}</p>
            <br />
            <Rating precision={0.1} value={props.movieRating === null ? 0 : props.movieRating} readOnly style={{position:'absolute', bottom: '45%'}}/>
            <p className="card-text"><small className="text-muted" style={{ position:'absolute', bottom: 0 }}>{props.movieReview} Reviews</small></p>
          </div>
        </div>
      </div>
      <hr style={{ color: '#1565c0' }}/>
    </>
  );
}

MovieMayLike.propTypes = {
  movieId: PropTypes.number,
  moviePicture: PropTypes.string,
  movieName: PropTypes.string,
  movieRating: PropTypes.number,
  movieReview: PropTypes.number
}

export default MovieMayLike;
