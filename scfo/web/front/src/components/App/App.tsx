import { FormEvent, useEffect, useRef, useState } from 'react';
import {
  AppRoot, Button, Div, Flex, FormItem,
  Group,
  Input,
  Panel,
  PanelHeader, Paragraph,
  Separator,
  SplitCol, SplitLayout,
  Text, Title
} from '@vkontakte/vkui';
import { Icon20LogoRustoreOutline, Icon24ArrowUp } from '@vkontakte/icons';
import { Message } from '../Message/Message';
import { TypingMessage } from '../TypingMessage/TypingMessage';

import styles from './App.module.scss';

export const enum MessageType {
  SENT = 'sent',
  RECEIVED = 'received',
}

interface ChatMessage {
  type: MessageType;
  text: string;
}

export const enum ServerStatus {
  TYPING = 'typing',
  IDLE = 'idle'
}

function App() {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [message, setMessage] = useState('');
  const [serverStatus, setServerStatus] = useState(ServerStatus.IDLE);
  const [shouldScroll, setShouldScroll] = useState(false);

  const threadRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const newSocket = new WebSocket('ws://localhost:3001');

    newSocket.addEventListener('open', () => {
      console.log('Соединение установлено');
    });

    newSocket.addEventListener('close', () => {
    });

    newSocket.addEventListener('error', () => {
    });

    newSocket.addEventListener('message', (message) => {
      try {
        const body = JSON.parse(message.data);

        switch (body.type) {
          case 'status':
            setServerStatus(body.data);
            break;
          case 'message':
            setMessages((prevMessages) => [...prevMessages, { type: MessageType.RECEIVED, text: body.data }]);
            setShouldScroll(true);
            break;
        }
      } catch (err) {
        console.error(err);
      }
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
      setSocket(null);
      console.log('disconnect');
    };
  }, []);

  const handleClick = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (message.length === 0) {
      return;
    }

    if (socket) {
      socket.send(message);
      setMessages((prevMessages) => [...prevMessages, { type: MessageType.SENT, text: message }]);
      setShouldScroll(true);
      setMessage('');
    }
  };

  useEffect(() => {
    threadRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
    setShouldScroll(false);
  }, [serverStatus, shouldScroll]);

  return (
    <AppRoot style={{ marginTop: '1rem' }}>
      <SplitLayout center>
        <SplitCol fixed  width={280} maxWidth={280}>
          <Panel style={{marginTop: '16px'}}>
            <Group>
              <Flex align="center" className={styles.title}>
              <Icon20LogoRustoreOutline height={60} width={60}/>
              <Title>RuStore</Title>
              </Flex>
              <Div>
              <Paragraph>
                Привет!
                <br/>
                Это ваш личный AI ассистент по документации RuStore – лучшего магазина приложений в Рунете.
              </Paragraph>
              </Div>
              <Text>Made with love by <b>кит-кат</b></Text>
            </Group>
          </Panel>
        </SplitCol>
        <SplitCol maxWidth={'600px'} autoSpaced>
          <Panel>
            <PanelHeader delimiter={'auto'}>Спросите у бота</PanelHeader>
            <Group>
              <Div className={styles.chatWrapper}>
                <Flex direction="column">
                  {
                    messages.map((item, index) => (
                      <Message text={item.text} key={index} type={item.type} />
                    ))
                  }
                  {serverStatus === ServerStatus.TYPING && <TypingMessage />}
                </Flex>
                <div ref={threadRef} />
              </Div>
              <Separator />
              <form onSubmit={handleClick}>
                <Flex align="center">
                  <FormItem style={{ flexGrow: 1 }}>
                    <Input placeholder={'Спросите что-нибудь'} value={message}
                           onChange={(e) => setMessage(e.target.value)} />
                  </FormItem>
                  <Button style={{ marginRight: 8 }} disabled={message.length === 0} size="l" before={<Icon24ArrowUp />}
                          type="submit" />
                </Flex>
              </form>
            </Group>
          </Panel>
        </SplitCol>
      </SplitLayout>
    </AppRoot>
  );
}

export default App;
