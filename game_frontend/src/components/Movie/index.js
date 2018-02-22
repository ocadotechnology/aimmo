import React, { PureComponent } from 'react'

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
