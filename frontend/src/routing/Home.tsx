import React from "react";
import styles from "../styles/Home.module.scss";

export default function Home() {
  return (
    <div className={styles.main}>
      <div className={styles.hero}>
        <span className={styles.eyebrow}>GeoGuessr · Venneliga</span>
        <h1 className={styles.title}>Velkommen til Geoleague</h1>
        <p className={styles.description}>
          Last opp resultater fra GeoGuessr og hold oversikt over hvem som er
          best til å gjette seg rundt i verden.
        </p>
      </div>
      <div className={styles.memeCard}>
        <img src="meme2.jpg" alt="" />
      </div>
    </div>
  );
}
