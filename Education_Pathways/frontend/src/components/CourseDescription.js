import React, { Component } from 'react';
import './css/course-description.css'
import 'bootstrap/dist/css/bootstrap.css';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import requisite_label from './img/requisite-label.png'
import empty_star from './img/star.png'
import API from '../api';
import Rating from '@mui/material/Rating';
import { Button, Grid, TextField } from '@mui/material';

let star = empty_star;

class CourseDescriptionPage extends Component {

  constructor(props) {
    super(props)

    this.state = {
      reviews: [],
      recommendations: [],
      leftReviewRating: 0,
      leftReviewDescription: "",
      recommendations: [],
      leftRecommendationCourse: "",
      leftRecommendationDescription: "",
      validCourse: "",
      minorDescription: "",
      course_code: "",
      course_name: "",
      division: "",
      department: "",
      graph: "",
      course_description: "",
      syllabus: "",
      prerequisites: "",
      corequisites: "",
      exclusions: "",
      related: "",
      starred: false,
      graphics: [],
      professors: "N/A",
      term: "N/A",
      hours: "N/A",
    }
  }



  componentDidMount() {
    Promise
      .all([
        API
          .get(`/course/details?code=${this.props.match.params.code}`, { code: this.props.course_code })
          .then(res => {
            console.log(res.data.course)
            this.setState({ course_code: res.data.course.code })
            this.setState({ course_name: res.data.course.name })
            this.setState({ division: res.data.course.division })
            this.setState({ department: res.data.course.department })
            this.setState({ course_description: res.data.course.description })
            this.setState({ graph: res.data.course.graph })
            this.setState({ professors: res.data.course.professors })
            this.setState({ hours: res.data.course.hours })
            this.setState({ term: res.data.course.term })
            this.setState({ related: res.data.course.related })
            let prereq_len = res.data.course.prereq.length
            if (prereq_len > 1) {
              let prereq_str = ""
              for (let i = 0; i < prereq_len; i++) {
                prereq_str += res.data.course.prereq[i]
                if (i !== prereq_len - 1) {
                  prereq_str += ", "
                }
              }
              this.setState({ prerequisites: prereq_str })
            } else {
              this.setState({ prerequisites: res.data.course.prereq })
            }
            let coreq_len = res.data.course.coreq.length
            if (coreq_len > 1) {
              let coreq_str = ""
              for (let i = 0; i < coreq_str; i++) {
                coreq_str += res.data.course.coreq[i]
                if (i !== coreq_len - 1) {
                  coreq_str += ", "
                }
              }
              this.setState({ corequisites: coreq_str })
            } else {
              this.setState({ corequisites: res.data.course.coreq })
            }
            let exclusion_len = res.data.course.exclusion.length
            if (exclusion_len > 1) {
              let exclusion_str = ""
              for (let i = 0; i < exclusion_str; i++) {
                exclusion_str += res.data.course.exclusion[i]
                if (i !== exclusion_len - 1) {
                  exclusion_str += ", "
                }
              }
              this.setState({ exclusions: exclusion_str })
            } else {
              this.setState({ exclusions: res.data.course.exclusion })
            }
            let syllabus_link = "http://courses.skule.ca/course/" + this.state.course_code
            this.setState({ syllabus: syllabus_link })

            let temp_graph = []
            //temp_graph.push(<ShowGraph graph_src={this.state.graph}></ShowGraph>)
            this.setState({ graphics: temp_graph })
          }),
        API
          .get(`/reviews?course=${this.props.match.params.code}`, { code: this.props.course_code })
          .then(res => {
            console.log(res.data)
            this.setState({ reviews: res.data })
          }),
        API
          .get(`/recommendations?course1=${this.props.match.params.code}`, { code: this.props.course_code })
          .then(res => {
            console.log(res.data)
            this.setState({ recommendations: res.data })
          }),
        API
          .get(`/minors?course=${this.props.match.params.code}`, { code: this.props.course_code })
          .then(res => {
            console.log(res.data)
            this.setState({ minorDescription: res.data.minorInfo })
          })
      ])
      .then(() => {
        console.log("new state after initial load: ", this.state)
      })
  }


  openLink = () => {
    const newWindow = window.open(this.state.syllabus, '_blacnk', 'noopener,noreferrer');
    if (newWindow) {
      newWindow.opener = null;
    }
  }

  handleRating = (_event, newValue) => this.setState({ leftReviewRating: newValue })

  handleDescription = (event) => this.setState({ leftReviewDescription: event.target.value })

  handleButton = () => {
    if (this.state.leftReviewRating === 0 || this.state.leftReviewDescription.trim() === "") {
      alert("Please select a rating and/or fill the description box")
    } else {
      API
        .post(`/reviews?course=${this.state.course_code}`, { description: this.state.leftReviewDescription, rating: this.state.leftReviewRating })
        .then(res => {
          this.setState({ reviews: [...this.state.reviews, { course: this.state.course_code, description: this.state.leftReviewDescription, rating: this.state.leftReviewRating }] })
        })
        .then(() => {
          console.log("new state after adding new review: ", this.state)
          this.setState({ leftReviewRating: 0, leftReviewDescription: "" })
        })
    }
  }

  handleCourseRecommendation = (event) => {
    this.setState({ leftRecommendationCourse: event.target.value })
    API
      .post(`/test?courseOrig=${this.state.course_code}`, { courseOrig: this.state.course_code, courseCheck: event.target.value })
      .then(res => this.setState({ validCourse: res.data.course }))
  }

  handleDescriptionRecommendation = (event) => this.setState({ leftRecommendationDescription: event.target.value })

  handleButtonRecommendation = () => {
    if (this.state.leftRecommendationDescription.trim() === "" || this.state.leftRecommendationCourse.trim() === "") {
      alert("Please select course and/or fill the description box")
    } else if (this.state.validCourse == this.state.course_code) {
      alert("Please choose a course code different from this code.")
    } else if (this.state.validCourse == "") {
      alert("Course was not found! Please check the course code.")
    } else {
      API
        .post(`/recommendations?course1=${this.state.course_code}`, { course1: this.state.course_code, course2: this.state.validCourse, description: this.state.leftRecommendationDescription })
        .then(res => {
          this.setState({ recommendations: [...this.state.recommendations, { course1: this.state.course_code, course2: this.state.validCourse, description: this.state.leftRecommendationDescription }] })
        })
        .then(() => {
          console.log("new state after adding new recommendation: ", this.state)
          this.setState({ leftRecommendationCourse: "", leftRecommendationDescription: "", validCourse: "" })
        })
    }
  }

  render() {
    return (

      <div className="page-content">
        <Container className="course-template">
          <Row float="center" className="course-title">
            <Col xs={8}>
              <h1>{this.state.course_code} : {this.state.course_name}</h1>
            </Col>
            {/* <Col xs={4}>
              <img src={star} onClick={this.check_star} alt="" />
            </Col> */}
          </Row>
          <Row>
            <Col className="col-item">
              <h3>Division</h3>
              <p>{this.state.division}</p>
            </Col>
            <Col className="col-item">
              <h3>Department</h3>
              <p>{this.state.department}</p>
            </Col>
            <Col className="col-item">
              <h3>Past Tests and Syllabi</h3>
              <button className={"syllabus-link"} onClick={this.openLink}>View</button>
            </Col>
          </Row>
          <Row className="col-item course-description">
            <h3>Course Description</h3>
            <p>{this.state.course_description}</p>
          </Row>
          <Row>
            <Col className="col-item">
              <h3>Professor</h3>
              <p>{this.state.professors}</p>
            </Col>
            <Col className="col-item">
              <h3>Terms</h3>
              <p>{this.state.term}</p>
            </Col>
            <Col className="col-item">
              <h3>Hours</h3>
              <p>{this.state.hours}</p>
            </Col>
          </Row>
          <Row className="col-item course-requisite">
            <Row>
              <h3>Course Requisites</h3>
            </Row>
            <Row>
              <Row>
                <Col className="requisites-display">
                  <h4>Pre-Requisites</h4>
                  <p>{this.state.prerequisites}</p>
                </Col>
                <Col className="requisites-display">
                  <h4>Co-Requisites</h4>
                  <p>{this.state.corequisites}</p>
                </Col>
              </Row>
              <Row>
                <Col className="requisites-display">
                  <h4>Exclusion</h4>
                  <p>{this.state.exclusions}</p>
                </Col>
                <Col className="requisites-display">
                  <h4>{this.state.course_code} is required for</h4>
                  <p>{this.state.related}</p>
                </Col>
              </Row>
            </Row>
          </Row>
          <Row className="col-item minor-description">
            <h3>Engineering Minors</h3>
            <p>{this.state.minorDescription}</p>
          </Row>
          <Row className="col-item course-recommendations">
            <h3>Course Recommendations</h3>
            <Container>
              {this.state.recommendations.map(recommendation =>
                <Row >
                  <Col>
                    <h3 align="center">{recommendation.course2}</h3>
                  </Col>
                  <Col>
                    <p align="left">{recommendation.description}</p>
                  </Col>
                </Row>
              )}
              <Grid marginTop={2} container spacing={2}>
                <Grid item xs={2}>
                  <TextField label="Course Code" multiline fullWidth value={this.state.leftRecommendationCourse} onChange={this.handleCourseRecommendation} />
                </Grid>
                <Grid item xs={8}>
                  <TextField label="Recommendation description" multiline fullWidth value={this.state.leftRecommendationDescription} onChange={this.handleDescriptionRecommendation} />
                </Grid>
                <Grid item xs={2}>
                  <Button fullWidth size="large" variant="contained" onClick={this.handleButtonRecommendation}>Submit</Button>
                </Grid>
              </Grid>
            </Container>
          </Row>

          <Row className="course-reviews">
            <h3>Course Reviews</h3>
            <Container>
              {this.state.reviews.map(review =>
                <Row >
                  <Col>
                    <Rating size="large" readOnly value={review.rating} />
                  </Col>
                  <Col>
                    <p align="left">{review.description}</p>
                  </Col>
                </Row>
              )}
              <Grid marginTop={2} container spacing={2}>
                <Grid item xs={2}>
                  <Rating size="large" value={this.state.leftReviewRating} onChange={this.handleRating} />
                </Grid>
                <Grid item xs={8}>
                  <TextField label="Leave a review" multiline fullWidth value={this.state.leftReviewDescription} onChange={this.handleDescription} />
                </Grid>
                <Grid item xs={2}>
                  <Button fullWidth size="large" variant="contained" onClick={this.handleButton}>Submit</Button>
                </Grid>
              </Grid>
            </Container>
          </Row>
        </Container>
      </div>

    )
  }
}

export default CourseDescriptionPage
