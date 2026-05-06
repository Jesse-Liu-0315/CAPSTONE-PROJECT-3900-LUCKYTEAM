import React from 'react';
import PropTypes from 'prop-types';

const MovieDetailCast = (props) => {
  const castName = props.castName;
  const castNameNoSpace = castName.replaceAll(' ', '_');

  const jumpToCastDetail = () => {
    window.location = `/cast/${props.castId}/${castNameNoSpace}`;
  }

  return (
    <div className='col-auto' style={{ marginLeft: '12px', padding: '0px', textAlign: 'center', cursor: 'pointer' }} onClick={jumpToCastDetail}>
      <img src={props.castPicture} alt="Cast" style={{ width: '130px', height: '193px' }} />
      <p style={{ margin: '0px' }}>{props.castName}</p> 
    </div>
  );
}

MovieDetailCast.propTypes = {
  castId: PropTypes.number,
  castPicture: PropTypes.string,
  castName: PropTypes.string,
}

export default MovieDetailCast;
