import React from 'react';
import NavArea from './comps/NavArea';
import { RoutesTree } from './routing/RoutesTree';
import './styles/globals.scss';

function App() {
  return (
    <NavArea>
      <RoutesTree />
    </NavArea>
  );
}

export default App;
