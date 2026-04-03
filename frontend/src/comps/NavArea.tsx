import * as React from "react";
import styles from "./NavAreaStyle.module.scss";
import { ReactNode } from "react";
import { Link } from "react-router-dom";
import AddIcon from "@mui/icons-material/Add";

const pages = ["Leaderboard"];

export default function NavArea({ children }: { children: ReactNode }) {
  return (
    <div className={styles.shell}>
      <nav className={styles.nav}>
        <div className={styles.navLeft}>
          <Link to="/" className={styles.logo}>
            <span className={styles.logoText}>Geoleague</span>
          </Link>
          <div className={styles.navLinks}>
            {pages.map((page) => (
              <Link
                key={page}
                to={"/" + page.toLowerCase()}
                className={styles.navLink}
              >
                {page}
              </Link>
            ))}
          </div>
        </div>

        <div className={styles.navRight}>
          <Link to="/new-game" className={styles.addButton}>
            <AddIcon style={{ fontSize: 14 }} />
            Nytt spill
          </Link>
        </div>
      </nav>

      <main className={styles.content}>{children}</main>
    </div>
  );
}
