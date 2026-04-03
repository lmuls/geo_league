import React, { useEffect, useState } from "react";
import CollapsibleTable from "../comps/CollapsibleTable";
import { Player } from "../types";
import style from "../styles/Leaderboard.module.scss";

export function Leaderboard() {
  const [players, setPlayers] = useState<Player[]>([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const res = await fetch(`${process.env.REACT_APP_DATABASE_URL}/leaderboard/`);
    if (res.status === 200) {
      const data = await res.json();
      setPlayers(data.players);
    }
  };

  return (
    <div className={style.component}>
      <div className={style.pageHeader}>
        <h1 className={style.title}>Leaderboard</h1>
        <p className={style.subtitle}>Totalt poeng — alle spill</p>
      </div>
      <CollapsibleTable content={players} />
    </div>
  );
}
