import React, { useState } from "react";
import { Player } from "../types";
import { SubTable } from "./SubTable";
import styles from "./CollapsibleTable.module.scss";

function rankColor(rank: number): string {
  if (rank === 1) return "var(--rank-1)";
  if (rank === 2) return "var(--rank-2)";
  if (rank === 3) return "var(--rank-3)";
  return "var(--text-faint)";
}

function Row({ player, rank }: { player: Player; rank: number }) {
  const [open, setOpen] = useState(false);
  const color = rankColor(rank);

  return (
    <div
      className={`${styles.row} ${open ? styles.rowOpen : ""}`}
      style={{ "--rank-color": color } as React.CSSProperties}
    >
      <button className={styles.rowMain} onClick={() => setOpen(!open)}>
        <span className={styles.rankNum}>{String(rank).padStart(2, "0")}</span>

        <span className={styles.name}>{player.name}</span>

        <span className={styles.meta}>
          <span className={styles.gamesBadge}>{player.games.length} spill</span>
        </span>

        <span className={styles.points}>
          {player.points.toLocaleString("no-NO")}
          <span className={styles.ptsSuffix}>pts</span>
        </span>

        <span className={`${styles.chevron} ${open ? styles.chevronOpen : ""}`}>
          ↓
        </span>
      </button>

      {open && (
        <div className={styles.details}>
          <SubTable games={player.games} />
        </div>
      )}
    </div>
  );
}

export default function CollapsibleTable({ content }: { content: Player[] }) {
  if (content.length === 0) {
    return (
      <div className={styles.empty}>
        <span className={styles.emptyIcon}>◎</span>
        <p>Ingen spillere ennå</p>
        <p className={styles.emptyHint}>Last opp et spill for å komme i gang</p>
      </div>
    );
  }

  return (
    <div className={styles.table}>
      <div className={styles.header}>
        <span className={styles.headerRank}>#</span>
        <span className={styles.headerName}>Spiller</span>
        <span />
        <span className={styles.headerPoints}>Poeng</span>
        <span />
      </div>
      <div className={styles.rows}>
        {content.map((player, i) => (
          <Row key={player.name} player={player} rank={i + 1} />
        ))}
      </div>
    </div>
  );
}
