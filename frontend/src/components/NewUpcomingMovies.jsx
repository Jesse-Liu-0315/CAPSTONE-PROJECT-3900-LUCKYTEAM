import React from 'react';
import PropTypes from 'prop-types';

const NewUpcomingMovies = (props) => {
  const jumpToMovieDetail = () => {
    window.location = `/movie/${props.movieId}/${props.movieName.replaceAll(' ', '_')}`;
  }

  return (
    <>
      <div className='col-auto' style={{ textAlign: 'center', cursor: 'pointer', padding: '0px'}} >
          <img src={props.moviePicture} alt="Movie" style={{ width: '190px', height: '250px' }} onClick={jumpToMovieDetail}/>
          <p className="card-text"><small className="text-muted" onClick={jumpToMovieDetail}>{props.movieName}</small></p>
      </div>
    </>
  );
}

NewUpcomingMovies.propTypes = {
  moviePicture: PropTypes.string,
}

export default NewUpcomingMovies;
