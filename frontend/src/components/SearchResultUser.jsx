import React from 'react';
import PropTypes from 'prop-types';
import { Button } from '@mui/material';
import Chip from '@mui/material/Chip';
import defaultPhoto from '../user_profile_default.png'

const SearchResultUser = (props) => {
  const [substring, setSubstring] = React.useState(props.userDescription.substring(0, 380));
  const [needMore, setNeedMore] = React.useState(props.userDescription.length > 380 ? true : false);
  const [moreStatus, setMoreStatus] = React.useState(false);

  React.useEffect(() => {
    setSubstring(props.userDescription.substring(0, 380));
  }, [props.userDescription]);

  React.useEffect(() => {
    setNeedMore(props.userDescription.length > 380 ? true : false);
  }, [props.userDescription]);

  const jumpToUserDetail = () => {
    window.location = `/otherprofile/${props.userId}`;
  }

  const moreButton = () => {
    setMoreStatus(!moreStatus);
  }

  return (
    <>
      <div className="row">
        <div className="card mb-3" style={{ border: '0px' }}>
          <div className="row g-0">
            <div className="col-auto">
              <img src={props.userPhoto === null ? defaultPhoto : props.userPhoto} className="img-fluid" alt="Movie" style={{ width: '230px', height: '350px', cursor: 'pointer' }} onClick={jumpToUserDetail} />
            </div>
            <div className="col" style={{ width: '70%' }}>
              <div className="card-body" style={{ position:'relative', height: '100%', padding: '0px', paddingLeft: '5px' }}>
                <div className='row'>
                  <div className='col-auto'>
                    <h5 style={{ cursor: 'pointer', margin: '0px' }} className="card-title" onClick={jumpToUserDetail}>{props.userName}</h5>
                  </div>
                  <div className='col-auto' style={{ padding: '0px' }}>
                    {props.userTag !== null && 
                      <Chip label={props.userTag} variant="outlined" style={{ height: '24px' }} />
                    }
                  </div>
                </div>
                <br/>
                {moreStatus && 
                  <p style={{ margin: '0px' }}>{props.userDescription}</p>
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
                <p className="card-text" style={{ position:'absolute', bottom: 0, margin: '0px'}}><small className="text-muted">{props.userViews} Views</small></p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <hr/>
    </>
  );
}

SearchResultUser.propTypes = {
  userDescription: PropTypes.string,
  userId: PropTypes.number,
  userName: PropTypes.string,
  userPhoto: PropTypes.string,
  userViews: PropTypes.number,
}

export default SearchResultUser;
