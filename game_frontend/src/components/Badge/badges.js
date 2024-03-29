import ChangeDirectionBadge from 'img/1_change_direction.svg'
import RandomDirectionsBadge from 'img/1_random_directions.svg'
import InvestigateBadge from 'img/1_investigate.svg'
import AvoidBadge from 'img/2_avoid.svg';
import PickupBadge from 'img/2_pick_up.svg';


export const badgeInfo = {
  '1:1': {
    title: 'Congratulations!',
    message: 'You have earned your first badge! See how many more badges you can get.',
    img: ChangeDirectionBadge,
    name: 'Change direction',
  },
  '1:2': {
    title: 'Well done!',
    message: 'You just earned the second badge by going in random directions!',
    img: RandomDirectionsBadge,
    name: 'Random directions',
  },
  '1:3': {
    title: 'Congratulations!',
    message: 'You have earned the final badge in this era by investigating a location!',
    img: InvestigateBadge,
    name: 'Investigate location',
  },
  '2:1': {
    title: 'Amazing job!',
    message: 'You created your first subroutine!',
    img: AvoidBadge,
    name: 'Create subroutine'
  },
  '2:2': {
    title: 'You\'re an explorer!',
    message: 'You\'re ready to pick up your first artefact!',
    img: PickupBadge,
    name: 'Pickup artefact'
  },
}
