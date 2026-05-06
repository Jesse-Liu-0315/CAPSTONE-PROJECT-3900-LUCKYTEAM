import React from 'react';
import PropTypes from 'prop-types';
import { Button } from '@mui/material';

const SearchResultDirector = (props) => {
  const [substring, setSubstring] = React.useState(props.directorDescription.substring(0, 380));
  const [needMore, setNeedMore] = React.useState(props.directorDescription.length > 380 ? true : false);
  const [moreStatus, setMoreStatus] = React.useState(false);

  React.useEffect(() => {
    setSubstring(props.directorDescription.substring(0, 380));
  }, [props.directorDescription]);

  React.useEffect(() => {
    setNeedMore(props.directorDescription.length > 380 ? true : false);
  }, [props.directorDescription]);

  const jumpToDirectorDetail = () => {
    window.location = `/director/${props.directorId}/${props.directorName.replaceAll(' ', '_')}`;
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
              <img src={props.directorPhoto} className="img-fluid" alt="Movie" style={{ width: '230px', height: '350px', cursor: 'pointer' }} onClick={jumpToDirectorDetail} />
            </div>
            <div className="col">
              <div className="card-body" style={{ position:'relative', height: '100%', padding: '0px', paddingLeft: '5px' }}>
                <h5 style={{ cursor: 'pointer' }} className="card-title" onClick={jumpToDirectorDetail}>{props.directorName}</h5>
                <br/>
                {moreStatus && 
                  <p style={{ margin: '0px' }}>{props.directorDescription}</p>
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
                <p className="card-text" style={{ position:'absolute', bottom: 20, margin: '0px'}}><small className="text-muted">{props.directorViews} Views</small></p>
                <p className="card-text"><small className="text-muted" style={{ position:'absolute', bottom: 0 }}>{props.directorPerformance} Performances</small></p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <hr/>
    </>
  );
}

SearchResultDirector.propTypes = {
  directorDescription: PropTypes.string,
  directorId: PropTypes.number,
  directorName: PropTypes.string,
  directorPhoto: PropTypes.string,
  directorViews: PropTypes.number,
  directorPerformance: PropTypes.number,
}

export default SearchResultDirector;
