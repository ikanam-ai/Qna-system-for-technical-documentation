import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './components/App/App';

import { AdaptivityProvider, ConfigProvider } from '@vkontakte/vkui';
import "@vkontakte/vkui/dist/cssm/styles/themes.css";

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ConfigProvider appearance="light" platform="vkcom">
      <AdaptivityProvider>
        <App />
      </AdaptivityProvider>
    </ConfigProvider>
  </React.StrictMode>
);
