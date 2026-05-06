import React from 'react';
import PropTypes from 'prop-types';
import { Button } from '@mui/material';

const SearchResultCast = (props) => {
  const [substring, setSubstring] = React.useState(props.castDescription.substring(0, 380));
  const [needMore, setNeedMore] = React.useState(props.castDescription.length > 380 ? true : false);
  const [moreStatus, setMoreStatus] = React.useState(false);

  React.useEffect(() => {
    setSubstring(props.castDescription.substring(0, 380));
  }, [props.castDescription]);

  React.useEffect(() => {
    setNeedMore(props.castDescription.length > 380 ? true : false);
  }, [props.castDescription]);

  const jumpToCastDetail = () => {
    window.location = `/cast/${props.castId}/${props.castName.replaceAll(' ', '_')}`;
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
              <img src={props.castPhoto} className="img-fluid" alt="Movie" style={{ width: '230px', height: '350px', cursor: 'pointer' }} onClick={jumpToCastDetail} />
            </div>
            <div className="col">
              <div className="card-body" style={{ position:'relative', height: '100%', padding: '0px', paddingLeft: '5px' }}>
                <h5 style={{ cursor: 'pointer' }} className="card-title" onClick={jumpToCastDetail}>{props.castName}</h5>
                <br/>
                {moreStatus && 
                  <p style={{ margin: '0px' }}>{props.castDescription}</p>
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
                <p className="card-text" style={{ position:'absolute', bottom: 20, margin: '0px'}}><small className="text-muted">{props.castViews} Views</small></p>
                <p className="card-text"><small className="text-muted" style={{ position:'absolute', bottom: 0 }}>{props.castPerformances} Performances</small></p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <hr/>
    </>
  );
}

SearchResultCast.propTypes = {
  castDescription: PropTypes.string,
  castId: PropTypes.number,
  castName: PropTypes.string,
  castPhoto: PropTypes.string,
  castViews: PropTypes.number,
  castPerformances: PropTypes.number
}

export default SearchResultCast;
