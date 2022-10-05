import React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import {Game} from "../types";
import {formatDate} from "../util/mainUtils"

export function SubTable({games}: {games: Game[]}) {
  return (
    <Table size="small" aria-label="purchases">
      <TableHead>
        <TableRow>
          <TableCell>Game</TableCell>
          <TableCell>Dato</TableCell>
          <TableCell>Kart</TableCell>
          <TableCell>Poeng</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {games.map((historyRow) => (
          <TableRow key={historyRow.points}>
            <TableCell><a href={`https://www.geoguessr.com/results/${historyRow.id}`}>{historyRow.id}</a></TableCell>
            <TableCell component="th" scope="row">
                  {formatDate(historyRow.date)}
            </TableCell>
            <TableCell>{historyRow.map_name}</TableCell>
            <TableCell>
              {historyRow.points}
            </TableCell>
            </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
