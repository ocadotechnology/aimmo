import React, { Component } from 'react'
import { connect } from 'react-redux'
import { actions } from '../../redux/features/GhibliMovies'
import Movie from '../../components/Movie'

class GamePage extends Component {
  render () {
    const movieItems = this.props.movies.map(movie =>
      <Movie key={movie.id} movie={movie} />
    )

    return (
      <div>
        <div>Welcome to the AIMMO game screen</div>
        <button
          onClick={() => { this.props.fetchMovies() }}>
          Get the GhibliMovies!
        </button>
        <ul>
          {movieItems}
        </ul>

      </div>
    )
  }
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
