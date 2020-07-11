import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from "react-router-dom";
import 'antd/dist/antd.css';
import './index.css';
import Root from 'pages'

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
        {/* root 밑에 있는 컴포넌트들은 라우팅 가능 */}
        <Root />
    </BrowserRouter>
  </React.StrictMode>,
  
  document.getElementById('root')
);


