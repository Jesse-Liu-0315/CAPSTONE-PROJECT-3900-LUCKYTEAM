import React from 'react';
import PropTypes from 'prop-types';
import { Button } from '@mui/material';

const MostReviewedMovies = (props) => {
  const [substring, ] = React.useState(props.movieDescription.substring(0, 300));
  const [needMore, ] = React.useState(props.movieDescription.length > 300 ? true : false);
  const [moreStatus, setMoreStatus] = React.useState(false);

  const jumpToMovieDetail = () => {
    window.location = `/movie/${props.movieId}/${props.movieName.replaceAll(' ', '_')}`;
  }

  const moreButton = () => {
    setMoreStatus(!moreStatus);
  }

  return (
    <>
      <div className="row">
        <div className="card" style={{ border: '0px' }}>
          <div className="row g-0">
            <div className="col-auto">
              <img src={props.moviePicture} className="img-fluid" alt="Movie" style={{ width: '150px', height: '235px', cursor: 'pointer' }} onClick={jumpToMovieDetail} />
            </div>
            <div className="col">
              <div className="card-body" style={{ position:'relative', height: '100%', padding: '0px', paddingLeft: '5px' }}>
                <h5 style={{ cursor: 'pointer' }} className="card-title" onClick={jumpToMovieDetail}>{props.movieName}</h5>
                {moreStatus && 
                  <p style={{ margin: '0px' }}>{props.movieDescription}</p>
                }
                {!moreStatus && 
                  <p style={{ margin: '0px' }}>{substring}</p>
                }
                {needMore && 
                  <>
                    {moreStatus && 
                      <div style={{ textAlign: 'end' }}>
                        <Button onClick={moreButton}>Less</Button>
                      </div>
                    }
                    {!moreStatus &&
                      <div style={{ textAlign: 'end' }}>
                        <Button onClick={moreButton}>More</Button>
                      </div>
                    }
                  </>
                }
                <p className="card-text"><small className="text-muted" style={{ position:'absolute', bottom: 0 }}>{props.movieReview} Reviews</small></p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <hr/>
    </>
  );
}

MostReviewedMovies.propTypes = {
  movieId: PropTypes.number,
  moviePicture: PropTypes.string,
  movieName: PropTypes.string,
  movieDescription: PropTypes.string,
  movieRating: PropTypes.number,
  movieReview: PropTypes.number,
}

export default MostReviewedMovies;
