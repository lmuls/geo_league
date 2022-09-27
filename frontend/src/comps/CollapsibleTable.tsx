import React from "react";
import Box from "@mui/material/Box";
import Collapse from "@mui/material/Collapse";
import IconButton from "@mui/material/IconButton";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import { SubTable } from "./SubTable";
import {Game, Player} from "../types"

function Row({player}: {player: Player}) {
  const [open, setOpen] = React.useState(false);

  return (
    <React.Fragment>
      <TableRow sx={{ "& > *": { borderBottom: "unset" } }}>
        <TableCell>
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
        <TableCell size={"medium"} component="th" scope="row">
              <a className={"player-name"}>{player.name}</a>
        </TableCell>
        <TableCell align="right">
          {player.games.length}
        </TableCell>
        <TableCell align="right">{player.points}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 1 }}>
              <Typography variant="h6" gutterBottom component="div">
                Spilte games
              </Typography>
              <SubTable
                games={player.games}
              />
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </React.Fragment>
  );
}

export default function CollapsibleTable({
  content,
}: {
  content: Player[];
}) {
    return (
      <TableContainer component={Paper}>
        <Table stickyHeader aria-label="collapsible table">
          <TableHead>
            <TableRow>
              <TableCell />
              <TableCell>Speller</TableCell>
              <TableCell align="right">Spilte games</TableCell>
              <TableCell align="right">Poeng</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {content.map((element) => (
              <Row
                player={element}
                key={element.name}
              />
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  } 
