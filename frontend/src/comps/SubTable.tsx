import React from "react";
import { Chip, Link } from "@mui/material";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { Game } from "../types";
import {formatDate} from "../util/mainUtils"

export function SubTable({games}: {games: Game[]}) {
  return (
    <Table size="small" aria-label="purchases">
      <TableHead>
        <TableRow>
          <TableCell>Dato</TableCell>
          <TableCell>Kart</TableCell>
          <TableCell>Poeng</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {games.map((historyRow) => (
          <TableRow key={historyRow.points}>
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
