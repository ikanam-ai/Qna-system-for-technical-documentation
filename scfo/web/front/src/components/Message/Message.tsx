import { Div, Text } from '@vkontakte/vkui';
import { MessageType } from '../App/App';

import styles from './Message.module.scss';
import { marked } from 'marked';
import { useMemo } from 'react';

export interface MessageProps {
  text: string;
  type: MessageType;
}

export const Message = ({ text, type }: MessageProps) => {
  const messageHtml = useMemo(() => marked.parse(text), [text]);

  return (
    <Div className={type === MessageType.SENT ? styles.wrapperSent : styles.wrapperReceived}>
      <Text dangerouslySetInnerHTML={{ __html: messageHtml }} />
    </Div>
  );
};
