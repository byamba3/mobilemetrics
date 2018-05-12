import React, { Component } from 'react';
import { Button, Row, Col } from 'react-bootstrap';
import logo from './logo.svg';
import axios from 'axios';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      performance:"",
      battery:"",
      display:"",
      camera:"",
      overall:"",
      articles: []
    };
  }

  submitPhoneName = (e) =>{
    let data = {
      phoneType:this.state.textBody
    }
    var self = this;
    axios.post('http://127.0.0.1:3453/analyze',data)
    .then(function (response) {
      console.log(response.data.result);
      self.setState({
        performance: response.data.result.performance, 
        battery: response.data.result.battery,
        display: response.data.result.display,
        camera: response.data.result.camera,
        overall: response.data.result.overall ,
        articles: response.data.result.articles

      });
      console.log(response.data.performance)
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  textChange = (e) =>{
    e.preventDefault()
    if(e && e.target && e.target.value){
      this.setState({textBody: e.target.value});
    }
    
  }
  render() {
    return (
      <div className="Outer">
        <div className="App">
        
          <Row>
            <input type = "text" placeholder="Phone Name" onChange={this.textChange}></input>
            <button onClick={this.submitPhoneName}>Search Ratings</button>
          </Row>
          <Row>
            <h3> The Score ranges from -1 to 1 </h3>
          </Row>  
          <Row>    
          <p className="outputs" id ="Performance:"><b>Performance: </b>{this.state.performance}</p>
          <p className="outputs" id ="Battery:"><b>Battery: </b>{this.state.battery}</p>
          <p className="outputs" id ="Display:"><b>Display: </b>{this.state.display}</p>
          <p className="outputs" id ="Camera:"><b>Camera: </b>{this.state.camera}</p>
          <p className="outputs" id ="Overall Score:"><b>Overall Score: </b>{this.state.overall}</p>
            <div className="articles"><b>Sources:</b><i>{
              this.state.articles ?
                this.state.articles.map((article, index) => (
                    <p>{article}</p>
                ))
              : ""
            }</i>
          </div>
          </Row>
        </div>
      </div>
    );
  }
}

export default App;
