import Fastify, { FastifyInstance, RouteShorthandOptions } from 'fastify';

import fastifyWS from '@fastify/websocket';

const server: FastifyInstance = Fastify({});

const opts: RouteShorthandOptions = {
  schema: {
    response: {
      200: {
        type: 'object',
        properties: {
          pong: {
            type: 'string'
          }
        }
      }
    }
  }
};

server.register(fastifyWS);

server.register(async function(fastify) {
  fastify.get('/', { websocket: true }, (socket /* WebSocket */ /* FastifyRequest */) => {
    socket.send(JSON.stringify({ type: 'message', data: 'Задайте мне любой вопрос, и я постараюсь вам помочь!' }));
    socket.on('message', async (message: string) => {
      socket.send(JSON.stringify({ type: 'status', data: 'typing' }));

      const mlRes = await fetch('http://pybackend:8000/receive-prompt', {
        method: 'POST',
        body: JSON.stringify({ text: message.toString() }),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const res = await mlRes.json();

      socket.send(JSON.stringify({ type: 'message', data: res.message }));
      socket.send(JSON.stringify({ type: 'status', data: 'idle' }));
    });
  });
});

server.get('/ping', opts, async () => {
  return { pong: 'it worked!' };
});

try {
  server.listen({ port: 3001, host: '0.0.0.0' }, ()=> {
    console.log('listening on port 3001');
  });
} catch (err) {
  server.log.error(err);
  process.exit(1);
}
