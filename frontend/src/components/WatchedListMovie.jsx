import React from 'react';
import PropTypes from 'prop-types';
import Rating from '@mui/material/Rating';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import makeRequest from '../helpers/Fetch';

const WatchedListMovie = (props) => {

  const jumpToMovieDetail = () => {
    window.location = `/movie/${props.movieId}/${props.movieName.replaceAll(' ', '_')}`;
  }

  const deleteButton = async () => {
    const body = {
      movie_id: parseInt(props.movieId),
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
    }
    try {
      await makeRequest('/watchedlist/remove', 'POST', body);
      props.setSuccessOpen(true);
      props.setSuccessMessage('Delete a watched movie success');
      const newWishResult = props.watchedResult.filter(value => value.movie_id !== props.movieId);
      props.setWatchedResult(newWishResult);
    } catch (error) {
      props.setErrorOpen(true);
      props.setErrorMessage(error);
    }
  }

  return (
    <>
      <div className="row" style={{ marginLeft: '20px' }}>
        <div className="col-auto" style={{ padding: '0px' }}>
          <img src={props.moviePicture} className="img-fluid rounded-start" alt="Movie" style={{ height: '180px', cursor: 'pointer' }} onClick={jumpToMovieDetail} />
        </div>
        <div className="col-8" style={{ padding: '0px' }}>
          <div className="card-body" style={{ position: 'relative', height: '100%', padding: '0px', paddingLeft: '5px' }}>
            <h5 style={{ cursor: 'pointer' }} className="card-title" onClick={jumpToMovieDetail}>{props.movieName}</h5>
            <p style={{ marginBottom: '0px' }}>{props.movieDescription}</p>
            <Rating precision={0.1} value={props.movieRating} readOnly style={{ position: 'absolute', bottom: 20 }} />
            <p className="card-text"><small className="text-muted" style={{ position: 'absolute', bottom: 0 }}>{props.movieReview} Reviews</small></p>
          </div>
        </div>
        <div className="col justify-content-end" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <IconButton size="large" aria-label="delete" onClick={deleteButton}>
            <DeleteIcon fontSize="large" />
          </IconButton>
        </div>
      </div>
      <hr/>
    </>
  );
}

WatchedListMovie.propTypes = {
  setErrorOpen: PropTypes.func,
  setErrorMessage: PropTypes.func,
  setSuccessOpen: PropTypes.func,
  setSuccessMessage: PropTypes.func,
  watchedResult: PropTypes.array,
  setWatchedResult: PropTypes.func,
  movieId: PropTypes.number,
  moviePicture: PropTypes.string,
  movieName: PropTypes.string,
  movieDescription: PropTypes.string,
  movieRating: PropTypes.number,
  movieReview: PropTypes.number,
}

export default WatchedListMovie;
