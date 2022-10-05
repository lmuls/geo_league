import { platform } from "os";
import React, { useEffect, useState } from "react"
import CollapsibleTable from "../comps/CollapsibleTable";
import { Player } from "../types";
import style from "../styles/Leaderboard.module.scss"


export function Leaderboard() {
    const [loading, isLoading] = useState<boolean>(false)
    const [players, setPlayers] = useState<Player[]>([])

    useEffect(() => {
        fetchData()
    }, [])

    const fetchData = async () => {
        const res = await fetch(`${process.env.REACT_APP_DATABASE_URL}/leaderboard/`, )
        if(res.status === 200) {
            const data = await res.json()
            setPlayers(data.players)
        }
    }

    return (
        <div className={style.component}>
            <CollapsibleTable content={players} />
        </div>
        
    )

}