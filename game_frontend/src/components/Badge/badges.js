import React from 'react'

import ChangeDirectionBadge from 'img/1_change_direction.svg'
import AllDirectionsBadge from 'img/1_all_directions.svg'
import InvestigateBadge from 'img/1_investigate.svg'

export const badgeInfo = [
  {
    title: 'Congratulations!',
    message: 'You have earned your first badge! See how many more badges you can get.',
    img: ChangeDirectionBadge,
    name: 'Change direction',
  },
  {
    title: 'Well done!',
    message: 'You just earned the second badge by going to all directions!',
    img: AllDirectionsBadge,
    name: 'All directions',
  },
  {
    title: 'Congratulations!',
    message: 'You have earned the final badge in this era by investigating a location!',
    img: InvestigateBadge,
    name: 'Investigate location',
  },
]