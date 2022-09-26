import React from "react"
import {Route, Routes} from "react-router-dom"

import ReactEx from "../comps/ReactEx"
import { Leaderboard } from "./Leaderboard"
import { NewGame } from "./NewGame"

export const RoutesTree = () => {
    return (
        <div>
            <Routes>
                <Route path="/ex" element={<ReactEx/>}/>
                <Route path="/leaderboard" element={<Leaderboard/>}/>
                <Route path="/new-game" element={<NewGame/>}/>
            </Routes>
        </div>
    )
}