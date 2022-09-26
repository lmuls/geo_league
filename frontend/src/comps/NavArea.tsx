import * as React from "react";
import styles from "./NavAreaStyle.module.scss";
import { ReactNode } from "react";
import {Link} from "react-router-dom"
import AddIcon from '@mui/icons-material/Add';

const pages = ["Leaderboard", "Spillere"];

export default function NavArea({ children }: { children: ReactNode }) {
  const renderLinks = (links: string[]) => {
    return links.map((link) => {
      return (
        <Link key={link} to={"/" + link.toLowerCase()}>
          <a className={styles.link}>{link}</a>
        </Link>
      );
    });
  };

  return (
    <div id={styles.mainFrame}>
      <div id={styles.navArea}>
        <nav className={styles.topNav}>
          <div className={styles.topNavLeft}>
            <Link to={"/"}>
              <a>
                <img src="geoleague.png" alt="Logo for geoleague" />
              </a>
            </Link>
            <div className={styles.links}></div>
          </div>
          <div className={styles.topNavRight}>
            <Link to={"/new-game"}>
            <AddIcon />
            
            </Link>
          </div>
        </nav>
        <div id={styles.pageOuterContents}>
          <aside id={styles.asideNav}>
            {renderLinks(pages)}
          </aside>
        <div id={styles.pageContents}>{children}</div>

        </div>
      </div>
    </div>
  );
}
