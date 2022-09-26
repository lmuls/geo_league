import { Button, TextField } from "@mui/material";
import React, { useState } from "react";
import styles from "../styles/NewGame.module.scss"

export function NewGame() {
    const [isSaving, setIsSaving] = useState<boolean>(false)
    const [formData, setFormData] = useState({
        game_id: undefined,
        date: undefined
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setFormData({
            ...formData,
           [e.target.name]: e.target.value})
    }

    const handleSave = async () => {
        setIsSaving(true)

        if(formData.game_id === undefined) {
            window.alert("Du må jo fylle inn en gameid da...")
            return
        }

        if(formData.date === undefined) {
            window.alert("Du må fylle inn en dato. Ellers får vi ikke holdt oversikt, og da blir det dårlig stemning")
            return
        }
        
        const resp = await fetch('/new-game/', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
              },
            body: JSON.stringify(formData)
        })

        if(resp.status === 201) {
            console.log("Game accepted, hope you played well")
            setIsSaving(false)
        } else {
            console.log("Oooops, an error.")
            setIsSaving(false)
        }
    }

    return (
        <div id={styles.component}>
            
            <h1>Send inn nytt spill</h1>
            <form>
                <TextField name="game_id" onChange={(e) => {
                        handleChange(e)
                    }} id="outlined-basic" label="Game ID" variant="outlined" />
                <TextField
                name="date"
                    id="date"
                    label="Dato"
                    onChange={(e) => {
                        handleChange(e)
                    }}
                    type="date"
                    defaultValue="today"
                    sx={{ width: 220 }}
                    InputLabelProps={{
                    shrink: true,
                    }}
                />
                <Button onClick={handleSave} variant="contained">Send inn</Button>
            </form>
        </div>
    )
}