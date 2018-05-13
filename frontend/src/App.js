import React, { Component } from 'react';
import { Label, InputGroup, FormGroup, ControlLabel, FormControl, HelpBlock,
  Button, Row, Col, ListGroup, ListGroupItem, Grid , PageHeader, Badge} from 'react-bootstrap';
import logo from './logo.svg';
import axios from 'axios';
import './App.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import './app2.css';
import './spinner.css';

const Test = ({articles_}) => (
  <div>
    {articles_.map(article => (
      <ListGroup>
        <ListGroupItem href={article.url} header = {article.title} key={article.title}>{article.domain}</ListGroupItem>
      </ListGroup>
    ))}
  </div>
);

const getRating = (score) => {
  if (score >= 0.5){
    return <Label bsStyle="success">Positive</Label>;
  } else if (score < 0.5 && score > -0.5){
    return <Label bsStyle="default">Neutral</Label>;
  } else if (score <= -0.5){
    return <Label bsStyle="danger">Negative</Label>;
  }
}

const format = /[!@#$%^&*()_\-=\[\]{};':"\\|,.<>\/?]/;

class App extends Component {
  constructor(props) {
    super(props)
    this.handleChange = this.handleChange.bind(this);

    this.state = {
      performance:"-",
      battery:"-",
      display:"-",
      camera:"-",
      overall:"-",
      showing:false,
      value: '',
      articles: null
    };
  }

  submitPhoneName = (e) =>{
    let data = {
      phoneType:this.state.value
    }
    var self = this;
    const { showing } = this.state;
    this.setState({ showing: !showing })
    axios.post('http://127.0.0.1:3453/analyze',data)
    .then(function (response) {
      console.log(response.data.result);
      self.setState({
        performance: response.data.result.performance, 
        battery: response.data.result.battery,
        display: response.data.result.display,
        camera: response.data.result.camera,
        overall: response.data.result.overall,
        showing: false,
        articles: response.data.result.articles

      });
      console.log(response.data.performance)
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  
  getValidationState() {
    const length = this.state.value.length;
    if (length == 0) return null;
    else if (format.test(this.state.value)) return 'error';
    else if (isNaN(this.state.value) && length < 3) return 'warning';
    else if (!isNaN(this.state.value)) return 'error';
    else return null;
    return null;
  }

  handleChange(e) {
    this.setState({ value: e.target.value });
  }

  getFeedback() {
    const length = this.state.value.length;
    if (length == 0) return null;
    if (format.test(this.state.value)) return 'You can not have special characters.';
    else if (isNaN(this.state.value) && length < 4) return 'Name is unusually short';
    else if (!isNaN(this.state.value)) return 'You can not have only numbers.';
  }

  render() {
    return (
      <Grid>
        <div className="App">
          <Row>
            <PageHeader>
              Mobile Metrics <small>SMARTPHONE SENTIMENT ANALYSIS</small>
            </PageHeader>
          </Row>
          <Row>
              <form>
                <FormGroup
                  controlId="formBasicText"
                  validationState={this.getValidationState()}
                >
                  <InputGroup className = "search-bar">
                    <FormControl
                      type="text"
                      value={this.state.value}
                      placeholder="Enter smartphone name"
                      onChange={this.handleChange}
                    />
                    <InputGroup.Button>
                      <Button bsStyle="primary" onClick={this.submitPhoneName}>Search Ratings</Button>
                    </InputGroup.Button>
                  </InputGroup>
                  <FormControl.Feedback />
                  <HelpBlock>{this.getFeedback()}</HelpBlock>
                </FormGroup>
              </form>
          </Row>
          <Row>
            <h3>SENTIMENT </h3>
            <small>(-1 to -0.5 is negative) (-0.5 to 0.5 is neutral) (0.5 - 1.0 is positive)</small>
          </Row>
          { this.state.showing 
                    ? <div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div>
                    : null
          }
          { !this.state.showing ?
            <div>
              <Row>    
                <Col md={12}>
                  <ListGroup>
                    <ListGroupItem className="outputs" id ="Performance:"><b>Performance: </b>{this.state.performance} {getRating(this.state.performance)}</ListGroupItem>
                    <ListGroupItem className="outputs" id ="Battery:"><b>Battery: </b>{this.state.battery} {getRating(this.state.battery)}</ListGroupItem>
                    <ListGroupItem className="outputs" id ="Display:"><b>Display: </b>{this.state.display} {getRating(this.state.display)}</ListGroupItem>
                    <ListGroupItem className="outputs" id ="Camera:"><b>Camera: </b>{this.state.camera} {getRating(this.state.camera)}</ListGroupItem>
                    <ListGroupItem className="outputs" id ="Overall Score:"><b>Article Score: </b>{this.state.overall} {getRating(this.state.overall)}</ListGroupItem>
                  </ListGroup>
                </Col>
              </Row> 
              <Row> 
                <Col md={12}>
                  { this.state.articles != null 
                        ? <h3> Found <Label bsStyle="primary">{this.state.articles.length}</Label> review sources.</h3>
                        : null
                  }                 
                </Col>
              </Row> 
              <Row> 
                <Col md={12}>
                  { this.state.articles != null && this.state.articles.length
                          ? <Test articles_={this.state.articles} />
                          : null
                  }   
                </Col>

              </Row>
            </div>
            : null
          }
        </div>
      </Grid>
    );
  }
}

export default App;
