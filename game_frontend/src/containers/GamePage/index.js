import React, { Component, Fragment } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'features/GhibliMovies'
import Movie from 'components/Movie'
import Button from 'components/Button'

export class GamePage extends Component {
  render () {
    const movieItems = this.props.movies.map(movie =>
      <Movie key={movie.id} movie={movie} />
    )

    return (
      <Fragment>
        <div>Welcome to the AIMMO game screen</div>
        <Button
          id='fetch-movies-button'
          onClick={() => { this.props.fetchMovies() }}>
          Get the GhibliMovies!
        </Button>
        <ul>
          {movieItems}
        </ul>
      </Fragment>
    )
  }
}

GamePage.propTypes = {
  movies: PropTypes.array,
  fetchMovies: PropTypes.func
}

const mapStateToProps = state => {
  return {
    movies: state.movieReducer.movies
  }
}

const mapDispatchToProps = {
  fetchMovies: actions.fetchMovies
}

export default connect(mapStateToProps, mapDispatchToProps)(GamePage)
