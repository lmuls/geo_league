import React from "react"
import {Route, Routes} from "react-router-dom"

import ReactEx from "../comps/ReactEx"
import { Leaderboard } from "./Leaderboard"
import { NewGame } from "./NewGame"
import Home from "./Home";

export const RoutesTree = () => {
    return (
        <div>
            <Routes>
                <Route path="/" element={<Home/>}/>
                <Route path="/leaderboard" element={<Leaderboard/>}/>
                <Route path="/new-game" element={<NewGame/>}/>
            </Routes>
        </div>
    )
}