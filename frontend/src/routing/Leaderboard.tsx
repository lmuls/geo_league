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
        const res = await fetch('/leaderboard/')
        if(res.status === 200) {
            const data = await res.json()
            setPlayers(data.players)
        }
    }

    console.log(players)

    const renderPlayer = (player: Player) => {
        return <h1>{player.name}</h1>
    }

    return (
        <div className={style.component}>
            <h1>Here be players</h1>
            <CollapsibleTable content={players} />
        </div>
        
    )

}