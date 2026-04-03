import React from "react";
import { Game } from "../types";
import { formatDate } from "../util/mainUtils";
import styles from "./SubTable.module.scss";

export function SubTable({ games }: { games: Game[] }) {
  return (
    <div className={styles.wrap}>
      <div className={styles.header}>
        <span>Kart</span>
        <span>Dato</span>
        <span className={styles.right}>Poeng</span>
        <span />
      </div>
      {games.map((game) => (
        <div key={game.id} className={styles.row}>
          <span className={styles.mapName}>{game.map_name}</span>
          <span className={styles.date}>{formatDate(game.date)}</span>
          <span className={styles.points}>
            {game.points.toLocaleString("no-NO")}
          </span>
          <a
            className={styles.link}
            href={`https://www.geoguessr.com/results/${game.id}`}
            target="_blank"
            rel="noreferrer"
          >
            ↗
          </a>
        </div>
      ))}
    </div>
  );
}
