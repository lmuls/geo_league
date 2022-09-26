import React from 'react';
import './App.css';
import NavArea from './comps/NavArea';
import {RoutesTree} from './routing/RoutesTree'
import "./styles/globals.scss"
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <NavArea>
        <RoutesTree />
      </NavArea>
    </ThemeProvider>
  );
}

export default App;
