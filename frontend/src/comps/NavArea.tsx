import * as React from "react";
import styles from "./NavAreaStyle.module.scss";
import { ReactNode } from "react";
import {Link} from "react-router-dom"
import AddIcon from '@mui/icons-material/Add';

const pages = ["Leaderboard"];

export default function NavArea({ children }: { children: ReactNode }) {
  const renderLinks = (links: string[]) => {
    return links.map((link) => {
      return (
        <Link className={styles.link} key={link} to={"/" + link.toLowerCase()}>
          {link}
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
                <img src="geoleague.png" alt="Logo for geoleague" />
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
