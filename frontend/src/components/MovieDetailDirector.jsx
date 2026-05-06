import React from 'react';
import PropTypes from 'prop-types';

const MovieDetailDirector = (props) => {
  const directorName = props.directorName;
  const directorNameWithSpace = directorName.replaceAll(' ', '_');

  const jumpToDirectorDetail = () => {
    window.location = `/director/${props.directorId}/${directorNameWithSpace}`;
  }

  return (
    <div className='col-auto' style={{ marginLeft: '12px', padding: '0px', textAlign: 'center', cursor: 'pointer' }} onClick={jumpToDirectorDetail}>
      <img src={props.directorPicture} alt="Cast" style={{ width: '130px', height: '193px' }} />
      <p style={{ margin: '0px' }}>{props.directorName}</p> 
    </div>
  );
}

MovieDetailDirector.propTypes = {
  directorId: PropTypes.number,
  directorPicture: PropTypes.string,
  directorName: PropTypes.string,
}

export default MovieDetailDirector;
