import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'

export default class Movie extends PureComponent {
  render () {
    const movie = this.props.movie
    return (
      <li>
        {movie.title} - {movie.director} - {movie.producer} - { movie.release_date}
      </li>
    )
  }
}

Movie.propTypes = {
  movie: PropTypes.shape({
    title: PropTypes.string.isRequired,
    director: PropTypes.string.isRequired,
    producer: PropTypes.string.isRequired,
    release_date: PropTypes.string.isRequired,
  })
}
