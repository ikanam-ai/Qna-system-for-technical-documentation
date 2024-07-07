import { Div } from '@vkontakte/vkui';

import styles from './TypingMessage.module.scss';


export const TypingMessage = () => {
  return (
    <Div className={styles.wrapperReceived}>
      <div className={styles.typing}>
        <div className={styles.dot}></div>
        <div className={styles.dot}></div>
        <div className={styles.dot}></div>
      </div>
    </Div>
  )
}
