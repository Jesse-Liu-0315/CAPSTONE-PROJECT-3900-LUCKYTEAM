import React from 'react';
import PropTypes from 'prop-types';
import Rating from '@mui/material/Rating';
import defaultPhoto from '../user_profile_default.png'
import { Button } from '@mui/material';
import makeRequest from '../helpers/Fetch';
import Chip from '@mui/material/Chip';

const RecentReview = (props) => {
  const [numLike, setNumLike] = React.useState(props.reviewLike);
  const [numDisLike, setNumDisLike] = React.useState(props.reviewDisLike);

  const thumbsUpButton = async () => {
    const body = {
      movie_id: parseInt(props.movieId),
      review_id: parseInt(props.reviewId),
    }
    try {
      await makeRequest('/review/like', 'POST', body);
      setNumLike(numLike + 1);
    } catch (error) {
      props.setErrorOpen(true);
      props.setErrorMessage(error);
    }
  }

  const thumbsDownButton = async () => {
    const body = {
      movie_id: parseInt(props.movieId),
      review_id: parseInt(props.reviewId),
    }
    try {
      await makeRequest('/review/dislike', 'POST', body);
      setNumDisLike(numDisLike + 1);
    } catch (error) {
      props.setErrorOpen(true);
      props.setErrorMessage(error);
    }
  }

  const deleteButton = async () => {
    const body = {
      movie_id: parseInt(props.movieId),
      review_id: parseInt(props.reviewId),
      token: localStorage.getItem('luckyToken') === null ? '' : localStorage.getItem('luckyToken'),
    }
    try {
      await makeRequest('/review/delete', 'POST', body);
      const newOverRating = (props.overallRatingNum * props.reviews.length - props.reviewRating) / (props.reviews.length - 1);
      props.setOverallRatingNum(isNaN(newOverRating) === true ? 0 : newOverRating);
      const reviews = props.reviews.filter(value => value.review_id !== props.reviewId);
      props.setReviews(reviews);
    } catch (error) {
      props.setErrorOpen(true);
      props.setErrorMessage(error);
    }
  }

  const jumpToUserDetail = () => {
    window.location = `/otherprofile/${props.userId}`;
  }

  return (
    <>
      <div className="row">
        <div className="col-auto" style={{ marginLeft: '15px', marginRight: '5px', padding: '0px', width: '50px' }}>
          <img src={props.userPhoto === null ? defaultPhoto : props.userPhoto} style={{ width: '50px', cursor: 'pointer' }} alt="user_photo" onClick={jumpToUserDetail} />
        </div>
        <div className="col-10" style={{ padding: '0px' }}>
          <div className='row' style={{ height: '45px' }}>
            <div className='col' style={{ display: 'flex', alignItems: 'center' }}>
              <div className='row'>
                <div className="col-auto" style={{ paddingRight: '0px', display: 'flex', alignItems: 'center' }}>
                  <p style={{ margin: '0px', fontSize: '13px', padding: '0px', marginLeft: '10px', marginRight: '5px',cursor: 'pointer' }} onClick={jumpToUserDetail}>Review by {props.userName}</p>
                  {props.userTag !== null && 
                    <Chip label={props.userTag} variant="outlined" style={{ height: '24px' }} />
                  }
                </div>
                <div className="col-auto" style={{ padding: '0px', display: 'flex', alignItems: 'center', marginLeft: '15px' }}>
                  <Rating precision={0.1} value={props.reviewRating} size='small' readOnly />
                </div>
              </div>
            </div>
            <div className='col' style={{ display: 'flex', alignItems: 'center', justifyContent: 'end' }}>
              <div className='row'>
                <div className="col-auto" style={{ padding: '0px', marginRight: '20px', display: 'flex', alignItems: 'center' }}>
                  <Button variant="outlined" size='small' sx={{ padding: '0px' }} onClick={thumbsUpButton}>&#128077;{numLike}</Button>
                </div>
                <div className="col-auto" style={{ padding: '0px', display: 'flex', alignItems: 'center' }}>
                  <Button variant="outlined" size='small' sx={{ padding: '0px' }} onClick={thumbsDownButton}>&#128078;{numDisLike}</Button>
                </div>
              </div>
            </div>
          </div>
          <p style={{ margin: '0px', fontSize: '13px', marginLeft: '10px' }}>{props.reviewComment}</p>
          {props.deletePermission && 
            <div style={{ textAlign: 'end' }}>
              <Button variant="outlined" size='small' sx={{ padding: '0px' }} onClick={deleteButton}>&#128465;</Button>
            </div>
          }
          <p style={{ margin: '0px', fontSize: '13px', textAlign: 'end' }}>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Date: {props.reviewDate}</p>
        </div>
      </div>
      <hr style={{ marginTop: '0px', marginBottom: '10px' }}/>
    </>
  );
}

RecentReview.propTypes = {
  setErrorOpen: PropTypes.func,
  setErrorMessage: PropTypes.func,
  movie_id: PropTypes.number,
  review_id: PropTypes.number,
  deletePermission: PropTypes.bool,
  userId: PropTypes.number,
  userPhoto: PropTypes.string,
  userName: PropTypes.string,
  reviewRating: PropTypes.number,
  reviewComment: PropTypes.string,
  reviewDate: PropTypes.string,
  reviewLike: PropTypes.number,
  reviewDisLike: PropTypes.number,
}

export default RecentReview;
